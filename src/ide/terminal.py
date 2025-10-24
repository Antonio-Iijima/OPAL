from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Switch, Static, RichLog, Input
from textual.app import ComposeResult

import sys



class TerminalFrame(Vertical):

    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.border_title = "Terminal"


    def compose(self) -> ComposeResult:
        yield TerminalPanel(id="TerminalPanel")
        yield OptionsPanel(id="OptionsPanel", classes="secondary")



class OptionsPanel(Horizontal):

    def compose(self) -> ComposeResult:
        
        flags = [
            '-d',
            '-p',
            '-z'
        ]

        # -i flag is just for show and consistency, so hardcode it
        yield Horizontal(
            Static(" -i ", classes="label secondary"),
            Switch(disabled=True, id="-i", value=True, classes="switch primary")
        )

        for flag in flags:
            yield Horizontal(
                Static(f" {flag} ", classes="label secondary"),
                Switch(value=flag in sys.argv, animate=True, id=flag, classes="switch primary"),
            )



class TerminalPanel(Vertical):

    def compose(self) -> ComposeResult:
        yield TerminalOpt(id="TerminalOpt", classes="extendedTopPanel secondary")
        yield Terminal(id="Terminal", classes="secondary")



class TerminalOpt(Horizontal):
    pass



class Terminal(VerticalScroll):

    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, can_focus = None, can_focus_children = None, can_maximize = None):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, can_focus=can_focus, can_focus_children=can_focus_children, can_maximize=can_maximize)


    def compose(self):
        yield TerminalLog()
        yield TerminalInputRow()


    def _on_focus(self, event):
        self.query_one(TerminalInput).focus(False)
        return super()._on_focus(event)



class TerminalLog(RichLog):
    
    def __init__(self, *, max_lines = None, min_width = 78, wrap = False, highlight = False, markup = False, auto_scroll = True, name = None, id = "TerminalLog", classes = None, disabled = False):
        super().__init__(max_lines=max_lines, min_width=min_width, wrap=wrap, highlight=highlight, markup=markup, auto_scroll=auto_scroll, name=name, id=id, classes=classes, disabled=disabled)



class TerminalInputRow(Horizontal):

    def compose(self):
        yield Static("(Ω) ")
        yield TerminalInput()



class TerminalInput(Input):
    
    def __init__(
            self, 
            value = None,
            placeholder = "", 
            highlighter = None, 
            password = False, *, 
            restrict = None, 
            type = "text", 
            max_length = 0, 
            suggester = None, 
            validators = None, 
            validate_on = None, 
            valid_empty = False, 
            select_on_focus = True, 
            name = None, 
            id = "TerminalInput", 
            classes = None, 
            disabled = False, 
            tooltip = None, 
            compact = True
            ):
        
        super().__init__(
            value,
            placeholder,
            highlighter,
            password,
            restrict=restrict,
            type=type,
            max_length=max_length,
            suggester=suggester,
            validators=validators,
            validate_on=validate_on,
            valid_empty=valid_empty,
            select_on_focus=select_on_focus,
            name=name, 
            id=id,
            classes=classes,
            disabled=disabled,
            tooltip=tooltip,
            compact=compact
            )
