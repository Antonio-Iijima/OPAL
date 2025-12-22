def info(self) -> None:
    features = sorted([(parent.__module__.split(".")[-2], parent.__name__) for parent in self.__class__.__bases__], key=lambda x: len(x[0]))
    offset = int(max(max(map(len, entry)) for entry in features) * 1.25)

    print(f"OPAL is a Parameterized Adaptive Language")
    for (module, selection) in features:
        print(f"{module[0].upper()}{module[1:]} {"."*(offset-len(module))} {selection}")
    print(f"Version {self.VERSION}")


def get_methods(self) -> list:
    return [method for method in self.__dir__() if not method.startswith("__")]


def call(self, event: str, *args, **kwargs) -> any:
    return self.__getattribute__(f"event_{event.lower().replace(" ", "_")}")(*args, **kwargs)


def __repr__(self) -> str:
    return f"OPAL version {self.VERSION}"
