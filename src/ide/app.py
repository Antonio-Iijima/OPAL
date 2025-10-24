from src.ide.editor import EditorFrame, Editor, FilteredDirectoryTree, EditorTabs
from src.ide.terminal import TerminalFrame, TerminalLog, TerminalInput, Terminal

from src.lang import interpreter as INT
from src.lang import repl as REP

from textual.widgets import Footer, TabPane, Input
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.binding import Binding
from textual import on

import sys



class IDE(App):


    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.theme = 'gruvbox'


    def compose(self) -> ComposeResult:
        yield IDEFrame(id="IDEFrame", classes="universal")
        yield Footer(compact=True)



class IDEFrame(Horizontal):


    BINDINGS = [
        Binding("ctrl+w", "close_tab()", "Close", priority=True),
        Binding("ctrl+s", "save_file()", "Save"),
        Binding("ctrl+r", "run_file()", "Run")
    ]
    

    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.selected_file = None
        self.selected_id = None

        sys.setrecursionlimit(10**5)
        self.REPL = REP.REPL()
        self.EXPR = ""


    def _on_mount(self, event):
        self.init_opal_interpreter()

        self.tabs = self.query_one(EditorTabs)
        self.query_one(Terminal).border_title = f"OPAL v{INT.interpreter.VERSION}"        

        return super()._on_mount(event)


    def init_opal_interpreter(self):

        # Setup interpreter with flags
        INT.interpreter = INT.Interpreter(
            flags = {
            '-i' : True, # interactive interpreter
            '-d' : self.query_one("#-d").value, # debugging
            '-p' : self.query_one("#-p").value, # permanent extension changes; not typically recommended
            '-z' : self.query_one("#-z").value  # why
        })


    def compose(self) -> ComposeResult:
        yield EditorFrame(id="EditorFrame", classes="primary")
        yield TerminalFrame(id="TerminalFrame", classes="primary")


    def _get_current_editor(self) -> Editor:
        return self.tabs.query_one(f"#{self.tabs.active}").query_one(Editor)


    def _update_selection(self, file):
        if file is None:
            self.selected_file = self.selected_id = None
        else:
            self.selected_file = file
            self.selected_id = str(file).replace("/", "-").replace(".", "_")


    def process_input(self, stream, fromTerminal: bool = True) -> None:
        if fromTerminal:
            self.EXPR += f"{stream}\n"
            line = self.REPL.RER(self.EXPR.strip())
            if not isinstance(line, REP.REPL.Incomplete): self.EXPR = ""
            if not isinstance(line, REP.REPL.Comment) and line.get() != None: self.query_one(TerminalLog).write(line.get())
        else:  
            for line in self.REPL.RERL(stream):
                if line.get() != None: self.query_one(TerminalLog).write(line.get())
        terminal = self.query_one(Terminal)
        terminal.call_later(terminal.scroll_end, animate=True, speed=0) # easing="in_out_cubic"


    def _on_unmount(self):
        INT.interpreter.exit_extensions()
        return super()._on_unmount()


    @on(Input.Submitted)
    def write_input_to_terminal(self, event):
        self.query_one(TerminalInput).clear()

        log = self.query_one(TerminalLog)

        if event.value == "clear": log.clear()
        elif event.value in ("exit", "quit"): 
            INT.interpreter.exit_extensions()
            self.query_ancestor(IDE).exit()
        else:
            log.write(f"{self.REPL.prompt()}{event.value}")
            self.process_input(event.value)


    @on(FilteredDirectoryTree.Selected)
    def open_in_new_tab(self, selected: FilteredDirectoryTree.Selected):
        if self.tabs.active == "DefaultPane": self.tabs.remove_pane("DefaultPane")

        self._update_selection(selected.file)
        self._open_tab()
    

    @on(EditorTabs.TabActivated)
    def select_new_tab_info(self, event):
        if event.tab.id == "--content-tab-DefaultPane":
            self._update_selection(None)
        else:
            editor = self._get_current_editor()
            self._update_selection(editor.file)
            if not editor.text: self._open_file()


    def _open_tab(self) -> None:

        # Tab already exists, switch to it
        if self.tabs.query(f"#{self.selected_id}"):
            self.tabs.active = self.selected_id

        # Open in new tab
        else:

            editor = Editor.code_editor(
                language="python", 
                show_cursor=True,
                show_line_numbers=True,
                compact=True
            )
            editor.file = self.selected_file

            tab = TabPane(
                self.selected_file.name,
                editor,
                id=self.selected_id
            )

            self.tabs.add_pane(tab)
            self.tabs.active = tab.id


    def _close_tab(self) -> None:

        if self.tabs.active not in (None, "DefaultPane"):

            editor = self._get_current_editor()
            self._update_selection(editor.file)

            if editor.saved:
                self.tabs.remove_pane(self.tabs.active)

            else:
                self.notify(f"{editor.file.name} has unsaved changes")


    def _save_file(self) -> None:
        if self.tabs.active not in (None, "DefaultPane"):
            editor = self._get_current_editor()
            with open(editor.file, "w") as file:
                file.write(editor.text)
                editor.saved = True


    def _open_file(self) -> None:
        editor = self._get_current_editor()

        with open(self.selected_file, "r") as file:
            if not editor.text: 
                editor.text = file.read()


    def action_save_file(self) -> None:
        self._save_file()
        self.notify(f"{self.selected_file.name} saved")


    def action_close_tab(self) -> bool:
        self._close_tab()


    def action_run_file(self):
        self.query_one(TerminalLog).clear()
        INT.interpreter.exit_extensions()
        self.init_opal_interpreter()
        self.process_input(self._get_current_editor().text.splitlines(), fromTerminal = False)
