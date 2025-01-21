# TQM mules
TQM mules is a package to parse save files from the mobile version of Titan Quest Legendary Edition. 

**Note:** It currently does **not** support any save file editing. It is solely meant to help with inventory management
across characters (i.e., mules) on mobile. 

**Note:** All items can be parsed, but currently common items cannot be annotated (i.e., grey, yellow and green).

----

## INSTALLATION

### Dependencies 

- [Python 3](https://www.python.org/downloads/)


The script has no external dependencies and can be run immediately after cloning the repository. However, if you execute 
it this way, ensure you are in the project's root directory.

```
git clone https://github.com/BertBog/tqm_mules.git
cd tqm_mules
python3 tqmmules/scripts/parse_saves.py
```

Alternatively, the package can be installed in the current Python environment, allowing it to be executed from any 
location.

```
git clone https://github.com/BertBog/tqm_mules.git
cd tqm_mules
pip install .
parse_saves.py  # On UNIX
parse_saves.exe  # On Windows 
```

-----

## USAGE

The save data is usually located in the following directory:
`Android\data\com.hg.titanquestedition\files\Preferences\SaveData`

The script does not make any changes, but I suggest you make a backup just in case.
The script expects the `Main` and `Sys` directories to be present in the input directory.

### Example

```
python tqmmules/scripts/parse_saves.py --dir-in /path/to/SaveData
```

### Options

```
usage: parse_saves.py [-h] --dir-in DIR_IN [--output OUTPUT] [--skip-annot]
                      [--debug]

options:
  -h, --help       show this help message and exit
  --dir-in DIR_IN  Directory with TQ save files
  --output OUTPUT  Output file
  --skip-annot     Skip the item annotation
  --debug          Show debug messages
  --version        Print version and exit
```

-----

## CONTACT

[Create an issue](https://github.com/BioinformaticsPlatformWIV-ISP/PACU/issues) to report bugs, propose new functions or ask for help.

**Note:** I won’t have much time to implement additional features. Feel free to modify the code to add any functionality
you need.  

-----

## ACKNOWLEDGEMENTS

- THQ Nordic AB – For developing and publishing this excellent mobile port.
- [TQVaultAE](https://github.com/EtienneLamoureux/TQVaultAE) – For inspiring the approach to parsing save files.
- [TQDB](https://github.com/fonsleenaars/tqdb) – For providing valuable insights into item data parsing.

-----

## DISCLAIMER

Titan Quest, THQ and their respective logos are trademarks and/or registered trademarks of THQ Nordic AB. This 
non-commercial project is in no way associated with THQ Nordic AB.
