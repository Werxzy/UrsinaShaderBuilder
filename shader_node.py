from ursina import *
from shader_instructions import *
from color_atlas import *
from shader_node_connector import NodeConnector


'''
holds a single instruction and all inputs and puts
will be a child of shader_builder_manager
'''

class ShaderNode(Entity):
    def __init__(self, instruction, **kwargs):
        super().__init__()

        self.instruction = instruction
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

        self.ui_name = self.append_text(instruction)
        self.ui_divider1 = self.append_divider()
        self.ui_desc = self.append_text(GLSL[instruction]['description'], size=0.7)
        self.ui_divider2 = self.append_divider()
        self.ui_func = self.append_text(GLSL[instruction]['function'], size=0.7)

        self.ui_divider1.scale_x = self.ui_build_width
        self.ui_divider2.scale_x = self.ui_build_width

        self.ui_back = self.build_back()

        self.build_inputs_outputs_ui()


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

    def build_inputs_outputs_ui(self):  
        i = 0.5    
        # build inputs
        for k,v in GLSL[self.instruction]['inputs'].items():
            conn = NodeConnector(parent = self, x_disp = self.ui_build_width * 0.5, yth = i, variable = k, variable_type = v, isOutput = False)
            self.inputs.append(conn)
            i += 1
        
        i = 0.5     
        # build output(s)
        for k,v in GLSL[self.instruction]['outputs'].items():
            conn = NodeConnector(parent = self, x_disp = self.ui_build_width * 0.5, yth = i, variable = k, variable_type = v)
            self.outputs.append(conn)
            i += 1

# - - - - - - -

    #goes through all of the outputs and checks the data types that are possible, disconnecting any invalid connections
    def update_connections(self):
        nodes = [self]
        while len(nodes) > 0:
            if len(nodes[0].inputs) > 0:
                r = set(range(len(nodes[0].inputs[0].variable_type)))
                for i in nodes[0].inputs:
                    p_types = i.get_possible_data_types()
                    
                    data_types = set()
                    for p in p_types:
                        data_types.add(p[0])
                    r_overlap = r & data_types
                    
                    if len(r_overlap) == 0:
                        i.disconnect_all() #should only be one anyways
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
        