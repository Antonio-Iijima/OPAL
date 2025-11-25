from src.core.opal import build


#OPAL = build(0, 0, 0, 0, 0)
OPAL = build(*[0]*5)
OPAL.show()
print()
print(type(OPAL))
