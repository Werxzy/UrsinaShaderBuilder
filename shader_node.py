from ursina import *
from shader_instructions import *
from color_atlas import *
from shader_node_connector import NodeConnector


'''
holds a single instruction and all inputs and puts
will be a child of shader_builder_manager
'''

class ShaderNode(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.inputs = []
        self.outputs = []
        self.dragged = False

        self.data_type_set = -1 # nth data type in [float, vec2, vec3, ...]
        # needs to be checked any time that a connection would be made or removed

        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.ui_build_width = 0.2
        self.ui_build_pos = 0 # to allow appending ui without intersection
        self.ui_spacing = 0.01


# - - - ui builder functions - - -

    def append_divider(self):
        return Entity(parent = self, model = 'quad', position = Vec2(0, self.ui_build_pos), scale = (0.2,0.001), color = c_node_dark)

    def append_text(self, text, text_color = c_text, size = 1):
        ent = Text(text, parent = self, color = text_color, scale = size)
        ent.position = Vec2(-ent.width * 0.5, self.ui_build_pos - self.ui_spacing) #adjust based on text width and starting y pos
        self.ui_build_pos -= ent.height + self.ui_spacing * 2 # add the starting y position for next element
        self.ui_build_width = max(self.ui_build_width, ent.width + self.ui_spacing)

        return ent

    def build_back(self):
        quadScale = Vec2(self.ui_build_width, -self.ui_build_pos)
        ent = Entity(parent = self, model = Quad(scale = quadScale, radius=0.02), z = 0.1, origin_y = quadScale.y * 0.5, color = c_node_back, collider='box')
        return ent

    def build_connector(self, variable, variable_type, isOutput, offset = 0):
        conn = NodeConnector(parent = self, x_disp = self.ui_build_width * 0.5, yth = offset, variable = variable, variable_type = variable_type, isOutput = isOutput)
        if isOutput:
            self.outputs.append(conn)
        else:
            self.inputs.append(conn)


# - - - - - - -

    #goes through all of the outputs and checks the data types that are possible, disconnecting any invalid connections
    def update_connections(self):
        nodes = [self]
        while len(nodes) > 0:
            if len(nodes[0].inputs) > 0:
                r = set(range(len(nodes[0].inputs[0].variable_type)))
                for i in nodes[0].inputs: # get overlaps that exist on each node (disconnect any if they suddenly don't work)
                    p_types = i.get_possible_data_types()
                    
                    data_types = set()
                    for p in p_types:
                        data_types.add(p[0])
                    r_overlap = r & data_types
                    
                    if len(r_overlap) == 0:# no matching types
                        i.disconnect_all() # should only be one anyways
                    else:
                        r = r_overlap

                if len(r) == 1: # one matching input set
                    nodes[0].data_type_set = r.pop()

                    for o in nodes[0].outputs:# propogate, since we know this node's output type
                        for c in o.connections:
                            nodes.append(c.parent)

            else: # node has only an output (should only have one usually)
                nodes[0].data_type_set = 0
                for o in nodes[0].outputs: # propogate, since we know this node's output type
                    for c in o.connections:
                        nodes.append(c.parent)

            nodes.pop(0)

    def disconnection(self, connector):
        if connector in self.inputs:
           self.data_type_set = -1
    
    def input(self, key):
        if key == 'left mouse down' and self.ui_back.hovered:
            self.dragged = True
        if key == 'left mouse up':
            self.dragged = False

    def update(self):
        if self.dragged:
            self.x += mouse.velocity[0] / self.parent.scale_x
            self.y += mouse.velocity[1] / self.parent.scale_y * window.aspect_ratio
            if mouse.velocity[0] != 0 or  mouse.velocity[1] != 0:
                for i in self.inputs:
                    i.update_line()
                for o in self.outputs:
                    o.update_line()

    def on_destroy(self):
        for i in self.inputs:
            i.disconnectAll()
        for o in self.outputs:
            o.disconnectAll()
        