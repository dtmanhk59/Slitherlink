from satispy import Variable, Cnf
import itertools


class VarCreator:
  id = 0

  @staticmethod
  def create():
    VarCreator.id = VarCreator.id + 1
    return Variable(str(VarCreator.id))


def var():
  return VarCreator.create()


def select(n : int, lst: list):
  c = Cnf()
  for cs in itertools.combinations(lst, n + 1):
    e = Cnf()
    for x in cs:
      e |= -x
    c &= e
  
  for cs in itertools.combinations(lst, len(lst) - n + 1):
    e = Cnf()
    for x in cs:
      e |= x
    c &= e
  return c


def add_one(number : Variable, result: Variable, pre_remember : Variable, remember: Variable) -> Cnf:
  cnf = Cnf()
  if pre_remember is None:
    cnf &= select(1, [number, result])
    cnf &= select(1, [number, -remember])
  else:
    cnf &= (select(1, [number, result, pre_remember])| select(3, [number, result, pre_remember]))
    pass
  return cnf

def add_one(number : list, result : list, remember : list, length : int):
  cnf = Cnf()
  for i in range(0, length):
    cnf &= add_one(number[i], result[i], remember[i])
  pass


def test_select():
  v1 = Variable(str(1))
  v2 = Variable(str(2))
  vs = [v1, v2]
  vx = select(1, vs)
  print(vx)
  pass


def test_var():
  v1 = var()
  v2 = var()
  v3 = var()
  print(v1, v2, v3)
  pass


if __name__ == "__main__":
  #test_select()
  n = var()
  r = var()
  re = var()
  add_one(n, r, re)