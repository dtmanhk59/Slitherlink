import matplotlib.pyplot as plt
import networkx as nx
import itertools
from satispy import Variable, Cnf
from satispy.solver import Minisat
from Common import select


class Id:
  i = 0
  def 

class SlitherLink:
  def __init__(self, table, height, width):
    self.table = table
    self.height = height
    self.width = width

  def set_table_nodes(self):
    nx_table = nx.grid_2d_graph(self.height, self.width)
    for node in nx_table.nodes:
      row, column = node
      nx_table.nodes[node]['value'] = self.table[row][column]
    self.table_nodes = nx_table

  def set_id(self):
     Variable(str(id))
    pass

    lass MyClass:
...     i = 3

  def set_table_edges(self):
    nx_table nx.grid_2d_graph(self.height + 1, self.width + 1)

    pass


# input data of slitherlink
# Duong Manh
# 11/11/2017
Table = [
    [5, 2, 3, 2, 3],
    [2, 5, 5, 5, 5],
    [0, 5, 5, 1, 3],
    [2, 3, 5, 5, 5],
    [5, 5, 5, 5, 3]]
H = 5
W = 5

# Make grid
# g is grid of edge
# t is grid of cell
# Duong Manh
# 11/11/2017
g = nx.grid_2d_graph(H + 1, W + 1)
t = nx.grid_2d_graph(H, W)

# set value for all node in table
# Duong Manh
# 11/11/2017
for node in t.nodes:
    t.nodes[node]['value'] = Table[node[0]][node[1]]

# Contructor exp and id to solver by minisat
# Duong Manh
# 11/11/2017
exp = Cnf()
id = 0

# Creating variables...
# Duong Manh
# 11/11/2017

# create variable for all node in edge
# Duong Manh
# 11/11/2017
for node in g.nodes():
    id = id + 1
    g.nodes[node]['variable'] = Variable(str(id))

# create variable for all node in edge
# Duong Manh
# 11/11/2017
for edge in g.edges():
    id = id + 1
    g.edges[edge]['variable'] = Variable(str(id))


# create variable for all edge in table
# Duong Manh
# 11/11/2017
for edge in t.edges():
    id = id + 1
    t.edges[edge]['variable'] = Variable(str(id))
    id = id + 1
    t.edges[edge]['variable1'] = Variable(str(id))

# create variable for all node in table
# Duong Manh
# 11/11/2017
for node in t.nodes():
    id = id + 1
    t.nodes[node]['variable'] = Variable(str(id))
    id = id + 1
    t.nodes[node]['exit'] = Variable(str(id))

for y, x in t.nodes():
    up     = g.edges[(y, x), (y, x + 1)]['variable']
    left   = g.edges[(y, x), (y + 1, x)]['variable']
    down   = g.edges[(y + 1, x), (y + 1, x + 1)]['variable']
    right  = g.edges[(y, x + 1), (y + 1, x + 1)]['variable']
    edges  = [up, left, down, right]
    exp &= select(Table[y][x], edges)

for node in g.nodes():
    adje = [g.edges[node, adjn]['variable'] for adjn in g.adj[node]]
    exp &= select(2, adje)

for node1, node2 in g.edges():
    # data = [edge merge, cell, cell]
    # data = [edge merge, cell]
    data = []
    # add edge merge
    data.append(g.edges[node1, node2]['variable'])
    # index cell
    index = [node1, (node1[0] + node1[1] - node2[1], node1[1] + node1[0] - node2[0])]
    # add cell
    for i in index:
        try:
            data.append(t.nodes[i]['variable'])
        except KeyError:
            pass
    if len(data) == 3:
        c = Cnf()
        for edge in data:
            c |= - edge
        exp &= c
        for edge in data:
            c = Cnf()
            for edge1 in [e for e in data if e != edge]:
                c |= edge1
            exp &= - edge | c
    elif len(data) == 2:
        for edge in data:
            c = Cnf()
            for edge1 in [e for e in data if e != edge]:
                c |= edge1
            exp &= - edge | c
    else:
        assert 'Not format data [merge, cell, cell] or [merge, cell]'

# One node in table is node exit
# Duong Manh
# 11/11/2017
c = Cnf()
for node in t.nodes():
    c |= t.nodes[node]['exit']
exp &= c
c = Cnf()
for com in itertools.combinations(t.nodes, 2):
    for node in com:
        c |= - t.nodes[node]['exit']
exp &= c
for node in t.nodes():
    exp &= - t.nodes[node]['exit'] | t.nodes[node]['variable']

# Duong Manh
# 12/11/2017
for edge in t.edges():
    # - t.edges[edge]['variable'] || - t.edges[edge]['variable']
    exp &= - t.edges[edge]['variable'] | - t.edges[edge]['variable1']
    exp &= t.edges[edge]['variable'] | t.edges[edge]['variable1']


for node in t.nodes():
    adjNode = t.adj[node]
    for i in range(2,5):
        print(i)
        listNodeTrue = itertools.combinations(adjNode, i)
        for com in listNodeTrue:
            c1 = Cnf()
            #c3 = Cnf()
            for node1 in com:
                c1 |= - t.nodes[node1]['variable']
                #c3 |= - t.nodes[node1]['variable1']
            for node2 in adjNode:
                if node2 not in com:
                    c1 |= t.nodes[node2]['variable']
                    #c3 |= t.nodes[node2]['variable1']
            c4 = Cnf()
            c2 = Cnf()
            for node3 in com:
                c2 |= - t.edges[node, node3]['variable']
                c4 |= - t.edges[node, node3]['variable1']
                for node4 in com:
                    if node4 != node3:
                        c2 |= t.edges[node, node3]['variable1']
                        c4 |= t.edges[node, node3]['variable']

            exp &= - t.nodes[node]['variable'] | c1 | c2
            exp &= - t.nodes[node]['variable'] | c1 | c4





# slover by minisat
# Duong Manh
# 11/11/2017
solver = Minisat('minisat %s %s')
print("Solving...")
solution = solver.solve(exp)
if not solution.success:
    print("not solution success")
    exit()
print("Extracting solution...")





# extracting solution g.edges
# Duong Manh
# 11/11/2017
for e in g.edges():
    try:
        g.edges[e]['solution'] = solution[g.edges[e]['variable']]
    except KeyError:
        g.edges[e]['solution'] = None


# draw
# Duong Manh
# 11/11/2017
pos = nx.spring_layout(g, iterations=100)

colors = []
nx.draw(g, pos, with_labels=True)
for e in g.edges():
    if g.edges[e]['solution']:
        colors.append('g')
    else:
        colors.append('w')
nx.draw(g, pos, node_color='k', node_size=0, edge_color=colors)

plt.savefig("imgs/drawEdge.png")
plt.show()


# draw
# Duong Manh
# 11/11/2017
for e in t.nodes():
    try:
        t.nodes[e]['solution'] = solution[t.nodes[e]['variable']]
    except KeyError:
        t.nodes[e]['solution'] = None

colors = []
for e in t.nodes:
    try:
        t.nodes[e]['solutionExit'] = solution[t.nodes[e]['exit']]
        if solution[t.nodes[e]['exit']]:
            colors.append('r')
        else:
            if t.nodes[e]['solution'] == True:
                colors.append('b')
            else:
                colors.append('w')
    except KeyError:
        t.node[e]['solutionExit'] = None
        colors.append('g')

nx.draw(t, pos, node_color='k')
node_labels = {}
for i in t.nodes():
    if t.nodes[i]['solution']:
        node_labels[i] = [t.nodes[i]['value'], i]


for e in t.edges():
    try:
        t.edges[e]['solution'] = solution[t.edges[e]['variable']]
    except KeyError:
        t.edges[e]['solution'] = None
colors1 = []

for e in t.edges():
    if t.edges[e]['solution'] != None:
        if t.edges[e]['solution']:
            colors1.append('g')
        else:
            colors1.append('r')
    else:
        colors1.append('b')

nx.draw(t, pos, labels=node_labels, node_color=colors, edge_color=colors1)
plt.savefig("imgs/solutionTable.png")
plt.show()

for e in t.edges():
    try:
        t.edges[e]['solution'] = solution[t.edges[e]['variable1']]
    except KeyError:
        t.edges[e]['solution'] = None
colors1 = []

for e in t.edges():
    if t.edges[e]['solution'] != None:
        if t.edges[e]['solution']:
            colors1.append('g')
        else:
            colors1.append('r')
    else:
        colors1.append('b')

nx.draw(t, pos, labels=node_labels, node_color=colors, edge_color=colors1)
plt.savefig("imgs/solutionTable1.png")
plt.show()