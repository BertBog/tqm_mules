import argparse
from datetime import datetime
from pathlib import Path

from tqmmules.app.itemdb import ItemDB
from tqmmules.app.saveparser import SaveParser
from tqmmules.app.tqmmlogger import logger, initialize_logging
from tqmmules.version import __version__


def _parse_args() -> argparse.Namespace:
    """
    Parses the command line arguments.
    :return: Parsed arguments
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--dir-in', type=Path, required=True, help='Directory with TQ save files')
    argument_parser.add_argument('--output', type=Path, required=False, help='Output file')
    argument_parser.add_argument('--skip-annot', action='store_true', help='Skip the item annotation')
    argument_parser.add_argument('--debug', action='store_true', help='Show debug messages')
    argument_parser.add_argument(
        '--version', help='Print version and exit', action='version', version=f'tqm_mules {__version__}')
    return argument_parser.parse_args()


def run() -> None:
    """
    Runs the script.
    :return: None
    """
    args = _parse_args()
    initialize_logging(args.debug)

    # Set the output path
    if args.output is None:
        timestamp_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        args.output = Path.cwd() / f'output_{timestamp_str}.tsv'
        logger.info(f'Output location not specified, defaulting to {args.output}')

    # Find save files
    logger.info(f'Parsing saves in directory: {args.dir_in}')
    if not all(x in {p.name for p in args.dir_in.iterdir()} for x in ('Main', 'Sys')):
        logger.warning("The 'Sys' and 'Main' directories were not found in the input directory")
    path_saves_chr = list(p for p in args.dir_in.glob('**/Player.chr') if p.parent.name != 'Backup')
    paths_saves = list(args.dir_in.glob('**/*winsys.dxb')) + path_saves_chr
    logger.info(f'Found {len(paths_saves):,} save files, {len(path_saves_chr):,} characters')

    # Parse the saves
    records_out = SaveParser.parse_all(paths_saves)
    logger.info(f'Parsed {len(records_out):,} items')
    if len(records_out) == 0:
        logger.info('No items could be parsed')
        exit(0)

    # Annotate items with additional info
    if not args.skip_annot:
        db_items = ItemDB()
        records_out = db_items.annotate_all(records_out)

    # Create the output file
    with open(args.output, 'w') as handle:
        handle.write('\t'.join(str(x) for x in records_out[0].keys() if x not in ('save',)))
        handle.write('\n')
        for row in records_out:
            handle.write('\t'.join(str(v) for k, v in row.items() if k not in ('save',)))
            handle.write('\n')
    logger.info(f'Output exported to: {args.output}')


if __name__ == '__main__':
    run()
