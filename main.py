from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Scrollbar, Checkbutton, Label, Button
import vis
import os

toolbar_list = ['new_file', 'open_file', 'save', 'cut', 'copy', 'paste',
                'undo', 'redo', 'run']


class DSL4Tree(Tk):
    toolbar_res = []
    file_name = None

    def __init__(self):
        super().__init__()
        self._set_window_()
        self._create_shortcut_bar_()
        self._create_body_()

    def _set_window_(self):
        self.title("DSL4Tree")
        self.is_show_line_num = IntVar()
        self.is_show_line_num.set(1)

    def _create_shortcut_bar_(self):
        shortcut_bar = Frame(self, height=25)
        shortcut_bar.pack(fill='x')

        for i, t in enumerate(toolbar_list):
            tool_btn = Button(shortcut_bar, text=t,
                              command=self._shortcut_action(t))

            tool_btn.pack(side='left')
            self.toolbar_res.append(t)

    def _create_body_(self):
        self.line_number_bar = Text(self, width=4, padx=3, takefocus=0, border=0,
                                    background='#FFFFFF', state='disabled')
        self.line_number_bar.pack(side='left', fill='y')

        self.content_text = Text(self, wrap='word', undo=True)
        self.content_text.pack(expand='yes', fill='both')
        self.content_text.bind('<Control-N>', self.new_file)
        self.content_text.bind('<Control-n>', self.new_file)
        self.content_text.bind('<Control-O>', self.open_file)
        self.content_text.bind('<Control-o>', self.open_file)
        self.content_text.bind('<Control-S>', self.save)
        self.content_text.bind('<Control-s>', self.save)
        self.content_text.bind('<Control-A>', self.select_all)
        self.content_text.bind('<Control-a>', self.select_all)
        self.content_text.bind(
            '<Any-KeyPress>', lambda e: self._update_line_num())
        self.bind('<Escape>', exit_program)

        scroll_bar = Scrollbar(self.content_text)
        scroll_bar["command"] = self.content_text.yview
        self.content_text["yscrollcommand"] = scroll_bar.set
        scroll_bar.pack(side='right', fill='y')

    def _update_line_num(self):
        if self.is_show_line_num.get():
            row, col = self.content_text.index("end").split('.')
            line_num_content = "\n".join([str(i) for i in range(1, int(row))])
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.insert('1.0', line_num_content)
            self.line_number_bar.config(state='disabled')
        else:
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.config(state='disabled')

    def _toggle_highlight(self):
        if self.is_highlight_line.get():
            self.content_text.tag_remove("active_line", 1.0, "end")
            self.content_text.tag_add(
                "active_line", "insert linestart", "insert lineend+1c")
            self.content_text.after(200, self._toggle_highlight)
        else:
            self.content_text.tag_remove("active_line", 1.0, "end")

    def handle_menu_action(self, action_type):
        if action_type == "Undo":
            self.content_text.event_generate("<<Undo>>")
        elif action_type == "Redo":
            self.content_text.event_generate("<<Redo>>")
        elif action_type == "Cut":
            self.content_text.event_generate("<<Cut>>")
        elif action_type == "Copy":
            self.content_text.event_generate("<<Copy>>")
        elif action_type == "Paste":
            self.content_text.event_generate("<<Paste>>")

        if action_type != "Copy":
            self._update_line_num()

        return "break"

    def _shortcut_action(self, type):
        def handle():
            if type == "new_file":
                self.new_file()
            elif type == "open_file":
                self.open_file()
            elif type == "save":
                self.save()
            elif type == "cut":
                self.handle_menu_action("Cut")
            elif type == "copy":
                self.handle_menu_action("Copy")
            elif type == "paste":
                self.handle_menu_action("Paste")
            elif type == "undo":
                self.handle_menu_action("Undo")
            elif type == "redo":
                self.handle_menu_action("Redo")
            elif type == "run":
                self.run()

            if type != "copy" and type != "save" and type != "run":
                self._update_line_num()
        return handle

    def select_all(self, event=None):
        self.content_text.tag_add('sel', '1.0', 'end')
        return "break"

    def new_file(self, event=None):
        self.title("New - DSL4Tree")
        self.content_text.delete(1.0, END)
        self.file_name = None

    def open_file(self, event=None):
        input_file = filedialog.askopenfilename(initialdir=os.getcwd())
        if input_file:
            self.title("%s - DSL4Tree" % os.path.basename(input_file))
            self.file_name = input_file
            self.content_text.delete(1.0, END)
            with open(input_file, 'r') as _file:
                self.content_text.insert(1.0, _file.read())

    def save(self, event=None):
        if not self.file_name:
            self.save_as()
        else:
            self._write_to_file(self.file_name)

    def save_as(self, event=None):
        input_file = filedialog.asksaveasfilename()
        if input_file:
            self.file_name = input_file
            self._write_to_file(self.file_name)

    def _write_to_file(self, file_name):
        try:
            content = self.content_text.get(1.0, 'end')
            with open(file_name, 'w') as the_file:
                the_file.write(content)
            self.title("%s - DSL4Tree" % os.path.basename(file_name))
        except IOError:
            messagebox.showwarning("Save", "Error!")

    def run(self):
        try:
            content = self.content_text.get(1.0, 'end')
            with open(os.path.join(os.getcwd(), 'temp.bt'), 'w') as the_file:
                the_file.write(content)
        except IOError:
            pass
        self.destroy()
        callvis()


def exit_program(event):
    sys.exit()


def callvis():
    vis.exec()


if "__main__" == __name__:
    app = DSL4Tree()
    app.mainloop()
