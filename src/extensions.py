#INCLUDE loop as loop
def loop(for_, i, in_, range_, start, stop, step, contents):
   from evaluate import evaluate
   for i in range(start, stop, step):
      evaluate(contents)


#EXCLUDE
EXTENSIONS = {name : fun for (name, fun) in locals().items() if callable(fun)}
