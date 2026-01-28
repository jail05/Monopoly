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
        self.number_of_property = 0

    def add_color(self,color):
        new = pNode(color,"COLOR")
        self.root.addChild(new)
        return new

    def add_property(self,color,property):
        new = pNode(property,"PROPERTY")
        color.add_child(new)
        self.number_of_property += 1
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
        self.number_of_property -= 1

    def has_property(self,node,property):
        if not node.node_type== "PROPERTY" and node.value==property:
            return True

        for child in node.children:
            if self.has_property(child,property):
                return True

        return False
    def get_property_count(self):
        return self.number_of_property

    def clear_all_properties(self):

        for color_node in self.root.children:


            properties = []

            for child in color_node.children:
                if child.node_type == "PROPERTY":
                    properties.append(child)


            for prop_node in properties:
                prop_node.value.owner_id = None
                color_node.removeChild(prop_node)
                self.number_of_property -= 1

    def export(self):
        result = {}
        for color_node in self.root.children:
            color = color_node.value
            result[color] = []

            for prop_node in color_node.children:
                if prop_node.node_type == "PROPERTY":
                    prop = prop_node.value
                    result[color].append({
                        "property_id": prop.ID,
                        "houses": prop.house_count,
                        "hotel": prop.has_hotel_,
                        "mortgaged": prop.mortgaged
                    })
        return result




