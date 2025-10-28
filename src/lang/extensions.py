from src.lang import interpreter as INT
from src.lang import environment as ENV
from src.lang import evaluate as EVA
from src.lang import keywords as KEY
from src.lang import parser as PAR
from src.lang import repl as REP



#INCLUDE factorial as !
def factorial(n):
   n = EVA.evaluate(n)
   return 1 if n <= 1 else n * factorial(n-1)



#INCLUDE ternary as ?
def ternary(ifthis, thenthis, elsethis):
   return EVA.evaluate(thenthis if EVA.evaluate(ifthis) else elsethis)



def loop(i, contents):
   for _ in range(i):
      EVA.evaluate(contents)
