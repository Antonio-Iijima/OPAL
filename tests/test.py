import os
import sys



def test(filepath: str, args: list = []) -> None:
    """Recursively test files and directories."""

    # Test files with input.txt as standard sample input
    if os.path.isfile(filepath) and filepath.endswith('.op'):
        os.system(f"echo '\nFILE: {filepath}'")
        os.system(f"coverage run --parallel-mode ../src/main.py {filepath} {" ".join(args)} < input.txt && echo")

    # Otherwise recurse into directory
    elif os.path.isdir(filepath):
        for file in sorted(os.listdir(filepath)): 
            if file not in ["htmlcov"]: test(f"{filepath}/{file}", args)


def main() -> None:
    """Run all tests with command line args."""

    # Automatically run with command line flags, removing them from sys.argv as found; else by default run with all flags if none provided
    flags = [ flag for flag in ["-i", "-d", "-p", "-z"] if (flag in sys.argv and not(sys.argv.remove(flag))) ] or ["-i", "-d", "-p", "-z"]
    
    # Set initial directory to test folder
    initialDirectory = sys.argv[1] if len(sys.argv) > 1 else "../tests"

    os.system("echo '\nRunning without flags\n'")
    test(initialDirectory)
    
    # Run tests with each flag separately
    for flag in flags:
        os.system(f"echo '\nRunning with {flag} flag\n'")
        test(initialDirectory, args = [flag])

    # Finally print results
    os.system("coverage combine && coverage report && coverage html")
    


if __name__ == "__main__": main()
