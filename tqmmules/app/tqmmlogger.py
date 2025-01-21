import logging


logger = logging.getLogger('tqm_mules')


def initialize_logging(debug: bool = False) -> None:
    """
    Initializes the logging.
    :param debug: If True, debug messages are printed
    :return: None
    """
    formatter = logging.Formatter('%(asctime)s - %(module)15s - %(levelname)7s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.name = 'console'
    logger.addHandler(console_handler)

    # General logging level
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
