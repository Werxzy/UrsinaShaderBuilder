import string
from ursina import *
from shader_instructions import *
from color_atlas import *
from shader_node_connector import NodeConnector
from extra_models import x_vert

'''
Base class for all nodes.

Almost always a child of shader_builder_manager
'''

class ShaderNode(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        from shader_builder_manager import ShaderBuilderManager
        self.manager:ShaderBuilderManager = None
        self.inputs:list[NodeConnector] = []
        self.outputs:list[NodeConnector] = []
        self.dragged = False
        self.mode = ''

        self.data_type_set = -1 # nth data type in [float, vec2, vec3, ...]
        # needs to be checked any time that a connection would be made or removed
            # or when node settings are changed 

        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.ui_build_width = 0.2
        self.ui_build_pos = 0 # to allow appending ui without intersection
        self.ui_spacing = 0.01

        if self.manager == None:
            print_warning('No manager assigned.')


# - - - ui builder functions - - -

    def append_divider(self):
        self.ui_build_pos -= self.ui_spacing
        return Entity(parent = self, model = 'quad', position = Vec2(0, self.ui_build_pos), scale = (0.2,0.001), color = c_node_dark)

    def append_text(self, text, text_color = c_text, size = 1):
        ent = Text(text, parent = self, color = text_color, scale = size)
        ent.position = Vec2(-ent.width * 0.5, self.ui_build_pos - self.ui_spacing) #adjust based on text width and starting y pos
        self.ui_build_pos -= ent.height + self.ui_spacing # add the starting y position for next element
        self.ui_build_width = max(self.ui_build_width, ent.width + self.ui_spacing * 2)

        return ent

    def append_value_input(self, name, data_type, text_color = c_text, on_change = None):
        ent_name = Text(name + ':', parent = self, scale = 0.8, color = text_color)
        ent_name.position = Vec2(self.ui_spacing - self.ui_build_width * 0.5, self.ui_build_pos - self.ui_spacing)

        if data_type in ['float', 'int', 'uint', 'var']:
            ent_field = TextField(parent = self, scale = 0.8, scroll_size = (12,1), max_lines = 1, type = data_type, register_mouse_input = True)
            if data_type == 'float': ent_field.text = '0.0'
            if data_type in ['int', 'uint']: ent_field.text = '0'
            if data_type == 'var': ent_field.text = 'var'

            ent_field.text_entity.color = text_color
            ent_field.render()
            
            ent_field.position = ent_name.position + Vec2(ent_name.width + self.ui_spacing, -(ent_name.height - ent_field.text_entity.height * 0.8) * 0.5)
            ent_field.shortcuts['indent', 'dedent'] = ('',)

            orig_render = ent_field.render
            
            def render():
                org_length = len(ent_field.text)
                if data_type in ['float', 'int', 'uint']:
                    if org_length == 0:
                        ent_field.text = '0'
                    elif data_type == 'float':
                        ent_field.text = ''.join([e for e in ent_field.text if e in '-0123456789.'])
                        sp = ent_field.text.split('.')
                        if len(sp) > 1: ent_field.text = '.'.join(sp[0:2]) + ''.join(sp[2:])
                        else: ent_field.text = ''.join(sp)

                    elif data_type == 'int':
                        ent_field.text = ''.join([e for e in ent_field.text if e in '-0123456789'])

                    else: # data_type == 'uint':
                        ent_field.text = ''.join([e for e in ent_field.text if e in '0123456789'])

                    if len(ent_field.text) == 0:
                        ent_field.text = '0'
                    else:
                        ent_field.text = ent_field.text[0] + ent_field.text[1:].replace('-','')
                    
                elif data_type == 'var':
                    if org_length == 0:
                        ent_field.text = 'var'
                    if ent_field.text[0] not in string.ascii_letters + '_':
                        ent_field.text = '_' + ent_field.text
                    ent_field.text = ''.join([e for e in ent_field.text if e in string.ascii_letters + '0123456789_'])
                
                ent_field.cursor.x -= org_length - len(ent_field.text)
                ent_field.cursor.x = max(0, ent_field.cursor.x)
                if len(ent_field.text) < ent_field.scroll_size[0]:
                    ent_field.scroll_position = (0,0)

                orig_render()
                if on_change != None: on_change(ent_field.text)

            ent_field.render = render

            quadScale = Vec2(self.ui_build_width - ent_name.width - self.ui_spacing * 2.5, ent_name.height + self.ui_spacing * 0.5)
            ent_field_back = Entity(parent = self, model = Quad(scale = quadScale, radius=0.006), origin_x = -quadScale.x * 0.5, origin_y = quadScale.y * 0.5, color = c_node_dark)
            ent_field_back.position = ent_name.position + Vec2(ent_name.width + self.ui_spacing * 0.5, self.ui_spacing * 0.25)
            ent_field_back.z = 0.05

            ent_field.scroll_size = (floor(quadScale.x / ent_field.text_entity.width * len(ent_field.text) / 0.8 - 1),1)

        elif data_type == 'bool':
            x_model = Mesh(vertices=x_vert, mode='ngon', static=False)

            ent_field = Entity(parent = self, position = ent_name.position, scale = ent_name.height * 0.25, origin = (-2, 2, 0), model = x_model, color = text_color, visible = False)
            ent_field.text = 'false'
            ent_field.x += ent_name.width + self.ui_spacing * 0.75

            quadScale = Vec2(ent_name.height + self.ui_spacing * 0.5, ent_name.height + self.ui_spacing * 0.5)
            ent_field_back = Entity(parent = self, model = Quad(scale = quadScale, radius=0.006), z = 0.05, origin_x = -quadScale.x * 0.5, origin_y = quadScale.y * 0.5, color = c_node_dark, collider='box')
            ent_field_back.position = Vec2(ent_name.x + ent_name.width + self.ui_spacing * 0.5, ent_name.y + self.ui_spacing * 0.25)

            def set_value(val):
                ent_field.text = 'true' if val else 'false'
                ent_field.visible = val
                if on_change != None: on_change(ent_field.text)

            ent_field.set_value = set_value

            def back_input(key):
                if key == 'left mouse down' and ent_field_back.hovered:
                    ent_field.set_value(ent_field.text == 'false')

            ent_field_back.input = back_input                

        else:
            print_warning('ShaderNode.append_value_input() : invalid data type : ' + str(data_type))           

        self.ui_build_pos -= ent_name.height + self.ui_spacing # add the starting y position for next element
        # self.ui_build_width = max(self.ui_build_width, ent.width + self.ui_spacing)

        return (ent_name, ent_field, ent_field_back)

    def append_drop_down(self, name, options:dict, on_select, text_color = c_text, start_value = ''):
        ent_name = Text(name + ':', parent = self, scale = 0.8, color = text_color)
        ent_name.position = Vec2(self.ui_spacing - self.ui_build_width * 0.5, self.ui_build_pos - self.ui_spacing)

        ent_field = Text(list(options.keys())[0] if start_value == '' else start_value, parent = self, position = ent_name.position, scale = 0.8, color = text_color)
        ent_field.x += ent_name.width + self.ui_spacing

        quadScale = Vec2(self.ui_build_width - ent_name.width - self.ui_spacing * 2.5, ent_field.height + self.ui_spacing * 0.5)
        ent_field_back = Entity(parent = self, model = Quad(scale = quadScale, radius=0.006), z = 0.05, origin_x = -quadScale.x * 0.5, origin_y = quadScale.y * 0.5, color = c_node_dark, collider='box')
        ent_field_back.position = Vec2(ent_name.x + ent_name.width + self.ui_spacing * 0.5, ent_field.y + self.ui_spacing * 0.25)

        def on_select_wrapper(option):
            ent_field.text = option
            self.manager.destroy_menu()
            on_select(option)

        def back_input(key):
            if key == 'left mouse down' and ent_field_back.hovered:
                self.manager.create_menu(Vec3(ent_field_back.get_position(self.manager)) - Vec3(ent_field_back.origin_x, -self.ui_spacing * 0.5,0),
                    options, min(len(options), 8), on_select_wrapper, width = 0.16)

        ent_field_back.input = back_input
        ent_field_back.on_destroy = self.manager.destroy_menu

        self.ui_build_pos -= ent_name.height + self.ui_spacing # add the starting y position for next element

        return (ent_name, ent_field, ent_field_back)

    # needs to be the last appended to be stable
    # automatically appends the back
    def append_expandable_text_field(self, text = '', size = [0.3,0.3], text_size = 0.8):
        w = Text.get_width('a', font='VeraMono.ttf') * text_size
        h = Text.size * text_size
        inner_space = self.ui_spacing * 0.5
        ent_text = TextField(parent = self, 
            position = (size[0] * -0.5, self.ui_build_pos - self.ui_spacing - inner_space, 0), 
            register_mouse_input = True, 
            scroll_size = (floor(size[0] / w), floor(size[1] / h)),
            text = text,
            scale = text_size)
        self.manager.append_activeable_entity(ent_text)
        ent_text.node_size = size
        
        quadScale = Vec2(size[0] + inner_space * 2, size[1] + inner_space * 2)
        ent_text_back = Entity(parent = self, 
            model = Quad(scale = quadScale, radius=0.006), 
            y = self.ui_build_pos - self.ui_spacing,
            z = 0.05, 
            origin_y = quadScale.y * 0.5, 
            color = c_node_dark,
            collider = 'box')
        destroy(ent_text.bg)
        ent_text.bg = ent_text_back


        self.ui_build_pos -= size[1] + self.ui_spacing + inner_space * 2
        self.ui_build_width = max(self.ui_build_width, size[0] + self.ui_spacing * 2 + inner_space * 2)

        self.ui_back = self.build_back()

        return (ent_text, ent_text_back)

    def build_back(self):
        quadScale = Vec2(self.ui_build_width, -self.ui_build_pos + self.ui_spacing)
        ent = Entity(parent = self, model = Quad(scale = quadScale, radius=0.02), z = 0.1, origin_y = quadScale.y * 0.5, color = c_node_back, collider='box')
        return ent

    def build_connector(self, variable, variable_type, isOutput, offset = 0, optional = False):
        conn = NodeConnector(parent = self, x_disp = self.ui_build_width * 0.5, yth = offset, variable = variable, variable_type = variable_type, isOutput = isOutput, optional = optional)
        if isOutput:
            self.outputs.append(conn)
        else:
            self.inputs.append(conn)
        return conn


# - - - - - - -

    #goes through all of the outputs and checks the data types that are possible, disconnecting any invalid connections
    def update_connections(self):
        nodes = [self]
        while len(nodes) > 0:
            if len(nodes[0].inputs) > 0:
                r = set(range(len(nodes[0].inputs[0].variable_type)))
                for i in nodes[0].inputs: # get overlaps that exist on each node (disconnect any if they suddenly don't work)
                    p_types = i.get_possible_data_types()
                    
                    data_types = set()
                    for p in p_types:
                        data_types.add(p[0])
                    r_overlap = r & data_types
                    
                    if len(r_overlap) == 0:# no matching types
                        i.disconnect_all() # should only be one anyways
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

    # Returns true if:
    # len(inputs) > 0 and all connected and at least 1 output connected
    # len(inputs) > 0 and all connected and len(outputs) == 0
    # len(inputs) == 0 and there is at least 1 output connected
    # len(inputs) == 0 and len(outputs) == 0 (this is a weird but useful case)
    def is_all_connected(self):
        if len(self.inputs) > 0:
            for i in self.inputs:
                if not (i.any_connected() or i.optional):
                    return False

        if len(self.outputs) > 0:
            for o in self.outputs:
                if o.any_connected():
                    return True

            return False

        return True

    def any_outputs_connected(self):
        for o in self.outputs:
            if o.any_connected():
                return True
        return False
    
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
            i.disconnect_all()
        for o in self.outputs:
            o.disconnect_all()


# - - - shader builder functions - - -

    # Called when building the shader.
    # To be replaced in inheriting classes.
    def build_shader(self): pass

    # Called when adding a node to the manager.
    # determines if the node is usable in the given mode.
    def valid_mode(self, mode): return True

    # Checks if the node is ready to build.
    def is_build_ready(self):
        ready = True
        
        for i in self.inputs:
            if not i.is_build_ready():
                ready = False
                break

        return ready

    def clear_build_variables(self):
        for o in self.outputs:
            o.clear_build_variable()

    # Called when preparing to save the shader.
    # Returns any data unique to this node's class.
    def save(self): return {}

    # Called when loading the node.
    # Sets data of the node.
    # The manager will handle the connections and position.
    def load(manager, data): return None
        