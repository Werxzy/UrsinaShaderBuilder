import json
import string
from tkinter import Tk, filedialog, messagebox
from ursina import *

from Prefabs.bar_menu import BarMenu
from Prefabs.search_menu import SearchMenu
from Prefabs.warning_message import WarningMessage

from shader_node import ShaderNode
from shader_node_connector import NodeConnector
from Nodes.node_user_inout import UserInOutNode
from Nodes.node_variable import ConstantNode
from Nodes.node_builtin_output import BuiltInOutputNode
from Nodes.node_instruction import InstructionNode
from Nodes.node_variable_splitter import VariableSplitterNode
from Nodes.node_convert import ConvertNode
from Nodes.node_comment import CommentNode
from Nodes.node_preview_shader_input import PreviewShaderInputNode
from Nodes.node_array_access import ArrayAccessNode
from Nodes.node_array_assign import ArrayAssignNode

from shader_instructions import DataTypeLayouts, GLSL_catagorized
from ExtraData.color_atlas import *
from ExtraData.builtin_shaders import Base_Shader

'''
Manager file that holds all the nodes and builds the shader.
'''

class ShaderBuilderManager(Entity):

    version = '0.1.0'

    menu_options = {
        'Inputs/Outputs' : {
            'Shader Input' : 'UserInOutNode,input', 
            'Shader Output' : 'UserInOutNode,output', 
            'Built-In' : dict([(v,'BuiltInOutputNode,'+v) for v in BuiltInOutputNode.build_in_attributes.keys()])
            },
        'Constant' : dict([(v,'ConstantNode,'+v) for v in DataTypeLayouts]),
        'Conversion' : {
            'Splitter / Merger' : 'VariableSplitterNode,a',
            'Type Conversion' : 'ConvertNode,a',
        },
        'Array' : {
            'Array Access' : 'ArrayAccessNode,a',
            'Array Assign' : 'ArrayAssignNode,a',
        },
        # 'Instruction' : dict([(v,'InstructionNode,'+v) for v in GLSL])
    }
    menu_options.update(dict((cat,dict((v,'InstructionNode,'+v) for v in con)) for cat,con in GLSL_catagorized.items()))
    menu_options.update({'Comment' : 'CommentNode,a'})

    right_click_options = {
        'Delete' : 'Delete'
    }

    bar_menu_options = {
        'File' : {
            'New...' : {
                'New Empty': 'file,new,empty',
                'Example Shader': 'file,new,base',
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

        self.shader_nodes:list[ShaderNode] = []
        self.bar_menu = BarMenu(options = ShaderBuilderManager.bar_menu_options, z = -2, on_selected = self.bar_menu_selected)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.create_menu_trigger = False
        self.node_menu = None
        self.selected_node = None
        self._mode = 'fragment'
        self.activeable_entities = []
        self.shader_inputs = dict()

        self.tk = Tk()
        self.tk.withdraw()

        self.preview_entity:Entity = None
        self.preview_cam = None


    #quickly organize the nodes based on how the inputs/outputs are connected
    def organize_nodes():
        pass


    def input(self, key):
        if self.mode == 'preview': return

        not_active = not self.any_active_entities()

        if key == 'scroll up' and not_active:
            self.scale *= 1.1
            self.scale_z = 1
            self.position = (self.position - mouse.position) * 1.1 + mouse.position

        if key == 'scroll down' and not_active:
            self.scale /= 1.1
            self.scale_z = 1
            self.position = (self.position - mouse.position) / 1.1 + mouse.position

        if key == 'right mouse down':
            for an in self.animations:
                an.kill()
                
        if key == 'right mouse up':
            self.create_menu_trigger = 1
            
        if key == 'space' and not_active:
            self.create_menu_trigger = 2

        if key == 's' and held_keys['control']:
            self.save_load(False)
            
        if key == 'o' and held_keys['control']:
            self.save_load(True)

        if key == 'n' and held_keys['control']:
            if self.confirm_window('Start a new Shader?\nAny unsaved work will be lost.'):
                self.destroy_all_nodes()

    def update(self):
        if self.preview_entity != None:
            self.preview_entity.rotation_y += time.dt * 10

        if self.mode == 'preview': return

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
            

    def build_shader(self, mode, clear_shader_inputs = True):
        if clear_shader_inputs:
            self.shader_inputs.clear()

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
        if nodes_queued[0]:
            to_pos = -nodes_queued[1].position
            to_pos.y -= nodes_queued[1].ui_build_pos * 0.5
            self.send_message('Warning : Required input not connected.', self.move_window_to, to_pos, mode)
            return 'bad'

        for node in nodes_queued[1]:
            node.build_shader()
        
        final_build = '#version 450\n\n'
        final_build += self.build['inout'] + '\n'
        if len(self.build['function']) > 0: final_build += self.build['function'] + '\n'
        final_build += 'void main(){\n' + self.build['main'] + '}'

        return final_build

    def save_shader(self, location = ''):
        
        data = {'version': ShaderBuilderManager.version, 'nodes':{}}
        
        nodes_queued = self.get_ordered_nodes()
        if nodes_queued[0]: return

        for i,node in enumerate(nodes_queued[1]):
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
        f = self.build_shader('fragment', False)

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
                self.send_message('Error : Failed to load file.')
                return

        if data['version'] != ShaderBuilderManager.version:
            self.send_message('Error : Unsupported version : ' + data['version'])
            return

        self.destroy_all_nodes()

        new_shader_nodes:dict[str,ShaderNode] = dict()

        for shader_type, nodes in data['nodes'].items():
            for name, node in nodes.items():
                node_class = node['class']
                if not all(c in string.ascii_letters for c in node_class):
                    self.send_message('Warning : Potential malicious input in file : ' + node_class + '.\n')
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
        self.quit_preview(self.shader_nodes[0].mode)
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
                    return (True, node)

                if nodes_queued.count(node) > 0:
                    nodes_queued.remove(node)
                nodes_to_check.append(node)
                nodes_queued.append(node)
            n += 1

        # Was back to front, now needs to be front to back (flow from inputs to outputs)
        nodes_queued.reverse() 

        return (False, nodes_queued)

    def preview_shader(self):
        build_time = time.time()
        
        v = self.build_shader('vertex')
        f = self.build_shader('fragment', False)
        if v == 'bad' or f == 'bad':
            return

        build_time = time.time() - build_time

        print('Vertex Shader :')
        print(v)
        print('Fragment Shader :')
        print(f)

        print('\nBuild Time:', build_time)

        s = Shader(vertex = v, fragment = f)

        self.preview_cam = EditorCamera()

        self.destroy_preview_entity()
        self.preview_entity = Entity(model = 'sphere', shader = s)

        for data_name, v in self.shader_inputs.items():
            data_type = v['data type']
            if data_type in DataTypeLayouts.keys():
                vals = ()
                for _ in DataTypeLayouts[data_type].items():
                    vals += (False if data_type[0] == 'b' else 0,)
                self.preview_entity.set_shader_input(data_name, vals)
            
        self._prev_mode = self.mode
        self.mode = 'preview'
        self.preview_input_node = PreviewShaderInputNode(self.shader_inputs, self.preview_entity, manager = self)
        self.scale = 1

    def quit_preview(self, mode = ''):
        if self.preview_cam != None:
            destroy(self.preview_cam)
            self.preview_cam = None
            destroy(self.preview_input_node)
            self.preview_input_node = None
        
        self.mode = mode if mode != '' else self._prev_mode

    def destroy_preview_entity(self):
        if self.preview_entity != None:
            destroy(self.preview_entity)
            self.preview_entity = None

    def build_shader_append(self, target, value, to_end = True):
        if target == 'inout' and value in self.build[target]:
            print('Detected duplicate inout value:', value) # this is okay, but don't have duplicates
        elif to_end:
            self.build[target] += value + '\n'
        else:
            self.build[target] = value + '\n' + self.build[target]

    # used to build a list of inputs that can be set by set_shader_input
    def build_shader_input_append(self, data_type, name, default = ''):
        if name in self.shader_inputs:
            pass # update it?
        else:
            self.shader_inputs.update({name: {'data type' : data_type, 'default' : default}})
    

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

    def append_activeable_entity(self, e):
        self.activeable_entities.append(e)

        if hasattr(e, 'on_destroy'):
            old_destroy = e.on_destroy
            def new_destroy():
                self.activeable_entities.remove(e)
                old_destroy()
            e.on_destroy = new_destroy
        else:
            def new_destroy():
                self.activeable_entities.remove(e)
            e.on_destroy = new_destroy

    def any_active_entities(self):
        if self.node_menu != None:
            return True
        for a in self.activeable_entities:
            if a.active:
                return True
        return False
        
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
        elif sp[0] == 'CommentNode':
            self.append_node(CommentNode(parent = self, manager = self, text = 'howdy :)' if random.random() < 0.005 else '', position = self.node_menu.position, z = 0))
        elif sp[0] == 'ArrayAccessNode':
            self.append_node(ArrayAccessNode(parent = self, manager = self, position = self.node_menu.position, z = 0))
        elif sp[0] == 'ArrayAssignNode':
            self.append_node(ArrayAssignNode(parent = self, manager = self, position = self.node_menu.position, z = 0))
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
            if self.mode == 'preview':
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
        ftypes = [('ursina shader files', '*.ursinashader'), ('JSON files', '*.json'), ('All files', '*')]
        if to_load: loc:str = filedialog.Open(parent = self.tk, filetypes = ftypes).show()
        else:       loc:str = filedialog.SaveAs(parent = self.tk, filetypes = ftypes).show()
        if loc != '': 
            if to_load: 
                self.load_shader(loc)
            else:  
                if not loc.endswith('.ursinashader'):
                    loc += '.ursinashader'
                self.save_shader(loc)

    def load_file(self, types):
        ftypes = [(t[1:] + ' files', '*' + t) for t in types]
        ftypes.insert(0, ('All files', '*'))
        return filedialog.Open(parent = self.tk, filetypes = ftypes).show()

    def confirm_window(self, message = 'Are you sure?'):
        return messagebox.askquestion('Confirm', message, parent = self.tk) == 'yes'

    def send_message(self, message, on_click = None, *click_args):
        WarningMessage(message, on_click = on_click, click_args = click_args, color_text = c_text, color_back = c_node_dark, color_close = c_red, z = -1)

    def move_window_to(self, pos, mode):
        self.mode = mode
        from ursina import curve
        self.animate('position', Vec3(pos[0], pos[1], 0), 1, curve=curve.in_out_cubic).start()

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
