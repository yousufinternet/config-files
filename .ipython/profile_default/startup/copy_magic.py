from IPython.core.magic import register_cell_magic


@register_cell_magic("copy")
def copy_cell(line, cell):
    try:
        import pyperclip
    except ImportError:
        return "Install pyperclip first"

    pyperclip.copy(cell)
