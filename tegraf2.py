import networkx as nx
import matplotlib.pyplot as plt
import itertools

class TreeNode:
    _ids = itertools.count()

    def __init__(self, value):
        self.id = next(TreeNode._ids)
        self.value = value
        self.children = []

def build_tree(parent, arr, start):
    for i in range(start, len(arr)):
        if parent.value is None or arr[i] > parent.value:
            child = TreeNode(arr[i])
            parent.children.append(child)
            build_tree(child, arr, i + 1)

def subtree_size(node):
    if not node.children:
        return 1
    return sum(subtree_size(c) for c in node.children)

def longest_path(node, path):
    if not node.children:
        return path
    best = []
    for c in node.children:
        cand = longest_path(c, path + [c])
        if len(cand) > len(best):
            best = cand
    return best

UNIT = 3.0
VERT_GAP = 1.8 

def layout_tree(G, node, x, y, depth, pos, labels, depths):
    pos[node.id] = (x, y)
    labels[node.id] = "START" if node.value is None else str(node.value)
    depths[node.id] = depth

    if not node.children:
        return

    total_width = subtree_size(node) * UNIT
    cur_x = x - total_width / 2

    for c in node.children:
        w = subtree_size(c) * UNIT
        cx = cur_x + w / 2
        cy = y - VERT_GAP

        G.add_edge(node.id, c.id)
        layout_tree(G, c, cx, cy, depth + 1, pos, labels, depths)
        cur_x += w


data = [4, 1, 13, 7, 0, 2, 8, 11, 3]

root = TreeNode(None)
build_tree(root, data, 0)

G = nx.DiGraph()
pos, labels, depths = {}, {}, {}

layout_tree(G, root, 0, 0, 0, pos, labels, depths)

lis_nodes = longest_path(root, [root])
lis_ids = {n.id for n in lis_nodes}

node_colors, node_sizes = [], []
for n in G.nodes():
    if n in lis_ids:
        node_colors.append("red")
        node_sizes.append(1500)
    elif depths[n] == 0:
        node_colors.append("lightblue")
        node_sizes.append(1400)
    elif depths[n] == 1:
        node_colors.append("lightblue")
        node_sizes.append(1200)
    else:
        node_colors.append("lightblue")
        node_sizes.append(600)

edge_colors, edge_widths = [], []
for u, v in G.edges():
    if u in lis_ids and v in lis_ids:
        edge_colors.append("red")
        edge_widths.append(3)
    else:
        edge_colors.append("black")
        edge_widths.append(1)

plt.figure(figsize=(28, 15))
nx.draw(
    G,
    pos,
    labels=labels,
    node_color=node_colors,
    node_size=node_sizes,
    edge_color=edge_colors,
    width=edge_widths,
    font_size=9,
    arrows=False
)
plt.title("Largest Monotonically Increasing Subsequence Tree")
plt.axis("off")
plt.show()

lis_values = [n.value for n in lis_nodes if n.value is not None]
print("Longest Increasing Subsequence:")
print("START → " + " → ".join(map(str, lis_values)))
print("Panjang LIS =", len(lis_values))
