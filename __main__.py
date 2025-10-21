from rich import print

import shutil
import pdoc
import sys
import os



def build(path: str = "OPAL/docs") -> None:
    """Build the documentation for OPAL."""
    
    sys.path.append(os.path.abspath(f"{__file__}/..")) 
    sys.path.append(os.path.abspath(f"{__file__}/../src")) 
    sys.path.append(os.path.abspath(f"{__file__}/../src/ide")) 
    sys.path.append(os.path.abspath(f"{__file__}/../src/lang")) 

    modules = ['lang', 'ide']  # Public submodules are auto-imported
    context = pdoc.Context()

    modules = [pdoc.Module(mod, context=context)
            for mod in modules]

    pdoc.link_inheritance(context)

    def recursive_htmls(mod: pdoc.Module):
        yield mod.name, mod.html()
        for submod in mod.submodules():
            yield from recursive_htmls(submod)

    os.path.isdir(path) and shutil.rmtree(path)
    os.mkdir(path)

    for mod in modules:
        for module_name, html in recursive_htmls(mod):
            with open(f"{path}/{".".join(module_name.split(".")[-2:])}.html", "x") as file:
                file.write(html)



if len(sys.argv) > 1:
    if "build-docs" in sys.argv:
        build()
    elif "ide" in sys.argv:
        os.system(f"python3 {os.path.abspath(f"{__file__}/../src/ide/app.py")}")
    else:
        os.system(f"python3 {os.path.abspath(f"{__file__}/../src/lang/main.py")} {" ".join(sys.argv[1:])}")

else: print("""
Command-line args:
    Interpreter : python3 main.py lang (<flags>)
    IDE         : python3 main.py ide
""")
