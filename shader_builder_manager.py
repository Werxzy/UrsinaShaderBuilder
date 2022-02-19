import json
import string
from tkinter import Tk, filedialog, messagebox
from ursina import *

from bar_menu import BarMenu
from search_menu import SearchMenu

from shader_node import ShaderNode
from shader_node_connector import NodeConnector
from node_user_inout import UserInOutNode
from node_variable import ConstantNode
from node_builtin_output import BuiltInOutputNode
from node_instruction import InstructionNode
from node_variable_splitter import VariableSplitterNode
from node_convert import ConvertNode

from shader_instructions import GLSL_catagorized
from color_atlas import *

'''
Manager file that holds all the nodes and builds the shader.
'''

class ShaderBuilderManager(Entity):

    version = '0.0'

    menu_options = {
        'Inputs/Outputs' : {
            'Shader Input' : 'UserInOutNode,input', 
            'Shader Output' : 'UserInOutNode,output', 
            'Built-In' : dict([(v,'BuiltInOutputNode,'+v) for v in BuiltInOutputNode.build_in_attributes.keys()])
            },
        'Constant' : dict([(v,'ConstantNode,'+v) for v in ConstantNode.data_type_layouts]),
        'Conversion' : {
            'Splitter / Merger' : 'VariableSplitterNode,a',
            'Type Conversion' : 'ConvertNode,a',
        }
        # 'Instruction' : dict([(v,'InstructionNode,'+v) for v in GLSL])
    }
    menu_options.update(dict((cat,dict((v,'InstructionNode,'+v) for v in con)) for cat,con in GLSL_catagorized.items()))
    right_click_options = {
        'Delete' : 'Delete'
    }

    bar_menu_options = {
        'File' : {
            'New...' : {
                'New Empty': 'file,new,empty',
                'New Prebuilt': 'file,new,base',
            },
            'Open' : 'file,open',
            'Save' : 'file,save',
            ' div': 'div',
            'Exit': 'exit',
        },
        'Vertex' : 'mode,vertex',
        'Fragment' : 'mode,fragment',
        'Preview' : 'preview'
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

        self.tk = Tk()
        self.tk.withdraw()

        self.preview_entity:Entity = None
        self.preview_cam = None

        #test node
        self.append_node(InstructionNode(parent = self, manager = self, instruction = 'Add', position = (-0.3,0)))
        self.append_node(VariableSplitterNode(parent = self, manager = self, position = (0,0.3)))
        self.append_node(InstructionNode(parent = self, manager = self, instruction = 'Clamp', position = (0.3,0)))
        self.append_node(ConstantNode(parent = self, manager = self, data_type='vec4', position = (-0.6,-0.3)))
        self.append_node(UserInOutNode(parent = self, manager = self, isOutput = True, position = (-0.3,-0.3)))
        self.append_node(UserInOutNode(parent = self, manager = self, isOutput = False, position = (0.0,-0.3)))
        self.append_node(BuiltInOutputNode(parent = self, manager = self, position = (0.4,-0.3)))


    #quickly organize the nodes based on how the inputs/outputs are connected
    def organize_nodes():
        pass


    def input(self, key):
        if self.mode == 'hide all': return

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

        if key == 's' and held_keys['control']:
            self.save_load(False)
            
        if key == 'o' and held_keys['control']:
            self.save_load(True)

        if key == 'n' and held_keys['control']:
            if self.confirm_window('Start a new Shader?\nAny unsaved work will be lost.'):
                self.destroy_all_nodes()

    def update(self):
        if self.mode == 'hide all': return

        if mouse.right:
            self.x += mouse.velocity[0]
            self.y += mouse.velocity[1] * window.aspect_ratio
        if self.create_menu_trigger > 0:
            
            # Create menu with 
            if (mouse.point == None and mouse.delta_drag.length() < 0.001) or self.create_menu_trigger == 2:
                self.create_menu(Vec3(Vec3(mouse.position) - self.position) / self.scale, 
                    ShaderBuilderManager.menu_options, 8, self.create_node)

            if self.create_menu_trigger == 1 and mouse.hovered_entity != None and mouse.delta_drag.length() < 0.001:
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

        nodes_queued = self.get_ordered_nodes(mode)
        if nodes_queued == 'bad':
            print_warning('not all connection made')
            return 'bad'

        for node in nodes_queued:
            node.build_shader()
        
        final_build = '#version 150\n\n'
        final_build += self.build['inout'] + '\n'
        if len(self.build['function']) > 0: final_build += self.build['function'] + '\n'
        final_build += 'void main(){\n' + self.build['main'] + '}'

        return final_build

    def save_shader(self, location = ''):
        
        data = {'version': ShaderBuilderManager.version, 'nodes':{}}
        
        nodes_queued = self.get_ordered_nodes()
        if nodes_queued == 'bad': return

        for i,node in enumerate(nodes_queued):
            save_data = node.save()
            if save_data == 'no not save': continue
            # there may be a case in which a node shouldn't be saved

            if node.mode not in data['nodes'].keys():
                data['nodes'].update({node.mode : {}})
            
            node.save_name = 'node_' + str(i) # name just helps other nodes communicate what they are connected to.

            node_data = {
                'class' : type(node).__name__,
                'position' : [node.x, node.y],
                'input connections' : [],
            }
            for inp in node.inputs:
                if inp.any_connected():
                    conn = inp.connections[0]
                    node_data['input connections'].append(conn.parent.save_name + '.' + str(conn.parent.outputs.index(conn)))
                else:
                    node_data['input connections'].append('disconnected')

            node_data.update(save_data)
            data['nodes'][node.mode].update({node.save_name : node_data})

        v = self.build_shader('vertex')
        f = self.build_shader('fragment')

        if v != 'bad': data.update({'vertex' : v})
        if f != 'bad': data.update({'fragment' : f})
        
        with open(location, 'w') as json_file:
            json.dump(data, json_file)

    def load_shader(self, location, data = dict()):
        if not self.confirm_window('Load shader?\nAny unsaved work will be lost.'): return

        if location != '':
            try:
                data = json.load(open(location, 'r'))
            except Exception as e:
                print_warning('file error', e)
                return

        if data['version'] != ShaderBuilderManager.version:
            print_warning('unsupported version', data['version'])
            return

        self.destroy_all_nodes()

        new_shader_nodes:dict[str,ShaderNode] = dict()

        for shader_type, nodes in data['nodes'].items():
            for name, node in nodes.items():
                node_class = node['class']
                if not all(c in string.ascii_letters for c in node_class):
                    print_warning('Potential malicious input ' + node_class + '.\n')
                    return

                new_node:ShaderNode = eval(node_class).load(self, node)
                new_node.mode = shader_type
                new_node.position = Vec3(node['position'][0], node['position'][1], 0)

                for i,conn in enumerate(node['input connections']):
                    conn:str
                    if conn == 'disconnected': continue
                    pos = conn.split('.')
                    new_node.inputs[i].connect(new_shader_nodes[pos[0]].outputs[int(pos[1])])
                
                new_shader_nodes.update({name : new_node})

        self.shader_nodes.extend(new_shader_nodes.values())
        self.set_nodes_visisble()

    def get_ordered_nodes(self, mode = ''):
        # queues the nodes from back to front and moves them back based on dependancies
        # then goes in reverse order
        nodes_to_check = list([n for n in self.shader_nodes if (len(n.outputs) == 0 and n.is_all_connected() and n.mode == mode) 
                                                            or (not n.any_outputs_connected() and mode == '')]) 
        # queues all nodes that have no outputs
        # if no mode is set, queue any node with no *connected* outputs

        nodes_queued = list(nodes_to_check)
        n = 0
        while n < len(nodes_to_check):
            for c in nodes_to_check[n].inputs:
                if not c.any_connected(): continue
                node = c.connections[0].parent
                if not node.is_all_connected() and mode != '':
                    return 'bad'

                if nodes_queued.count(node) > 0:
                    nodes_queued.remove(node)
                else:
                    nodes_to_check.append(node)
                nodes_queued.append(node)
            n += 1

        # Was back to front, now needs to be front to back (flow from inputs to outputs)
        nodes_queued.reverse() 

        return nodes_queued

    def preview_shader(self):
        build_time = time.time()
        
        v = self.build_shader('vertex')
        f = self.build_shader('fragment')
        if v == 'bad' or f == 'bad':
            print_warning('Can\'t build shader.')
            return

        build_time = time.time() - build_time

        print('Vertex Shadder :')
        print(v)
        print('Fragment Shader :')
        print(f)

        print('\nBuild Time:', build_time)

        s = Shader(vertex = v, fragment = f)

        self.preview_cam = EditorCamera()

        self.destroy_preview_entity()
        self.preview_entity = Entity(model = 'sphere', shader = s)
        self._prev_mode = self.mode
        self.mode = 'hide all'

    def quit_preview(self, mode = ''):
        if self.preview_cam != None:
            destroy(self.preview_cam)
            self.preview_cam = None
        
        self.mode = mode if mode != '' else self._prev_mode

    def destroy_preview_entity(self):
        if self.preview_entity != None:
            destroy(self.preview_entity)
            self.preview_entity = None

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

    def create_menu(self, position, options, scroll_count, on_selected, disable_search = False, disable_scroll_bar = False, **kwargs):
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
            on_selected = on_selected,
            **kwargs)

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
        elif sp[0] == 'UserInOutNode':
            self.append_node(UserInOutNode(parent = self, manager = self, isOutput = sp[1] == 'input', position = self.node_menu.position, z = 0))
        elif sp[0] == 'BuiltInOutputNode':
            self.append_node(BuiltInOutputNode(parent = self, manager = self, variable = sp[1], position = self.node_menu.position, z = 0))
        elif sp[0] == 'VariableSplitterNode':
            self.append_node(VariableSplitterNode(parent = self, manager = self, position = self.node_menu.position, z = 0))
        elif sp[0] == 'ConvertNode':
            self.append_node(ConvertNode(parent = self, manager = self, position = self.node_menu.position, z = 0))
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
            if self.mode == 'hide all':
                self.quit_preview()
            self.mode = vals[1]
            if NodeConnector.prepared_node != None:
                NodeConnector.prepared_node.destroy_prepared_line()
        elif vals[0] == 'file':
            if vals[1] == 'open':
                self.save_load(True)

            elif vals[1] == 'save':
                self.save_load(False)

            elif vals[1] == 'new':
                if vals[2] == 'empty':
                    if self.confirm_window('Start a new Shader?\nAny unsaved work will be lost.'):
                        self.destroy_all_nodes()
                elif vals[2] == 'base':
                    self.load_shader('', Base_Shader)

        elif vals[0] == 'exit':
            if self.confirm_window('Are you sure?\nAny unsaved work will be lost.'):
                sys.exit()
            
        elif vals[0] == 'preview':
            if NodeConnector.prepared_node != None:
                NodeConnector.prepared_node.destroy_prepared_line()
            if self.preview_cam == None:
                self.preview_shader()

    def save_load(self, to_load):
        ftypes = [('JSON files', '*.json'), ('All files', '*')]
        if to_load: loc = filedialog.Open(parent = self.tk, filetypes = ftypes).show()
        else:       loc = filedialog.SaveAs(parent = self.tk, filetypes = ftypes).show()
        if loc != '': 
            if to_load: self.load_shader(loc)
            else:  self.save_shader(loc)

    def confirm_window(self, message = 'Are you sure?'):
        return messagebox.askquestion('Confirm', message, parent = self.tk) == 'yes'

    def append_node(self, node:ShaderNode):
        if node.valid_mode(self.mode):
            node.mode = self.mode
            self.shader_nodes.append(node)
        else:
            destroy(node)

    def destroy_all_nodes(self):
        for n in self.shader_nodes:
            destroy(n)
        self.shader_nodes.clear()
        destroy(self.preview_entity)
        self.preview_entity = None

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if self._mode == value: return
        self._mode = value
        self.set_nodes_visisble()

    def set_nodes_visisble(self):
        for n in self.shader_nodes:
            n.enabled = n.mode == self._mode
