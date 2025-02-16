import re
from typing import List

from htmlnode import ParentNode
from inline_markdown import markdown_to_blocks, text_to_textnodes
from markdown_blocks import BlockType, block_to_block_type
from textnode import text_node_to_html_node


def extract_tile(markdown: str) -> str:
    match = re.match(r"^# (.*)", markdown)
    if not match:
        raise Exception("document did not begin with a h1")
    return match.group(1)


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    return ParentNode(tag="div", children=blocks_to_html(blocks))


def blocks_to_html(blocks: List[str]) -> List[ParentNode]:
    res = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.TEXT.value:
                res.append(block_to_html(block, "p"))
            case BlockType.HEADING.value:
                sep = block.split()
                num = len(sep[0])
                res.append(block_to_html(" ".join(sep[1:]), f"h{num}"))
            case BlockType.QUOTE.value:
                quote = "\n".join(b.lstrip("> ") for b in block.split("\n"))
                res.append(block_to_html(quote, "blockquote"))
            case BlockType.CODE.value:
                res.append(
                    ParentNode(
                        tag="pre", children=[block_to_html(block.strip("```"), "code")]
                    )
                )
            case BlockType.UNORDERED_LIST.value:
                unordered_list = [
                    block_to_html(" ".join(b.split()[1:]), "li")
                    for b in block.split("\n")
                ]
                res.append(ParentNode(tag="ul", children=unordered_list))
            case BlockType.ORDERED_LIST.value:
                ordered_list = [
                    block_to_html(" ".join(b.split()[1:]), "li")
                    for b in block.split("\n")
                ]
                res.append(ParentNode(tag="ol", children=ordered_list))
            case _:
                raise Exception("invalid block type")
    return res


def block_to_html(block: str, tag: str) -> ParentNode:
    return ParentNode(
        tag=tag,
        children=[text_node_to_html_node(node) for node in text_to_textnodes(block)],
    )
