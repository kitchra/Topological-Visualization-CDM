import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d

"""
Input format (in file):
    A 1 2 3
    B 2 3 4
    C 3 4 5
    ...
    Connections:
    AB
    BC
    CA
    ...
    
Preconditions: 
    * The graph must be connected
    * Vertically connected vertices must be directly above/below each other
    * Vertex coordinate values can not be greater than 10
"""

in_file = open(sys.argv[1], "r")
line = in_file.readline()

# Vertex format = 123 -> (1, 2, 3)
# Take in data set of values for vertices
v_set = []
while 'Connections:' not in line:
    # Create vertices such that each vertex is an array [name, x, y, z]
    spl = line.split(' ')
    v = [spl[0], int(spl[1]), int(spl[2]), int(spl[3])]

    v_set.append(v)
    line = in_file.readline()

# Create array of horizontal relations
hv_set = [[] for _ in range(11)]
for v in v_set:
    # Horizontally related if they are on the same y-level
    level = int(v[2])
    hv_set[level].append(v)

# Create array of vertical relations
vv_set = [[[] for _ in range(11)] for _ in range(11)]
for v in v_set:
    # Vertically related if they have the same x and z
    x_loc = int(v[1])
    z_loc = int(v[3])
    vv_set[x_loc][z_loc].append(v)

# Goes to the line after 'Connections:'
line = in_file.readline()

# Create connectivity matrix initialized to all zeros
c_matrix = np.zeros((len(v_set), len(v_set)), dtype=int)
c_set = []
while line:
    # Connection is an edge
    v1_name = line[:1]
    v2_name = line[1:2]
    v1_index = -1
    v2_index = -1

    # Find each vertex in the vertex set
    for i in range(len(v_set)):
        if v_set[i][0] == v1_name:
            v1_index = i
        elif v_set[i][0] == v2_name:
            v2_index = i

    if v1_index == -1 or v2_index == -1:
        print("Vertex connection not found")
        exit(0)

    # Create local variables of the vertices
    v1 = v_set[v1_index]
    v2 = v_set[v2_index]
    c_set.append((v1, v2))

    e_len = 0
    if v1[2] == v2[2]:
        # Same y-value, so must be horizontally connected. Get distance
        e_len = int(math.sqrt(pow(v1[1] - v2[1], 2) + pow(v1[3] - v2[3], 2)))
    else:
        # Must be vertically connected
        e_len = int(abs(v1[2] - v2[2]))

    # Add to connectivity matrix with connection distance
    c_matrix[v1_index][v2_index] = e_len
    c_matrix[v2_index][v1_index] = e_len

    line = in_file.readline()

# Dijkstra's algorithm
visited = []
dists = []

print("List of vertices:")
# Set the distance to each node to "infinity"
for i in range(len(v_set)):
    dists.append(1000)
    # Print each vertex name
    print v_set[i]

# Start and end points
start = raw_input("Enter start vertex: ")
end = raw_input("Enter end vertex: ")
start_index = -1
end_index = -1

# Find start vertex and set it to 0 distance value
for i in range(len(v_set)):
    if v_set[i][0] == start:
        dists[i] = 0
        start_index = i
    elif v_set[i][0] == end:
        end_index = i

# Parent array holds parent of each node in its current shortest path
parents = [0 for _ in range(len(v_set))]
while len(visited) < len(v_set):
    min_index = -1
    curr_min = 1000
    # Find vertex with the minimum distance value from start
    for i in range(len(dists)):
        if v_set[i] not in visited and dists[i] < curr_min:
            curr_min = dists[i]
            min_index = i

    # Add the min vertex to list of visited nodes
    visited.append(v_set[min_index])

    for j in range(len(v_set)):
        # Distance value from adjacency matrix
        c_dist = c_matrix[min_index][j]
        if c_dist != 0:
            # Vertices are adjacent, check edge distance
            if dists[j] > dists[min_index] + c_dist:
                # The path from source through current node is smaller
                # than the distance value currently stored
                dists[j] = int(dists[min_index] + c_dist)
                parents[j] = int(min_index)

# Store path as an array
path = [end_index]
curr = end_index
while curr != start_index:
    print(curr)
    curr = parents[curr]
    path.append(curr)

print("Minimum path:")
for v in reversed(path):
    # Prints the name of each vertex in the path
    print v_set[v][0]


# Last step: visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot vertices
for v in v_set:
    ax.scatter(v[1], v[2], v[3])
    ax.text(v[1], v[2], v[3], v[0], size=20, zorder=1)

# Plot relations
# for lev in hv_set:
#     h_x = []
#     h_y = []
#     h_z = []
#     for h in lev:
#         h_x.append(h[1])
#         h_y.append(h[2])
#         h_z.append(h[3])
#         line = art3d.Line3D(h_x, h_y, h_z, color='gray')
#         ax.add_line(line)
# for flr in vv_set:
#     v_x = []
#     v_y = []
#     v_z = []
#     for z in flr:
#         for v in z:
#             v_x.append(v[1])
#             v_y.append(v[2])
#             v_z.append(v[3])
#             line = art3d.Line3D(v_x, v_y, v_z, color='gray')
#             ax.add_line(line)


# Plot all connections
for c in c_set:
    x_edge = [c[0][1], c[1][1]]
    y_edge = [c[0][2], c[1][2]]
    z_edge = [c[0][3], c[1][3]]
    line = art3d.Line3D(x_edge, y_edge, z_edge, color='black')
    ax.add_line(line)

# Make arrays for the edges of the path to plot
e_x = []
e_y = []
e_z = []
for i in path:
    e_x.append(v_set[i][1])
    e_y.append(v_set[i][2])
    e_z.append(v_set[i][3])
    line = art3d.Line3D(e_x, e_y, e_z, color='red')
    ax.add_line(line)

plt.show()
