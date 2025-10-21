from rich import print

import shutil
import sys
import os



PATH = os.path.abspath(f"{__file__}/..")

if len(sys.argv) > 1:
    if "build-docs" in sys.argv:
        shutil.rmtree(f"{PATH}/docs")
        os.system(f"pdoc3 --html --force --output-dir {PATH}/docs/ {PATH}/src")
        os.system(f"mv {PATH}/docs/src/* {PATH}/docs/")
        shutil.rmtree(f"{PATH}/docs/src")

    elif "ide" in sys.argv:
        os.system(f"python3 {PATH}/../src/ide/app.py")
    else:
        os.system(f"python3 {PATH}/../src/lang/main.py {" ".join(sys.argv[1:])}")

else: print("""
Command-line args:
    Interpreter : python3 main.py lang (<flags>)
    IDE         : python3 main.py ide
""")
