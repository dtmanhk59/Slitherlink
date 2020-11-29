import matplotlib.pyplot as plt
import networkx as nx
import itertools
from satispy import Variable, Cnf
from satispy.solver import Minisat
from Common import select, var


class SlitherLink:
  def __init__(self, table, height, width):
    self.table = table
    self.height = height
    self.width = width
    self.table_nodes = self.set_table_nodes()
    self.table_edges = self.set_table_edges()
    self.cnf = Cnf()

  def set_table_nodes(self):
    table = nx.grid_2d_graph(self.height, self.width)
    for node in table.nodes:
      row, column = node
      table.nodes[node]['value'] = self.table[row][column]
    return table

  def set_table_edges(self):
    table = nx.grid_2d_graph(self.height + 1, self.width + 1)

    for node in table.nodes():
      table.nodes[node]['var'] = var()

    for edge in table.edges():
      table.edges[edge]['var'] = var()
    return table

  def rule_one(self):
    for node in self.table_nodes.nodes():
      row, col = node
      u = self.table_edges.edges[(row, col), (row, col + 1)]['var']
      l = self.table_edges.edges[(row, col), (row + 1, col)]['var']
      d = self.table_edges.edges[(row + 1, col), (row + 1, col + 1)]['var']
      r = self.table_edges.edges[(row, col + 1), (row + 1, col + 1)]['var']
      self.cnf &= select(self.table_nodes.nodes[node]['value'], [u, l, d, r])

  def rule_two(self):
    for node in self.table_edges.nodes():
      edges = [self.table_edges.edges[node, adj]['var'] for adj in self.table_edges.adj[node]]
      self.cnf &= (select(2, edges) | select(0, edges)) 

  def rule_three(self):
    pass

  def solve(self):
    solver = Minisat('minisat %s %s')
    print("Solving...")
    solution = solver.solve(self.cnf)
    if not solution.success:
      print("not solution success")
      exit()
    print("Extracting solution...")
    for edge in self.table_edges.edges():
      try:
        self.table_edges.edges[edge]['result'] = solution[self.table_edges.edges[edge]['var']]
      except KeyError:
        self.table_edges.edges[edge]['result'] = None

  def show(self):
    pos = nx.spring_layout(self.table_edges, iterations=100)
    colors = []
    nx.draw(self.table_edges, pos, with_labels=True)
    for edge in self.table_edges.edges():
      if self.table_edges.edges[edge]['result']:
        colors.append('g')
      else:
        colors.append('w')
    nx.draw(self.table_edges, pos, node_color='k', node_size=0, edge_color=colors)
    plt.savefig("drawEdge.png")
    # plt.show()


if __name__ == "__main__":
  table = [
      [5, 2, 3, 2, 3],
      [2, 5, 5, 5, 5],
      [0, 5, 5, 1, 3],
      [2, 3, 5, 5, 5],
      [5, 5, 5, 5, 3]]
  h = 5
  w = 5
  slither_link = SlitherLink(table, h, w)
  slither_link.rule_one()
  slither_link.rule_two()
  slither_link.solve()
  slither_link.show()
