from textual.containers import Vertical, Horizontal, Grid
from textual.widgets import TextArea, DirectoryTree
from textual.widgets import TabbedContent, TabPane
from textual.app import ComposeResult
from textual.message import Message

from typing import Iterable
from pathlib import Path

import os



class EditorFrame(Horizontal):
    
    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.border_title = "OPAL (Omni-Paradigm Programming Language)"


    def compose(self) -> ComposeResult:
        yield DirectoryPanel(id="DirectoryPanel", classes="tertiary")
        yield EditorPanel(id="EditorPanel", classes="secondary")
    


class DirectoryPanel(Vertical):

    def compose(self) ->ComposeResult:
        yield DirectoryOpt(id="DirectoryOpt", classes="extendedTopPanel secondary")
        yield FilteredDirectoryTree(id="DirectoryTree", path=os.path.abspath(__file__ + "/../../.."))



class DirectoryOpt(Horizontal):
    pass



class FilteredDirectoryTree(DirectoryTree):

    class Selected(Message):

        def __init__(self, file):
            super().__init__()
            self.file = file


    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [ path for path in paths if not path.name.startswith((".", "__")) ]
    

    def _on_directory_tree_file_selected(self, event) -> None:
        self.post_message(self.Selected(event.path))
        



class EditorPanel(Vertical):

    def compose(self) -> ComposeResult:
        with EditorTabs():
            yield TabPane(
                "New",
                Editor.code_editor(
                    id="DefaultEditor",
#                    language="python",
                    show_cursor=True,
                    show_line_numbers=True,
                    compact=True
                ),
                id="DefaultPane",
            )



class EditorTabs(TabbedContent):

    class SelectNone(Message):
        
        def __init__(self):
            super().__init__()


    def _on_tabs_cleared(self, event):
        self.add_pane(
            TabPane(
                "New",
                Editor.code_editor(
                    id="DefaultEditor",
#                    language="python",
                    show_cursor=True,
                    show_line_numbers=True,
                    compact=True
                ),
                id="DefaultPane",
            )
        ) == self.post_message(self.SelectNone())

        self.active = "DefaultPane"
        
        return super()._on_tabs_cleared(event)



class EditorOpt(Grid):
    pass



class Editor(TextArea):

    def __init__(self, text = "", *, language = None, theme = "css", soft_wrap = True, tab_behavior = "focus", read_only = False, show_cursor = True, show_line_numbers = False, line_number_start = 1, max_checkpoints = 50, name = None, id = None, classes = None, disabled = False, tooltip = None, compact = False, highlight_cursor_line = True, placeholder = ""):
        super().__init__(text, language=language, theme=theme, soft_wrap=soft_wrap, tab_behavior=tab_behavior, read_only=read_only, show_cursor=show_cursor, show_line_numbers=show_line_numbers, line_number_start=line_number_start, max_checkpoints=max_checkpoints, name=name, id=id, classes=classes, disabled=disabled, tooltip=tooltip, compact=compact, highlight_cursor_line=highlight_cursor_line, placeholder=placeholder)
        self.file = None
        self.saved = True


    def _on_key(self, event):
        self.saved = event.key == "ctrl+r"

        pairs = {
            "(" : "()",
            "{" : "{}",
            "[" : "[]",
            "'" : "''",
            '"' : "''"
        }

        if event.character in pairs:
            self.insert(pairs[event.character])
            self.move_cursor_relative(columns=-1)
            event.prevent_default()
