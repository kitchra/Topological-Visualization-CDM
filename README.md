# Topological-Visualization-CDM
Visualization tool for shortest path between two nodes in a 3D graph.

Based on the combinatorial data model for visualization the internal topology of buildings, where vertices represent rooms, and edges represent the connections between rooms (hallways, stairwells, etc.)

Current working model supports the following:
* Takes in a set of vertices and edges as parameters
* Prompts the user for start vertex and end vertex
* Calculates the shortest path between the start and end vertices
* Displays the shortest path on a graph in red, with other connections displayed in black.

Example:
Given the input in `input.txt`, the following graph will be plotted.
![Sample Graph from Input](input_sample.PNG)
