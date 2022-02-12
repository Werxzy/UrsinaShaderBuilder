from ursina import *
from bar_menu import BarMenu
from node_user_input import UserInputNode
from node_variable import ConstantNode
from node_builtin_output import BuiltInOutputNode
from node_instruction import InstructionNode
from search_menu import SearchMenu
from shader_instructions import GLSL_catagorized
from color_atlas import *
from shader_node import ShaderNode
from shader_node_connector import NodeConnector

'''
Manager file that holds all the nodes and builds the shader.
'''

class ShaderBuilderManager(Entity):

    menu_options = {
        'Constant' : dict([(v,'ConstantNode,'+v) for v in ConstantNode.data_type_layouts]),
        # 'Instruction' : dict([(v,'InstructionNode,'+v) for v in GLSL])
    }
    menu_options.update(dict((cat,dict((v,'InstructionNode,'+v) for v in con)) for cat,con in GLSL_catagorized.items()))
    right_click_options = {
        'Delete' : 'Delete'
    }

    bar_menu_options = {
        'File' : {
            'New' : 'file,new',
            'Open' : 'file,open',
            'Save' : 'file,save',
        },
        'Vertex' : 'mode,vertex',
        'Fragment' : 'mode,fragment',
    }

    def __init__(self, **kwargs):
        super().__init__(parent = camera.ui)
        # temp model/color

        self.shader_nodes:list[ShaderNode] = []
        self.bar_menu = BarMenu(options = ShaderBuilderManager.bar_menu_options, z = -2, on_selected = self.bar_menu_selected)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.create_menu_trigger = False
        self.node_menu = None
        self.selected_node = None
        self._mode = 'fragment'

        #test node
        self.append_node(InstructionNode(parent = self, manager = self, instruction = 'Add', position = (-0.3,0)))
        self.append_node(InstructionNode(parent = self, manager = self, instruction = 'Subtract', position = (0,0.3)))
        self.append_node(InstructionNode(parent = self, manager = self, instruction = 'Clamp', position = (0.3,0)))
        self.append_node(ConstantNode(parent = self, manager = self, data_type='vec4', position = (-0.6,-0.3)))
        self.append_node(ConstantNode(parent = self, manager = self, data_type='vec3', position = (-0.3,-0.3)))
        self.append_node(UserInputNode(parent = self, manager = self, position = (0.0,-0.3)))
        self.append_node(BuiltInOutputNode(parent = self, manager = self, position = (0.4,-0.3)))


    #quickly organize the nodes based on how the inputs/outputs are connected
    def organize_nodes():
        pass


    def input(self, key):
        if key == 'scroll up' and self.node_menu == None:
            self.scale *= 1.1
            self.scale_z = 1
            self.position = (self.position - mouse.position) * 1.1 + mouse.position

        if key == 'scroll down' and self.node_menu == None:
            self.scale /= 1.1
            self.scale_z = 1
            self.position = (self.position - mouse.position) / 1.1 + mouse.position

        if key == 'right mouse up':
            self.create_menu_trigger = 1
            
        if key == 'space' and self.node_menu == None:
            self.create_menu_trigger = 2

    def update(self):
        if mouse.right:
            self.x += mouse.velocity[0]
            self.y += mouse.velocity[1] * window.aspect_ratio
        if self.create_menu_trigger > 0:
            
            # Create menu with 
            if (mouse.point == None and mouse.delta_drag.length() < 0.001) or self.create_menu_trigger == 2:
                self.create_menu(Vec3(Vec3(mouse.position) - self.position) / self.scale, 
                    ShaderBuilderManager.menu_options, 8, self.create_node)

            if self.create_menu_trigger == 1 and mouse.hovered_entity != None:
                if mouse.hovered_entity.parent in self.shader_nodes:
                    self.create_menu(Vec3(Vec3(mouse.position) - self.position) / self.scale, 
                        ShaderBuilderManager.right_click_options, 
                        len(ShaderBuilderManager.right_click_options), 
                        self.node_menu_selected, 
                        disable_search = True, disable_scroll_bar = True)

                    self.selected_node = mouse.hovered_entity.parent

            self.create_menu_trigger = 0
            

    def build_shader(self, mode):
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
        nodes_to_check = list([n for n in self.shader_nodes if len(n.outputs) == 0 and n.is_all_connected() and n.mode == mode]) # queues all nodes that have no outputs
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

    def create_menu(self, position, options, scroll_count, on_selected, disable_search = False, disable_scroll_bar = False):
        if self.node_menu != None:
            self.destroy_menu()
            
        self.node_menu = SearchMenu(
            options, 
            parent = self, 
            position = position, 
            z = -1,

            disable_search = disable_search,
            disable_scroll_bar = disable_scroll_bar,
            option_scroll_count = scroll_count,

            color_text = c_text,
            color_text_highlight = c_text_highlight,
            color_back = c_node_back,
            color_search_box = c_node_dark,
            color_highlight = c_node_light,
            on_destroy = self.clear_menu_ref,
            on_selected = on_selected)

    def destroy_menu(self):
        destroy(self.node_menu)
        
    def clear_menu_ref(self):
        self.node_menu = None
        self.selected_node = None

    def create_node(self, val):
        sp = val.split(',')
        if sp[0] == 'ConstantNode':
            self.append_node(ConstantNode(parent = self, manager = self, data_type = sp[1], position = self.node_menu.position, z = 0))
        elif sp[0] == 'InstructionNode':
            self.append_node(InstructionNode(parent = self, manager = self, instruction = sp[1], position = self.node_menu.position, z = 0))
        else:
            return
        self.destroy_menu()

    def node_menu_selected(self, val):
        if val == 'Delete':
            self.shader_nodes.remove(self.selected_node)
            destroy(self.selected_node)
            self.selected_node = None
        
        self.destroy_menu()

    def bar_menu_selected(self, val):
        vals = val.split(',')

        if vals[0] == 'mode':
            self.mode = vals[1]
            if NodeConnector.prepared_node != None:
                NodeConnector.prepared_node.destroy_prepared_line()
        elif vals[0] == 'file':
            pass

    def append_node(self, node):
        node.mode = self.mode
        self.shader_nodes.append(node)

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if self._mode == value: return
        self._mode = value
        for n in self.shader_nodes:
            if not isinstance(n, ShaderNode): return
            n.enabled = n.mode == self._mode
