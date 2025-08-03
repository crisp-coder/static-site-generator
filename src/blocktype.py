from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_blocktype(block_text):
    if block_text.startswith("#"):
        return BlockType.HEADING
    elif block_text.startswith("```") and block_text.endswith("```"):
        return BlockType.CODE
    elif block_text.startswith(">"):
        return BlockType.QUOTE
    elif block_text.startswith("-"):
        return BlockType.UNORDERED_LIST

    for i in range(len(block_text)):
        if block_text[i].isnumeric():
            for j in range(i, len(block_text)):
                if block_text[j] == '.':
                    return BlockType.ORDERED_LIST
                elif not block_text[j].isnumeric():
                    break
            break

    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    text_blocks = markdown.split("\n\n")
    blocks = []
    for item in text_blocks:
        if item != "":
            blocks.append(item.strip())

    return blocks

