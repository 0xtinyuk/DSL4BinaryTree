from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from rbtree import RBTree, RBTreeNode
from bstree import BSTree, BSTreeNode


class BinaryTreeNode(BSTreeNode):
    def __init__(self, val, color="B"):
        self.val = val
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class BinaryTree(BSTree):
    def __init__(self):
        self.root = None
        self.index = -1
        self.action = ""
        self.ops = []
        self.content = []

    def interpret(self, model):
        for t in model.BinaryTrees:
            self.root = self.build(t)
            break

        for op in model.Operations:
            if op.__class__.__name__ == "Insert":
                self.ops.append(('i', op.val))
            if op.__class__.__name__ == "Delete":
                self.ops.append(('d', op.val))
        print(self.content)
        print(self.ops)
        return

    def build(self, t):
        if t.__class__.__name__ == 'NoneType':
            return None
        if t.BinaryTreeNodes.__class__.__name__ == 'Node':
            self.content.append(t.BinaryTreeNodes.val)
            current = BinaryTreeNode(t.BinaryTreeNodes.val)
            current.left = self.build(t.BinaryTreeNodes.left)
            current.right = self.build(t.BinaryTreeNodes.right)
            return current
        if t.BinaryTreeNodes.__class__.__name__ == 'INTNode':
            self.content.append(t.BinaryTreeNodes.val)
            return BinaryTreeNode(t.BinaryTreeNodes.val)
        if t.BinaryTreeNodes.__class__.__name__ == 'NULLNode':
            return None


def getmodel(debug=False):
    this_folder = dirname(__file__)
    bt_mm = metamodel_from_file(
        join(this_folder, 'BinaryTree.tx'), debug=False)
    metamodel_export(bt_mm, join(this_folder, 'bt_meta.dot'))
    bt_model = bt_mm.model_from_file(join(this_folder, 'temp.bt'))
    model_export(bt_model, join(this_folder, 'temp.dot'))
    binarytree = BinaryTree()
    binarytree.interpret(bt_model)
    return binarytree


if __name__ == "__main__":
    getmodel()
