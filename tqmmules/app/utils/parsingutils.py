import dataclasses
import re
import struct
from typing import Tuple, List, Dict

RE_PATTERN = "begin_block.*?end_block"


@dataclasses.dataclass
class Record:
    """
    Dataclass to hold data for a key in a block.
    """

    value_as_str: str
    value_as_bytes: bytes


def read_string(value_bytes: bytes) -> str:
    """
    Reads a string from a bytes value.
    :param value_bytes: Bytes value
    :return: Parsed string
    """
    str_len = struct.unpack("<I", value_bytes[0:4])[0]
    str_txt = value_bytes[4 : str_len + 4].decode("utf-8").strip()
    return str_txt


def read_int(value_bytes: bytes) -> int:
    """
    Reads an integer from a bytes value.
    :param value_bytes: Bytes value
    :return: Parsed integer
    """
    value = struct.unpack("<Q", value_bytes)[0]
    return value


def read_utf16(value_bytes: bytes) -> str:
    """
    Reads an UTF16 string from a bytes value.
    :param value_bytes: Bytes value
    :return: Parsed string
    """
    str_length = struct.unpack("<I", value_bytes[:4])[0]
    return (
        value_bytes[4 : 4 + (str_length * 4)]
        .decode(encoding="utf-16")
        .encode("latin1")
        .decode("utf-16")
    )


def determine_value_end(idx: int, start_with_key: List[Tuple[str, int]], block_end: int) -> int:
    """
    Determines where the current value ends (based on the next key).
    :param idx: Index
    :param start_with_key: List of tuples with the start of each key
    :param block_end: End of the block
    :return: Value end
    """
    if idx + 1 < len(start_with_key):
        key_next, val_start_next = start_with_key[idx + 1]
        return val_start_next - len(key_next)
    return block_end


KEYS = {
    "baseName": read_string,
    "prefixName": read_string,
    "suffixName": read_string,
    "relicName": read_string,
    "relicBonus": read_string,
    "seed": read_int,
    "var1": read_int,
    "relicName2": read_string,
    "relicBonus2": read_string,
    "var2": read_int,
}


def extract_record_from_match(block: re.Match, data_as_str: str, data_raw: bytes) -> Dict[str, Record]:
    """
    Extracts a record from a block regex match.
    :param block: regex match of the block
    :param data_as_str: Data as string
    :param data_raw: Raw data
    :return: Record information
    """
    item_data_as_str = data_as_str[block.start() : block.end()]

    # Determine that start of the value for each key
    key_with_idx_val_start = [
        (key, block.start() + item_data_as_str.index(key) + len(key))
        if key in item_data_as_str
        else None
        for key in KEYS
    ]

    # Determine the endpoint of the value (9 is the length of 'end_block')
    key_with_idx_interval = [
        (
            key,
            val_start,
            determine_value_end(i, key_with_idx_val_start, block.end() - 9),
        )
        for i, (key, val_start) in enumerate(key_with_idx_val_start)
    ]

    # Get the hex value of the key
    record_by_key = {}
    for key, v_start, v_end in key_with_idx_interval:
        record_by_key[key] = Record(
            value_as_str=data_as_str[v_start:v_end],
            value_as_bytes=data_raw[v_start:v_end],
        )
    return record_by_key
