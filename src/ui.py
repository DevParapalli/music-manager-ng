import py_cui

class UserInterface:
    def __init__(self, root: py_cui.PyCUI) -> None:
        self.root = root

        self.text_box = self.root.add_label("THIS SHOULD BE THE UI", 3, 2)

def run_ui():
    root = py_cui.PyCUI(7, 6)
    root.set_title("PyCUI Test")
    ui = UserInterface(root)
    root.set_refresh_timeout(0.1)
    root.start()
