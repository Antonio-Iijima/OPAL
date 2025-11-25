def show(self: object) -> None:
    print(f"Initialized {self.__class__.__name__} with the following language features:")
    info = sorted([(parent.__module__.split(".")[-2], parent.__name__) for parent in self.__class__.__bases__], key=lambda x: len(x[0]))
    offset = int(max(max(map(len, entry)) for entry in info) * 1.25)
    for (module, selection) in info:
        print(f"{module + "."*(offset-len(module))} {selection}")
