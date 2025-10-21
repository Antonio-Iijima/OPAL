#INCLUDE loop as loop
def loop(for_, i, in_, range_, start, stop, step, contents):
   for i in range(start, stop, step):
      EVA.evaluate(contents)


#EXCLUDE

EXTENSIONS = {name : fun for (name, fun) in locals().items() if callable(fun)}

import repl as REP
import parser as PAR
import keywords as KEY
import evaluate as EVA
import environment as ENV
import interpreter as INT
