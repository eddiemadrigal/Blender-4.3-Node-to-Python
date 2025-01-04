# Blender 4.3 Node to Python: Melting Object Script

This repository contains a Python script for Blender 4.3 that demonstrates how to create, manipulate, and connect Geometry Nodes through Python. The script generates a "melting" effect using a cube and a sphere, showcasing the power of Blender's scripting API for procedural workflows.

## Features

- **Object Creation**: Automatically creates a cube and a sphere, positions them in the scene, and applies smooth shading to the sphere.
- **Geometry Nodes Manipulation**:
  - Adds a Geometry Nodes modifier to the cube.
  - Creates and configures various nodes, including:
    - Subdivide Mesh
    - Delete Geometry
    - Geometry Proximity
    - Less Than or Equal Comparison
    - Object Info
  - Links nodes together programmatically to form a Geometry Nodes setup.
- **Node Management Utilities**:
  - List and print all nodes in the active Geometry Nodes tree.
  - Deselect all nodes for better organization.
- **Dynamic Linking**: Links nodes in the Geometry Nodes tree to achieve the desired melting effect.

## How It Works

1. **Object Creation**:
   - A cube is created at `(0, 0, 1)`.
   - A sphere is created at `(0, -2, 3)` and smooth shading is applied.

2. **Geometry Nodes Setup**:
   - A Geometry Nodes modifier is added to the cube.
   - Various nodes are added to the node tree and connected:
     - The sphere serves as the target for a Geometry Proximity node.
     - The proximity distance is compared using a Less Than or Equal node to control the effect.

3. **Utilities**:
   - Easily inspect the node setup and organize it programmatically.

4. **Execution**:
   - The `melt()` function brings everything together:
     - Objects are created.
     - Geometry Nodes are set up.
     - Nodes are deselected for a clean layout.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/eddiemadrigal/Blender-4.3-Node-to-Python.git
   cd Blender-4.3-Node-to-Python
