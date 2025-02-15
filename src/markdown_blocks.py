import re
from enum import Enum
from typing import Dict


class BlockType(Enum):
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"
    TEXT = "Normal"


def block_to_block_type(block: str) -> str:
    block_def: Dict[str, BlockType] = {
        r"^#{1,6} ": BlockType.HEADING,
        r"```[\s\S]*```": BlockType.CODE,
        r"^>": BlockType.QUOTE,
        r"^[*-] ": BlockType.UNORDERED_LIST,
        r"^(\d+). ": BlockType.ORDERED_LIST,
    }
    for pattern in block_def:
        if validate_block_type(block, block_def[pattern], pattern):
            return block_def[pattern].value
    return BlockType.TEXT.value


def validate_block_type(block: str, block_type: BlockType, pattern: str):
    try:
        match block_type:
            case BlockType.HEADING:
                return re.match(pattern, block)
            case BlockType.CODE:
                return re.match(pattern, block)
            case BlockType.QUOTE:
                expected_len = len(block.split("\n"))
                return len(re.findall(pattern, block, re.MULTILINE)) == expected_len
            case BlockType.UNORDERED_LIST:
                expected_len = len(block.split("\n"))
                return len(re.findall(pattern, block, re.MULTILINE)) == expected_len
            case BlockType.ORDERED_LIST:
                expected_len = len(block.split("\n"))
                matches = [int(i) for i in re.findall(pattern, block, re.MULTILINE)]
                return len(matches) == expected_len and sorted(matches) == matches
            case _:
                return False
    except Exception as _:
        return False
