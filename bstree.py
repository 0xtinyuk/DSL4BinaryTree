from rbtree import RBTree, RBTreeNode


class BSTreeNode(RBTreeNode):
    def __init__(self, val, color="B"):
        self.val = val
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class BSTree(RBTree):

    def __init__(self):
        super().__init__()

    def left_rotate(self, node):
        pass

    def right_rotate(self, node):
        pass

    def check_node(self, node, snap=True):
        pass

    def check_delete_node(self, node, snap=True):
        pass

    def pre_order_traversal(self, node, snap=True):
        if node == None:
            return []

        result = [node.val]
        node.set_red_node()
        self.snapshot(snap)
        node.set_black_node()
        result.extend(self.pre_order_traversal(node.left))
        result.extend(self.pre_order_traversal(node.right))
        return result

    def in_order_traversal(self, node, snap=True):
        if node == None:
            return []

        result = self.in_order_traversal(node.left)
        node.set_red_node()
        self.snapshot(snap)
        node.set_black_node()
        result.extend([node.val])
        result.extend(self.in_order_traversal(node.right))
        return result

    def post_order_traversal(self, node, snap=True):
        if node == None:
            return []

        result = self.post_order_traversal(node.left)
        result.extend(self.post_order_traversal(node.right))
        node.set_red_node()
        self.snapshot(snap)
        node.set_black_node()
        result.extend([node.val])
        return result
