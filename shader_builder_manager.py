from ursina import *
from node_variable import ConstantNode
from node_builtin_output import BuiltInOutputNode
from node_instruction import InstructionNode
from search_menu import SearchMenu
from shader_instructions import GLSL
from color_atlas import *

'''
Manager file that holds all the nodes and builds the shader.
'''

class ShaderBuilderManager(Entity):

    menu_options = {
        'Constant' : dict([(v,'ConstantNode,'+v) for v in ConstantNode.data_type_layouts]),
        'Instruction' : dict([(v,'InstructionNode,'+v) for v in GLSL])
    }

    def __init__(self, **kwargs):
        super().__init__(parent = camera.ui)
        # temp model/color

        self.shader_nodes = list()

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.create_menu = False
        self.search_menu = None

        #test node
        self.shader_nodes.append(InstructionNode(parent = self, manager = self, instruction = 'Add', position = (-0.3,0)))
        self.shader_nodes.append(InstructionNode(parent = self, manager = self, instruction = 'Subtract', position = (0,0.3)))
        self.shader_nodes.append(InstructionNode(parent = self, manager = self, instruction = 'Clamp', position = (0.3,0)))
        self.shader_nodes.append(ConstantNode(parent = self, manager = self, data_type='vec4', position = (-0.6,-0.3)))
        self.shader_nodes.append(ConstantNode(parent = self, manager = self, data_type='vec3', position = (-0.3,-0.3)))
        self.shader_nodes.append(ConstantNode(parent = self, manager = self, data_type='vec2', position = (0.0,-0.3)))
        self.shader_nodes.append(BuiltInOutputNode(parent = self, manager = self, position = (0.4,-0.3)))


    #quickly organize the nodes based on how the inputs/outputs are connected
    def organize_nodes():
        pass


    def input(self, key):
        if key == 'scroll up' and self.search_menu == None:
            self.scale *= 1.1
            self.scale_z = 1
            self.position = (self.position - mouse.position) * 1.1 + mouse.position

        if key == 'scroll down' and self.search_menu == None:
            self.scale /= 1.1
            self.scale_z = 1
            self.position = (self.position - mouse.position) / 1.1 + mouse.position

        if key == 'right mouse up':
            self.create_menu = 1
            
        if key == 'space' and self.search_menu == None:
            self.create_menu = 2

    def update(self):
        if mouse.right:
            self.x += mouse.velocity[0]
            self.y += mouse.velocity[1] * window.aspect_ratio
        if self.create_menu > 0:
            
            if (mouse.point == None and mouse.delta_drag.length() < 0.001) or self.create_menu == 2:
                if self.search_menu != None:
                    destroy(self.search_menu)
                self.search_menu = SearchMenu(
                    ShaderBuilderManager.menu_options, 
                    parent = self, 
                    position = Vec3(Vec3(mouse.position) - self.position) / self.scale, 
                    z = -1,
                    color_text = c_text,
                    color_text_highlight = c_text_highlight,
                    color_back = c_node_back,
                    color_search_box = c_node_dark,
                    color_highlight = c_node_light)

                def clear_ref():
                    self.search_menu = None
                self.search_menu.on_destroy = clear_ref
                self.search_menu.on_selected = self.create_node
            self.create_menu = 0
            

    def build_shader(self):
        self.build = {
            'inout' : '',
            'function' : '',
            'main' : '',
        }

        self.build_var_count = dict()
        self.build_var_finished = dict()

        for i in self.shader_nodes:
            i.clear_build_variables()

        # queues the nodes from back to front and moves them back based on dependancies
        # then goes in reverse order
        nodes_to_check = list([n for n in self.shader_nodes if len(n.outputs) == 0 and n.is_all_connected()]) # queues all nodes that have no outputs
        nodes_queued = list(nodes_to_check)
        n = 0
        while n < len(nodes_to_check):            
            for c in nodes_queued[n].inputs:
                node = c.connections[0].parent
                if not node.is_all_connected():
                    print_warning('not all connection made')
                    return 'bad'

                if nodes_queued.count(node) > 0:
                    nodes_queued.remove(node)
                else:
                    nodes_to_check.append(node)
                nodes_queued.append(node)
            n += 1

        # Was back to front, now needs to be front to back (flow from inputs to outputs)
        nodes_queued.reverse() 

        for node in nodes_queued:
            node.build_shader()
        
        final_build = '#version 150\n\n'
        final_build += self.build['inout'] + '\n'
        if len(self.build['function']) > 0: final_build += self.build['function'] + '\n'
        final_build += 'void main(){\n' + self.build['main'] + '}'

        return final_build

    def build_shader_append(self, target, value):
        self.build[target] += value + '\n'

    # returns the variable name with a version if the variable need to be initialized
    # (_vec3_0, vec3 _vec3_0)
    def get_variable(self, data_type):
        if data_type not in self.build_var_finished.keys(): # first variable of that type
            self.build_var_count[data_type] = -1
            self.build_var_finished[data_type] = list()
        
        if len(self.build_var_finished[data_type]) == 0: # no variables not in use
            c = self.build_var_count[data_type] + 1
            self.build_var_count[data_type] = c
            v = '_' + data_type + '_' + str(c)
            return (v, data_type + ' ' + v)

        v = self.build_var_finished[data_type].pop()

        return (v, v) # return a free variable

    def finished_variable(self, data_type, variable):
        self.build_var_finished[data_type].append(variable)

    def create_node(self, val):
        sp = val.split(',')
        if sp[0] == 'ConstantNode':
            self.shader_nodes.append(ConstantNode(parent = self, manager = self, data_type = sp[1], position = self.search_menu.position, z = 0))
        elif sp[0] == 'InstructionNode':
            self.shader_nodes.append(InstructionNode(parent = self, manager = self, instruction = sp[1], position = self.search_menu.position, z = 0))
        else:
            return
        destroy(self.search_menu)
        self.search_menu = None


