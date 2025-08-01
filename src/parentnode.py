from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node missing tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Parent node has no children")
        
        inner_html = ""
        for child in self.children:
            inner_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{inner_html}</{self.tag}>'

