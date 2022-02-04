from ursina import *
from shader_instructions import *
from color_atlas import *
from shader_node import ShaderNode

'''
Node that usually holds a glsl function or instruction
'''

class InstructionNode(ShaderNode):
    def __init__(self, instruction, **kwargs):
        super().__init__(**kwargs)

        self.instruction = instruction
        
        self.ui_name = self.append_text(instruction)
        self.ui_divider1 = self.append_divider()
        self.ui_desc = self.append_text(GLSL[instruction]['description'], size=0.7)
        self.ui_divider2 = self.append_divider()
        self.ui_func = self.append_text(GLSL[instruction]['function'], size=0.7)

        self.ui_divider1.scale_x = self.ui_build_width
        self.ui_divider2.scale_x = self.ui_build_width

        self.ui_back = self.build_back()

        i = 0.5
        # build inputs
        for k,v in GLSL[self.instruction]['inputs'].items():
            self.build_connector(k, v, False, i)
            i += 1
        
        i = 0.5     
        # build output(s)
        for k,v in GLSL[self.instruction]['outputs'].items():
            self.build_connector(k, v, True, i)
            i += 1  

