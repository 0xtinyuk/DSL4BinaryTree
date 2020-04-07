import tkinter
from PIL import Image, ImageTk
import functools
import rbtree
import bstree
import tree_process
import time
import copy
import sys


class Vis(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.index_displayed = -1
        self.bt = tree_process.getmodel()
        self.tree = copy.copy(self.bt)
        self.tree.snapshot()
        self._set_window_()
        self._create_body_()

    def _set_window_(self):
        self.title('RBTree_Visualization')
        self.resizable(True, True)
        self.geometry("")
        self.wm_attributes('-topmost', 1)
        self.after(1000, lambda: self.attributes("-topmost", 0))

    def _create_body_(self):
        self.protocol('WM_DELETE_WINDOW', self.exit_program)
        self.frame1 = tkinter.Frame(self, bd=2, relief='solid')
        self.label_img = tkinter.Label(self.frame1)
        self.label_img.pack(expand=1)
        self.frame2 = tkinter.Frame(self, relief='solid')
        self.b_switch_to_binarytree = tkinter.Button(
            self.frame2, text="BinaryTree")
        self.b_pre_order = tkinter.Button(self.frame2, text="Pre-order")
        self.b_in_order = tkinter.Button(self.frame2, text="In-order")
        self.b_post_order = tkinter.Button(self.frame2, text="Post-order")
        self.b_switch_to_bst = tkinter.Button(self.frame2, text="BSTree")
        self.b_switch_to_rbt = tkinter.Button(self.frame2, text="RBTree")
        self.b_run = tkinter.Button(self.frame2, text="RunOps")
        self.b_next = tkinter.Button(self.frame2, text="Next")
        self.b_previous = tkinter.Button(self.frame2, text="Previous")
        self.b_switch_to_binarytree.bind(
            "<Button-1>", self.switch_to_binarytree)
        self.b_switch_to_bst.bind("<Button-1>", self.switch_to_bstree)
        self.b_switch_to_rbt.bind("<Button-1>", self.switch_to_rbtree)
        self.b_pre_order.bind("<Button-1>", self.pre_order_traversal)
        self.b_in_order.bind("<Button-1>", self.in_order_traversal)
        self.b_post_order.bind("<Button-1>", self.post_order_traversal)
        self.b_next.bind("<Button-1>", self.next_img)
        self.b_previous.bind("<Button-1>", self.last_img)
        self.b_run.bind("<Button-1>", self.run_ops)
        self.b_run.config(state=tkinter.DISABLED)
        self.frame1.grid(row=0)
        self.frame2.grid(row=1)
        self.b_switch_to_binarytree.pack(side=tkinter.LEFT, fill=tkinter.X)
        self.b_switch_to_binarytree.config(state=tkinter.DISABLED)
        self.b_post_order.pack(side=tkinter.RIGHT)
        self.b_in_order.pack(side=tkinter.RIGHT)
        self.b_pre_order.pack(side=tkinter.RIGHT)
        self.b_next.pack(side=tkinter.RIGHT)
        self.b_previous.pack(side=tkinter.RIGHT)
        self.b_run.pack(side=tkinter.RIGHT)
        self.b_switch_to_rbt.pack(side=tkinter.RIGHT)
        self.b_switch_to_bst.pack(side=tkinter.RIGHT)
        self.frame1.grid_propagate(False)
        self.load_img()

    def title_type(self):
        if type(self.tree) == rbtree.RBTree:
            return 'RBTree Visualization {}/{}'
        elif type(self.tree) == bstree.BSTree:
            return 'BSTree Visualization {}/{}'
        else:
            return 'BinaryTree Visualization {}/{}'

    def load_img(self):
        if self.index_displayed+1 > self.tree.index:
            return
        self.index_displayed += 1
        baseheight = 400
        img = Image.open('pics/output{}.png'.format(self.index_displayed))
        self.title(self.title_type().format(
            self.index_displayed, self.tree.index))
        print('printing pics/output{}.png'.format(self.index_displayed))
        hpercent = (baseheight/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
        img_png = ImageTk.PhotoImage(img, master=self)
        self.label_img.configure(image=img_png)
        self.label_img.image = img_png

    def load_last_img(self):
        if self.index_displayed-1 <= 0:
            return
        self.index_displayed -= 1
        baseheight = 400
        img = Image.open('pics/output{}.png'.format(self.index_displayed))
        self.title(self.title_type().format(
            self.index_displayed, self.tree.index))
        print('displaying pics/output{}.png'.format(self.index_displayed))
        hpercent = (baseheight/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
        img_png = ImageTk.PhotoImage(img, master=self)
        self.label_img.configure(image=img_png)
        self.label_img.image = img_png

    def next_img(self, event):
        self.load_img()

    def last_img(self, event):
        self.load_last_img()

    def keep_loading_img(self):
        if self.index_displayed > self.tree.index:
            self.index_displayed = -1
            self.load_img()
            return
        if self.index_displayed+1 <= self.tree.index:
            self.load_img()
            if self.index_displayed+1 <= self.tree.index:
                self.after(2000, self.keep_loading_img)

    def run_ops(self, event):
        tkinter.messagebox.showinfo(
            'Operations', '{}'.format(self.bt.ops))
        self.b_run.config(state=tkinter.DISABLED)
        for i in self.bt.ops:
            o = i[0]
            val = i[1]
            if o == 'i':
                if not self.tree.search_node(val):
                    if type(self.tree) == rbtree.RBTree:
                        self.tree.add_node(
                            rbtree.RBTreeNode(val, "R"), snap=True)
                    elif type(self.tree) == bstree.BSTree:
                        self.tree.add_node(
                            bstree.BSTreeNode(val, "B"), snap=True)
                    else:
                        pass
                pass
            elif o == 'd':
                if self.tree.search_node(val):
                    self.tree.delete_node(val, snap=True)
        self.keep_loading_img()
        pass

    def switch_to_bstree(self, event):
        self.tree = bstree.BSTree()
        for i in self.bt.content:
            self.tree.add_node(bstree.BSTreeNode(i, "B"), snap=False)
        self.b_switch_to_bst.config(state=tkinter.DISABLED)
        self.b_switch_to_binarytree.config(state=tkinter.NORMAL)
        self.b_switch_to_rbt.config(state=tkinter.NORMAL)
        self.b_pre_order.config(state=tkinter.NORMAL)
        self.b_in_order.config(state=tkinter.NORMAL)
        self.b_post_order.config(state=tkinter.NORMAL)
        self.b_run.config(state=tkinter.NORMAL)
        self.index_displayed = -1
        self.tree.snapshot()
        self.keep_loading_img()
        pass

    def switch_to_rbtree(self, event):
        self.tree = rbtree.RBTree()
        for i in self.bt.content:
            self.tree.add_node(rbtree.RBTreeNode(i, "R"), snap=False)
        self.b_switch_to_bst.config(state=tkinter.NORMAL)
        self.b_switch_to_binarytree.config(state=tkinter.NORMAL)
        self.b_switch_to_rbt.config(state=tkinter.DISABLED)
        self.b_pre_order.config(state=tkinter.DISABLED)
        self.b_in_order.config(state=tkinter.DISABLED)
        self.b_post_order.config(state=tkinter.DISABLED)
        self.b_run.config(state=tkinter.NORMAL)
        self.index_displayed = -1
        self.tree.snapshot()
        self.keep_loading_img()
        pass

    def switch_to_binarytree(self, event):
        self.tree = copy.copy(self.bt)
        self.b_switch_to_bst.config(state=tkinter.NORMAL)
        self.b_switch_to_binarytree.config(state=tkinter.DISABLED)
        self.b_switch_to_rbt.config(state=tkinter.NORMAL)
        self.b_pre_order.config(state=tkinter.NORMAL)
        self.b_in_order.config(state=tkinter.NORMAL)
        self.b_post_order.config(state=tkinter.NORMAL)
        self.b_run.config(state=tkinter.DISABLED)
        self.index_displayed = -1
        self.tree.snapshot()
        self.keep_loading_img()
        pass

    def pre_order_traversal(self, event):
        if type(self.tree) == rbtree.RBTree:
            return
        result = self.tree.pre_order_traversal(self.tree.root)
        self.tree.snapshot()
        tkinter.messagebox.showinfo(
            'Traversal Result', 'The order of traversal is {}'.format(result))
        self.keep_loading_img()
        pass

    def in_order_traversal(self, event):
        if type(self.tree) == rbtree.RBTree:
            return

        result = self.tree.in_order_traversal(self.tree.root)
        self.tree.snapshot()
        tkinter.messagebox.showinfo(
            'Traversal Result', 'The order of traversal is {}'.format(result))
        self.keep_loading_img()
        pass

    def post_order_traversal(self, event):
        if type(self.tree) == rbtree.RBTree:
            return

        result = self.tree.post_order_traversal(self.tree.root)
        self.tree.snapshot()
        tkinter.messagebox.showinfo(
            'Traversal Result', 'The order of traversal is {}'.format(result))
        self.keep_loading_img()
        pass

    def exit_program(self):
        self.destroy()
        sys.exit()


def exec():
    app = Vis()
    app.mainloop()
