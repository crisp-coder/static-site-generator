


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        if children == None:
            self.children = []
        else:
            self.children = children
        if props == None:
            self.props = {}
        else:
            self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        prop_str = ""
        if self.props:
            for key in self.props.keys():
                prop_str += f' {key}="{self.props[key]}"'
        return prop_str

    def __eq__(self, other):
        return self.tag == other.tag \
        and self.value == other.value \
        and self.children == other.children \
        and self.props == other.props

    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'

