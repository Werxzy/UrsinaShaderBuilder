from ursina import *
from shader_instructions import *
from ExtraData.color_atlas import *
from shader_node import ShaderNode

'''
Node that usually holds a glsl function or instruction.
'''

class InstructionNode(ShaderNode):
    def __init__(self, instruction, **kwargs):
        super().__init__(**kwargs)

        self.instruction = instruction
        
        self.append_text(instruction)
        self.append_divider()
        self.append_text(GLSL[instruction]['description'], size=0.7)
        self.append_divider()
        self.append_text(GLSL[instruction]['function'], size=0.7)

        self.build_back()

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

    def build_shader(self):
        var_replace = dict()
        for i in self.inputs:
            var_replace[i.variable] = i.get_build_variable()

        for o in self.outputs:
            v = o.prepare_build_variable()
            var_replace[o.variable] = v

        inst = multireplace(GLSL[self.instruction]['function'], var_replace)
        self.manager.build_shader_append('main', inst)


    def save(self):
        return {'instruction' : self.instruction}

    def load(manager, data):
        return InstructionNode(parent = manager, manager = manager, instruction = data['instruction'])