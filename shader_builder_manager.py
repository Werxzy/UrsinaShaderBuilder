from ursina import *
from node_variable import ConstantNode
from node_instruction import InstructionNode

'''
Manager file that holds all the nodes and builds the shader.
'''

class ShaderBuilderManager(Entity):

    def __init__(self, **kwargs):
        super().__init__(parent = camera.ui)
        # temp model/color

        nodes = []

        for key, value in kwargs.items():
            setattr(self, key, value)

        #test node
        nodes.append(InstructionNode(parent = self, manager = self, instruction = 'Add', position = (-0.3,0)))
        nodes.append(InstructionNode(parent = self, manager = self, instruction = 'Subtract', position = (0,0.3)))
        nodes.append(InstructionNode(parent = self, manager = self, instruction = 'Clamp', position = (0.3,0)))
        nodes.append(ConstantNode(parent = self, manager = self, data_type='vec3', position = (-0.4,-0.3)))
        nodes.append(ConstantNode(parent = self, manager = self, data_type='vec2', position = (0.4,-0.3)))
        nodes.append(InstructionNode(parent = self, manager = self, instruction = 'Power', position = (0.0,-0.3)))


    #quickly organize the nodes based on how the inputs/outputs are connected
    def organize_nodes():
        pass


    def input(self, key):
        if key == 'scroll up':
            self.scale *= 1.1
            self.position = (self.position - mouse.position) * 1.1 + mouse.position

        if key == 'scroll down':
            self.scale /= 1.1
            self.position = (self.position - mouse.position) / 1.1 + mouse.position

    def update(self):
        if mouse.right:
            self.x += mouse.velocity[0]
            self.y += mouse.velocity[1] * window.aspect_ratio


    def buildShader(self):
        return ''