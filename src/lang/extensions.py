#INCLUDE loop as loop
def loop(for_, i, in_, range_, start, stop, step, contents):
   for i in range(start, stop, step):
      EVA.evaluate(contents)


#EXCLUDE

EXTENSIONS = {name : fun for (name, fun) in locals().items() if callable(fun)}

from src.lang  import interpreter as INT
from src.lang import environment as ENV
from src.lang import evaluate as EVA
from src.lang import keywords as KEY
from src.lang import parser as PAR
from src.lang import repl as REP
