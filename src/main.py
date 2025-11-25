from src.core.opal import OPAL



if __name__ == "__main__":
    print(OPAL.__class__.__name__)
    while 1:
        print(OPAL.process(input("> ")))
