class Selector:
    """Base selector class for all dynamic language features."""
    
    def select(self, i: int) -> any:
        return self.options[i]

    
    def show(self) -> None:
        print(self.__class__.__name__)
        for i, opt in enumerate(self.options):
            print(f"{i} : {opt.__name__}")
