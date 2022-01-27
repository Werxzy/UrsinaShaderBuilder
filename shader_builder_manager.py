from ursina import *
from shader_node import ShaderNode
from shader_node import CurveRenderer

'''
manager file that holds all the nodes and builds the shader
'''

class ShaderBuilderManager(Entity):

    def __init__(self, **kwargs):
        super().__init__(parent = camera.ui)
        # temp model/color

        nodes = []

        for key, value in kwargs.items():
            setattr(self, key, value)

        #test node
        nodes.append(ShaderNode(parent = self, instruction = 'Add'))

        # line = CurveRenderer(0.005, 40, parent = self)
        # line.set_curve([Vec3(0,0,0), Vec3(0.1,0,0), Vec3(0.1,0,0), Vec3(0.1,1,0), Vec3(0.1,1,0), Vec3(0.2,1,0)])
        # line.set_curve([Vec3(0,0,0), Vec3(1,0,0), Vec3(1,1,0), Vec3(2,1,0)])


    #quickly organize the nodes based on how the inputs/outputs are connected
    def organize_nodes():
        pass


    def input(self, key):
        #TODO displace based on cursor position
        if key == 'scroll up':
            self.scale *= 1.1

        if key == 'scroll down':
            self.scale /= 1.1
        pass

    def update(self):
        if mouse.right:
            self.x += mouse.velocity[0]
            self.y += mouse.velocity[1] * window.aspect_ratio


    def buildShader(self):
        return ''