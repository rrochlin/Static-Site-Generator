import re
from typing import List

from textnode import TextNode, TextType


def split_wrapper(delimiter: str, text_type: TextType):
    def wrapper(old_nodes: List[TextNode]):
        return split_nodes_delimiter(old_nodes, delimiter, text_type)

    return wrapper


code_split = split_wrapper("`", TextType.CODE)
italic_split = split_wrapper("*", TextType.ITALIC)
bold_split = split_wrapper("**", TextType.BOLD)


def text_to_textnodes(text: str) -> List[TextNode]:
    input_text = TextNode(text, TextType.TEXT)
    return code_split(
        italic_split(bold_split(split_nodes_link(split_nodes_image([input_text]))))
    )


def extract_markdown_images(text: str) -> List[str]:
    pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
    return pattern.findall(text)


def extract_markdown_links(text: str) -> List[str]:
    pattern = re.compile(r"\[(.*?)\]\((.*?)\)")
    return pattern.findall(text)


def markdown_to_blocks(markdown: str) -> List[str]:
    res = []
    blocks = markdown.split("\n\n")
    block = ""
    for block in blocks:
        if not block:
            continue
        res.append(block.strip())
    return res


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue
        # TODO do something with the URL
        node: TextNode
        parts = node.text.split(delimiter)
        if len(parts) < 3:
            res.append(node)
            continue
        for idx, part in enumerate(parts):
            if not part:
                continue
            res.append(TextNode(part, text_type if idx % 2 else node.text_type))
    return res


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue
        node: TextNode
        matches = extract_markdown_images(node.text)
        raw_text = node.text
        start = 0
        for match in matches:
            image_text = f"![{match[0]}]({match[1]})"
            idx = raw_text.find(image_text, start)
            if start != idx:
                res.append(TextNode(raw_text[start:idx], node.text_type))
            res.append(TextNode(match[0], TextType.IMAGES, match[1]))
            start = idx + len(image_text)
        if start < len(node.text):
            res.append(TextNode(raw_text[start:], node.text_type))
    return res


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue
        node: TextNode
        matches = extract_markdown_links(node.text)
        raw_text = node.text
        start = 0
        for match in matches:
            link_text = f"[{match[0]}]({match[1]})"
            idx = raw_text.find(link_text, start)
            if start != idx:
                res.append(TextNode(raw_text[start:idx], node.text_type))
            res.append(TextNode(match[0], TextType.LINKS, match[1]))
            start = idx + len(link_text)
        if start < len(node.text):
            res.append(TextNode(raw_text[start:], node.text_type))
    return res
