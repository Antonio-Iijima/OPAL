"""

## The IDE

OPAL comes with a built-in, terminal-based TUI (textual user interface) IDE. It is
implemented using the Python `Textual` and `Rich` libraries for a performant and visually
appealing UI. The IDE is quite customizable through the available CSS file, which can be 
modified live through the IDE itself (see main docs page for further information) 

Current functionality is not extensive, but will continue to be expanded. For now,
the IDE supports the following features:

- Syntax highlighting 
    - Basic, to be improved with custom parsing and highlighting for actual language keywords
- Switch-based interaction for flags
- Live CSS editing in `--ide-dev` mode
- Keybinds to close, save, and run files

"""
