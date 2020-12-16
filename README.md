# Graph Sandbox

## What?
This is a rough little graph sandbox written using python and tkinter. It includes functionality for quick creation of theoretical graphs and provides some analysis/computation on the given graphs. Check out the [How To](##How-To) section to learn how to use it! Or check out the [Features](##Features) section to learn about what all the app supports. Finally the [Structure](##structure) section gives some detail about the code structure.

## How To
* **Create a Vertex:** Left click anywhere on the canvas.
* **Create an Edge:** Left click once on an existing vertex, and again on the desired destination vertex. Double click the same vertex to add loops!
* **Move a Vertex:** Left click and hold on a vertex, you can now drag it anywhere on screen.
* **Delete a Vertex/Edge:** Right click on any vertex or edge in order to remove it. If you delete a vertex with edges, all its edges will also be deleted!
* **Toggle Directed Mode:** Hit `Shift+D` to toggle directed mode on/off. When on, the graph will display arrows indicating the direction of the edges

## Features
* **Create Vertices/Edges/Loops/Parallel Edges**
* **Vertex Labelling:** shown in the top right of a vertex in green
* **Degree Counting:** shown in the top left of a vertex in red
* **Current Graph Status Bar:** shown at the top of the screen. includes:
  *  **Vertex/Edge Counts**
  *  **Bipartite Indicator**
  *  **Component Counter**
  *  **Component List**
  *  **Bridge List**

## Structure
* `graph-sandbox.py` - The controller/driver. Run this to run the application
* `graph.py` - The model. This contains all definitions for graph representation and computation in a theoretical sense. Graphical representation is done elsewhere.
* `point.py` - Utility class for representing a point in 2D space, also includes tools for vector operations.
* `element.py` - Parent class for all graphical components of the app
  * `vertex.py` - Definition for a graphical vertex
  * `edge_group.py` - Utility class for storing edges in a vertex
  * `edge.py` - Definition for a graphical edge
  * `arrowhead` - Utility class for rendering points of arrows in directed mode
  * `label.py` - Utility class used in rendering labels above vertices. 