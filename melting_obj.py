import bpy

def create_objects():
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    # Add a cube at the origin and move it 1 unit up along the Z-axis
    bpy.ops.mesh.primitive_cube_add(
        size=2,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 1)  # Directly set the location to (0, 0, 1)
    )
    cube = bpy.context.object  # Reference to the newly created cube
    
    # Add a UV sphere at the origin and move it 3 units up along the Z-axis
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1,
        enter_editmode=False,
        align='WORLD',
        location=(0, -2, 3)  # Directly set the location to (0, -2, 3)
    )
    sphere = bpy.context.object  # Reference to the newly created sphere
    
    # Apply smooth shading to the sphere
    bpy.ops.object.shade_smooth()
    
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select the cube
    cube.select_set(True)
    
    # Set the cube as the active object
    bpy.context.view_layer.objects.active = cube
    
    return cube, sphere

def add_geo_node(cube, sphere):
    # Add a Geometry Nodes modifier to the cube
    bpy.ops.node.new_geometry_nodes_modifier()
    
    # Access the active Geometry Nodes node tree
    node_tree = cube.modifiers.active.node_group

    # Ensure the node tree is valid
    if node_tree and node_tree.type == 'GEOMETRY':
        # Initialize variables to store references to the nodes
        group_input_node = None
        group_output_node = None
        subdivide_mesh_node = None
        delete_geometry_node = None
        geo_proximity_node = None
        lt_or_eq_node = None

        # Iterate through the nodes to find the Group Input and Group Output nodes
        for node in node_tree.nodes:
            if node.bl_idname == 'NodeGroupInput':
                group_input_node = node
            elif node.bl_idname == 'NodeGroupOutput':
                group_output_node = node
            elif node.bl_idname == 'GeometryNodeSubdivideMesh':
                subdivide_mesh_node = node
            elif node.bl_idname == 'GeometryNodeDeleteGeometry':
                delete_geometry_node = node
            elif node.bl_idname == 'GeometryNodeProximity':
                geo_proximity_node = node
            elif node.bl_idname == 'FunctionNodeCompare':
                lt_or_eq_node = node
                
        # If the Less Than or Equal node doesn't exist, create it
        if not lt_or_eq_node:
            lt_or_eq_node_0 = node_tree.nodes.new('FunctionNodeCompare')
            lt_or_eq_node_0.operation = 'LESS_EQUAL'
            lt_or_eq_node_0.location = (0, -175)
                
        # If the Geometry Proximity node doesn't exist, create it
        if not geo_proximity_node:
            geo_prox_0 = node_tree.nodes.new('GeometryNodeProximity')
            geo_prox_0.location = (-200, -175)

        # If the Delete Geometry node doesn't exist, create it
        if not delete_geometry_node:
            delete_geo_0 = node_tree.nodes.new('GeometryNodeDeleteGeometry')
            delete_geo_0.name = "delete_geo_0"
            delete_geo_0.label = "delete_geo_0"
            delete_geo_0.location = (50, 0)  # Position the new node for clarity
            delete_geo_0.domain = 'FACE'
            delete_geo_0.mute = True

        # If the Subdivide Mesh node doesn't exist, create it
        if not subdivide_mesh_node:
            mesh_divider_0 = node_tree.nodes.new('GeometryNodeSubdivideMesh')
            mesh_divider_0.name = "mesh_divider_0"
            mesh_divider_0.label = "mesh_divider_0"
            mesh_divider_0.location = (-150, 0)  # Position the new node for clarity
            mesh_divider_0.inputs['Level'].default_value = 5
            
        if group_input_node and group_output_node:
            # Define the additional X distance
            additional_distance = 1500  # Adjust this value as needed
            
            # Move the Group Output node further along the X-axis
            group_output_node.location.x = group_input_node.location.x + additional_distance
            print(f"Moved 'Group Output' node to X: {group_output_node.location.x}")

            # Create links between the nodes
            links = node_tree.links
            links.new(group_input_node.outputs[0], mesh_divider_0.inputs[0])
            links.new(mesh_divider_0.outputs[0], delete_geo_0.inputs[0])
            links.new(delete_geo_0.outputs[0], group_output_node.inputs[0])
            
            object_info_node = node_tree.nodes.new('GeometryNodeObjectInfo')
            object_info_node.location = (-400, -175)  # Position the Object Info node
            
            links.new(object_info_node.outputs['Geometry'],geo_prox_0.inputs['Target'])
            links.new(geo_prox_0.outputs['Distance'], lt_or_eq_node_0.inputs['A'])
            lt_or_eq_node_0.inputs['B'].default_value = 1
            
            # Set the sphere as the object in the Object Info node
            object_info_node.inputs['Object'].default_value = sphere

            # Set the transform space to 'RELATIVE'
            object_info_node.transform_space = 'RELATIVE'

            print(f"Added Object Info node for sphere: {sphere.name}")
        else:
            print("Could not find 'Group Input' or 'Group Output' nodes.")
    else:
        print("Active object does not have a valid Geometry Nodes modifier.")
        
def get_node_info():
    # Access the active Geometry Nodes node tree
    node_tree = bpy.context.object.modifiers.active.node_group

    if node_tree and node_tree.type == 'GEOMETRY':
        nodes = node_tree.nodes
        print("Node Indices and Names:")
        for i, node in enumerate(nodes):
            print(f"Index {i}: {node.name} (Type: {node.type})")
    else:
        print("No active Geometry Nodes modifier found.")
        
def deselect_all_nodes():
    # Access the active Geometry Nodes node tree
    node_tree = bpy.context.object.modifiers.active.node_group

    # Ensure the node tree exists
    if node_tree and node_tree.type == 'GEOMETRY':
        for node in node_tree.nodes:
            node.select = False  # Deselect each node
        print("Deselected all nodes in the Geometry Nodes setup.")
    else:
        print("No active Geometry Nodes node tree found.")


def melt():
    cube, sphere = create_objects()
    add_geo_node(cube, sphere)
    deselect_all_nodes()

melt()
