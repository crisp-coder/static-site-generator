from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # Skip parsing if node is not a text node.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Split the node into multiple nodes and add them in the old node's place
        if delimiter in node.text:
            new_text_list = node.text.split(delimiter)
            if len(new_text_list) % 2 != 1:
                raise Exception(f"Unmatched delimiter {delimiter}")

            # Track text type because som e of the new nodes will still be text,
            # and some will have changed.
            next_text_type = TextType.TEXT
            for split_text in new_text_list:
                # Skip empty nodes
                if split_text != "":
                    new_node = TextNode(split_text, next_text_type, node.url)
                    new_nodes.append(new_node)

                # swap text types each iteration of loop.
                if next_text_type  == TextType.TEXT:
                    next_text_type  = text_type
                elif next_text_type  == text_type:
                    next_text_type  = TextType.TEXT

        # We still need to keep the node if no delimiter is found.
        else:
            new_nodes.append(node)
    return new_nodes



