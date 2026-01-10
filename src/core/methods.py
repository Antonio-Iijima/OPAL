def info(self) -> None:
    offset = int(len(max(self.FEATURES.keys(), key=len)) * 1.25)

    print(f"OPAL is a Parameterized Adaptive Language")
    for feature, (idx, selection) in self.FEATURES.items():
        print(f"{feature[0].upper()}{feature[1:]} {"."*(offset-len(feature))} | {idx} | {selection}")
    print(f"Version {self.VERSION}")


def get_methods(self) -> list:
    return [method for method in self.__dir__() if not method.startswith("__")]


def call(self, event: str, *args, **kwargs) -> any:
    return self.__getattribute__(f"event_{event.lower().replace(" ", "_")}")(*args, **kwargs)


def __repr__(self) -> str:
    return f"OPAL {self.VERSION}"
