from xdg.Config import root_mode


class pNode:
    def __init__(self,value,node_type):
        self.value = value
        self.node_type = node_type
        self.children = []

    def addChild(self,child):
        self.children.append(child)

    def removeChild(self,child):
        self.children.remove(child)

class PropertyTree:
    def __init__(self,player):
        self.root = pNode(player,"PLAYER")

    def add_color(self,color):
        new = pNode(color,"COLOR")
        self.root.addChild(new)
        return new

    def add_property(self,color,property):
        new = pNode(property,"PROPERTY")
        color.add_child(new)
        return new

    def add_house(self,property):
        new = pNode("house","HOUSE")
        property.add_child(new)

    def add_hotel(self,property):
        new = pNode("hotel","HOTEL")
        property.add_child(new)

    def remove_property(self,color,property):
        property.owner_id = None
        color.remove_child(property)

    def has_property(self,node,property):
        if not node.node_type== "PROPERTY" and node.value==property:
            return True

        for child in node.children:
            if self.has_property(child,property):
                return True

        return False






