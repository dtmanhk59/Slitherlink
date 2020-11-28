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


def select(n, lst):
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


def test_select():
  v1 = Variable(str(1))
  v2 = Variable(str(2))
  v3 = Variable(str(3))
  v4 = Variable(str(4))
  vs = [v1, v2, v3, v4]
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
  test_var()
