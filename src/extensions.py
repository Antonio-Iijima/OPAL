#INCLUDE loop as loop
def loop(for_, i, in_, range_, start, stop, step, contents):
   for i in range(start, stop, step):
      ev.evaluate(contents)


#EXCLUDE

EXTENSIONS = {name : fun for (name, fun) in locals().items() if callable(fun)}

import repl as rpl
import config as cf
import parser as prs
import keywords as kw
import evaluate as ev
import environment as env
import interpreter as intrp
