# coding: utf-8


class Node(object):
    cnt = 0

    def __init__(self, url):
        self.id = Node.cnt
        self.url = url
        self.children = []
        self.depth = 0
        Node.cnt += 1

    def add_child(self, node):
        node.depth = self.depth + 1
        node.rebuild()
        self.children.extend([node])

    def add_children(self, nodes):
        self.children.extend(nodes)
        self.rebuild()

    def rebuild(self):
        for c in self.children:
            c.depth = self.depth + 1
            c.rebuild()

    def _format_json_info(self):
        info = "'name': '{}', 'id': '{}'".format(self.url, self.id)
        children_list = [c._format_json_info() for c in self.children]
        children_json = ",".join(children_list)
        if children_json != "":
            info += ", 'children': [{}]".format(children_json)
        return "{" + info + "}"

    def create_data_js(self):
        return "const data = " + self._format_json_info() + ";"
        # return self._format_json_info()


if __name__ == "__main__":
    n1 = Node("n1")
    n2 = Node("n2")
    n3 = Node("n3")
    n4 = Node("n4")
    n5 = Node("n5")
    n6 = Node("n6")
    n7 = Node("n7")
    n8 = Node("n8")

    n1.add_children([n2, n3, n4])
    n2.add_children([n5, n6])
    n3.add_children([n7])
    n7.add_children([n8])

    print(n1.create_json())
2
