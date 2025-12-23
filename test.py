from src.core.opal import opal


print(opal)


tests = [
    "(+ 1 2)",
    "a",
    "(+ 1 (+ 3 4))",
    "((1 2) 3 (4 5))"
]


for test in tests:
    # print(test, "=>", end=' ')
    # print(OPAL.call("parse expr in", test), "=>", end=' ')
    # print(OPAL.call("parse expr out", OPAL.call("parse expr in", test)), "=>", end=' ')
    print(opal.parse_out(opal.parse_in(test)) == test)
