class Node:
    def __init__(self , data):
        self.data = data
        self.left = None
        self.right = None


class Tree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        new_node = Node(data)

        if not self.root:
            self.root = new_node
            return

        queue = [self.root]
        while queue:
            current = queue.pop(0)

            if not current.left:
                current.left = new_node
                return
            else:
                queue.append(current.left)

            if not current.right:
                current.right = new_node
                return
            else:
                queue.append(current.right)

    def find_node(self, data):
        if not self.root:
            return None

        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.data == data:
                return current
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        return None

    def delete(self, node):
        if not self.root or not node:
            return

        parent = self.parent(node)

        if not node.left and not node.right:
            replacement = None

        elif node.left and not node.right:
            replacement = node.left
        elif node.right and not node.left:
            replacement = node.right
        else:
            replacement = node.right

        if parent is None:
            self.root = replacement
        else:
            if parent.left == node:
                parent.left = replacement
            else:
                parent.right = replacement

    def get_height(self, node):
        if node is None:
            return -1

        return 1 + max(self.get_height(node.left),self.get_height(node.right))

    def get_size(self, node):
        if node is None:
            return 0
        return 1 + self.get_size(node.left) + self.get_size(node.right)

    def LMC(self):
        if not self.root:
            return None

        current = self.root
        while current.left:
            current = current.left

        return current

    def parent(self, node):
        if not self.root or self.root == node:
            return None

        queue = [self.root]
        while queue:
            current = queue.pop(0)

            if current.left == node or current.right == node:
                return current

            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        return None

    def print_preorder(self, node):
        if node is None:
            return
        print(node.data, end=" ")
        self.print_preorder(node.left)
        self.print_preorder(node.right)

    def print_postorder(self, node):
        if node is None:
            return
        self.print_postorder(node.left)
        self.print_postorder(node.right)
        print(node.data, end=" ")

    def print_inorder(self, node):
        if node is None:
            return
        self.print_inorder(node.left)
        print(node.data, end=" ")
        self.print_inorder(node.right)

    def create_tree(self, inorder, postorder):
        if not inorder or not postorder:
            return None

        root_value = postorder.pop()
        root = Node(root_value)

        index = inorder.index(root_value)

        root.right = self.create_tree(inorder[index + 1:], postorder)
        root.left = self.create_tree(inorder[:index], postorder)

        self.root = root
        return root




