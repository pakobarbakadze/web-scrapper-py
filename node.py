class Node:
    def __init__(self, container, element, class_name):
        self.container = container
        self.element = element
        self.className = class_name

    def get_text(self):
        curr_node = self.container.find(self.element, class_=self.className)
        if curr_node is not None:
            return curr_node.text
        else:
            return None

    def get_link(self):
        curr_node = self.container.find(self.element, class_=self.className)
        if curr_node is not None:
            return curr_node["href"]
        else:
            return None

    def get_email(self):
        into_container = self.container.find(self.element, class_=self.className)
        infos = into_container.findAll("li")
        for info in infos:
            if "@" in info.text:
                return info.text.strip()
        return None
