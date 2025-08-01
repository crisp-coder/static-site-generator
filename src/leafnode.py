from src.htmlnode import HTMLNode
from src.textnode import TextNode, TextType

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError()
        if self.tag:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        else:
            return f'{self.value}'


