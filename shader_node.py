from ursina import *
from shader_instructions import *
from color_atlas import *


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

        self.data_type_common = '' # where all inputs/outputs need to be the same type, like gentype
        self.data_type_set = -1 # nth data type in (gentype, float,)
        # these two need to be checked any time that a connection would be made or removed

        #TODO, line renderer and connecting nodes


        for key, value in kwargs.items():
            setattr(self, key, value)
        
        
        self.ui_build_width = 0.2
        self.ui_build_pos = 0 # to allow appending ui without intersection
        self.ui_spacing = 0.01

        self.ui_name = self.append_text(instruction)
        self.ui_divider1 = self.append_divider()
        self.ui_desc = self.append_text(GLSL[instruction]['description'])
        self.ui_divider2 = self.append_divider()
        self.ui_func = self.append_text(GLSL[instruction]['function'])

        self.ui_back = self.build_back()

        self.build_inputs_outputs_ui()


# - - - ui builder functions - - -

    def append_divider(self):
        return Entity(parent = self, model = 'quad', position = Vec2(0, self.ui_build_pos), scale = (0.2,0.001), color = c_node_dark)

    def append_text(self, text, text_color = c_text):
        ent = Text(text, parent = self, color = text_color)
        ent.position = Vec2(-ent.width * 0.5, self.ui_build_pos - self.ui_spacing) #adjust based on text width and starting y pos
        self.ui_build_pos -= ent.height + self.ui_spacing * 2 # add the starting y position for next element

        return ent

    def build_back(self):
        quadScale = Vec2(self.ui_build_width, -self.ui_build_pos)
        ent = Entity(parent = self, model = Quad(scale = quadScale, radius=0.02), z = 0.1, origin_y = quadScale.y * 0.5, color = c_node_back, collider='box')
        return ent

    def build_inputs_outputs_ui(self):  
        i = 0.5    
        # build inputs
        for k,v in GLSL[self.instruction]['inputs'].items():
            conn = NodeConnector(parent = self, x_disp = self.ui_build_width * 0.5, yth = i, variable = k, var_types = v, isOutput = False)
            self.inputs.append(conn)
            i += 1
        
        i = 0.5     
        # build output(s)
        for k,v in GLSL[self.instruction]['outputs'].items():
            conn = NodeConnector(parent = self, x_disp = self.ui_build_width * 0.5, yth = i, variable = k, var_types = v)
            self.inputs.append(conn)
            i += 1

# - - - - - - -

    
    def input(self, key):
        if key == 'left mouse down' and self.ui_back.hovered:
            self.dragged = True
        if key == 'left mouse up':
            self.dragged = False

    def update(self):
        if self.dragged:
            self.x += mouse.velocity[0] / self.parent.scale_x
            self.y += mouse.velocity[1] / self.parent.scale_y * window.aspect_ratio

    def on_destroy(self):
        for i in self.inputs:
            i.disconnectAll()
        for o in self.outputs:
            o.disconnectAll()
        