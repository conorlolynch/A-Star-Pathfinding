# A-Star-Pathfinding
Project visualizing the A* Search Algorithm finding the shortest path between two points.

## Getting Started

To get started just run the pathfinder.py file. From there place a start point, an end point and a number of obstacle walls and watch the A* Search Algorithm find the shortest path between the start node and end node given the numerous obstacle walls placed.

### Prerequisites

Following modules are required to run this program:

```
pygame==1.9.6
numpy==1.18.4
```

## Keybinds

S - Enables the start point to be placed with left click
E - Enables the end point to be placed with left click
W - Enables walls to be placed with left click (hold to drag wall over distance)
C - Clear screen
F - Run A* Algorithm and visualize progress

Left Click - Place wall/node at mouse location
Right Click - Remove wall/node at mouse location

## Usage and Explanation

For the algorithm to run a start node and end node must be placed on the grid. There is the option to place obstacles between these nodes so that the algorithm has to search further to find the shortest path.

The Algorithm knows the locations of both the start and end point on the grid. It starts off at the start point and looks at all neighbouring nodes and measures that nodes distance to the end node and the cost it would be to move to this node. Each time the algorithm moves on to the node with the lowest combination of these two factors. Through a series of iterations the algorithm will have made progress towards the end node and in the process have kept track of the path that took it there.

* One design decision I made with this version was not enabling the algorithm to move diagonally. Therefore the algorithm will find solutions that are only straight lines.

### Demonstration

TO BE ADDED

### Additional Information

- Algorithm can only travel in straight lines, diagonal directions of travel are ignored.

### Desired Features
- Make GUI prettier.
