from satispy import Variable, Cnf
import itertools


class VarCreator:
  id = 0

  @staticmethod
  def create():
    VarCreator.id = VarCreator.id + 1
    return Variable(str(VarCreator.id))


class MinisatSolver:
  @staticmethod
  def solve(cnf):
    solver = Minisat('minisat %s %s')
    solution = solver.solve(cnf)
    if not solution.success:
      print("not solution success")
      exit()
    print("Extracting solution...")
    return solution


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


def _add_one(number : Variable, result: Variable, pre_remember : Variable, remember: Variable) -> Cnf:
  cnf = Cnf()
  if pre_remember is None:
    # a[0] <=> -b[0]
    cnf &= select(1, [number, result])
    # c[0] <=> b[0]
    cnf &= select(1, [number, -remember])
  else:
    # c[i] <=> b[i] ^ c[i-1]
    cnf &= (-remember | number) & (-remember | pre_remember) & (-remember | -number | -pre_remember)
    # a[i] <=> b[i] + c[i-1]
    cnf &= (select(0, [number, result, pre_remember]) | select(2, [number, result, pre_remember]))
  return cnf


def add_one(number : list, result : list, remember : list, length : int):
  cnf = Cnf()
  cnf &= _add_one(number[0], result[0], None, remember[0])
  for i in range(1, length):
    cnf &= _add_one(number[i], result[i], remember[i-1], remember[i])
  return cnf


def test_add_one():
  number = [var(), var()]
  result = [var(), var()]
  remember = [var(), var()]
  cnf = add_one(number, result, remember, 2)
  print(cnf)

def test_select():
  v1 = Variable(str(1))
  v2 = Variable(str(2))
  v3 = Variable(str(3))
  vs = [v1, v2, v3]
  cnf = select(2, vs) | select(0, vs)
  print(cnf)
  pass


def test_var():
  v1 = var()
  v2 = var()
  v3 = var()
  print(v1, v2, v3)
  pass


if __name__ == "__main__":
  # test_select()
  test_add_one()