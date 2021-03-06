from ursina import *
from instanced_box import InstancedBox
from shader_instructions import DataTypes
from shader_node import ShaderNode
from ExtraData.color_atlas import *
from ExtraData.extra_models import *

'''
Creates a definition of a struct
'''

class StructDefinitionNode(ShaderNode):

    array_options = {
        'Single Variable' : 0,
        'Array' : 1,
        '2D Array' : 2,
        '3D Array' : 3,
    }

    def __init__(self, name = 'struct_name', **kwargs):
        super().__init__(**kwargs)

        self.ui_build_width = 0.25

        self.append_text('Struct Definition', size = 0.8)
        self.append_divider()
        self.ui_name = self.append_value_input('Name', 'var')
        self.ui_name[1].text = name
        self.ui_name[1].render()
        self.append_divider()
        self.button = self.append_button('Add Variable', self.add_group, color = c_green_dark)
        self.build_back()

        self.section_groups = []
        # array of tuples
        # [0] = variable name
        # [1] = variable type
        # [2] = array dimensions
        # [3] = array of array size fields
        # [4] = divider

    def find_group(self, entity):
        for i, g in enumerate(self.section_groups):
            if entity in g:
                return i
        return -1

    def add_group(self, data_type = None, array_start = None, array_sizes = None):
        ui_type = self.append_drop_down('Type', dict((v,v) for v in DataTypes), self.on_selected)
        if data_type: ui_type[1].text = data_type
        ui_array = self.append_drop_down('', StructDefinitionNode.array_options, on_select = self.on_array_change, extra_info = ui_type, set_to_key = True)
        if array_start: ui_array[1].text = array_start
        ui_buttons = self.append_side_buttons(ui_type)
        ui_div = self.append_divider()
        
        self.move_ui_section(ui_buttons, self.button, True)
        self.move_ui_section(ui_type, self.button, True)
        self.move_ui_section(ui_array, self.button, True)
        self.move_ui_section(ui_div, self.button, True)

        self.build_back()

        section = [ui_buttons, ui_type, ui_array, ui_div, list()]
        self.section_groups.append(section)

        if array_sizes: self.on_array_change(ui_buttons, len(array_sizes), array_sizes)

        return section


    def append_side_buttons(self, section_starter):
        button_size = 0.015
        spacing = self.ui_spacing * 0.5
        rounding = 0.01
        extra = 0.01
        quadScale = Vec2(button_size + spacing * 2, button_size * 3 + spacing * 4)
        back = InstancedBox.main_group.new_entity(parent = self, 
            box_scale = (quadScale.x * 0.5 - rounding + extra, quadScale.y * 0.5 - rounding, rounding * 2, rounding * 2), 
            position = (-self.ui_build_width * 0.5 - button_size * 0.5 - spacing + extra, -quadScale.y * 0.5 + self.ui_build_pos, 0.2), 
            color = c_node_dark)

        x_start = -button_size * 0.5 - extra
        y_start = button_size + spacing

        self.create_button(back, button_size, (x_start, y_start, -0.01), up_arrow_vert, (section_starter, 0), c_node_light)
        y_start -= spacing + button_size
        self.create_button(back, button_size, (x_start, y_start, -0.01), down_arrow_vert, (section_starter, 1), c_node_light)
        y_start -= spacing + button_size
        self.create_button(back, button_size, (x_start, y_start, -0.01), x_vert, (section_starter, 2), c_red)

        return self.append_ui_section((back, 0))
        
    def create_button(self, parent, size, position, model, data, color):

        def input(key):
            if key == 'left mouse down' and button.hovered:
                self.button_press(button.data)

        button = Entity(parent = parent,
            model = Mesh(vertices=model, mode='ngon', static=False), 
            scale = size * 0.25, 
            collider = 'box',
            position = position,
            origin = (-2,0,0),
            color = color)

        button.data = data
        button.input = input

        return button

    def button_press(self, data):
        group = self.find_group(data[0])
        b = data[1]

        if b == 0: # move up
            if group == 0: return
            self.move_group_up(group)

        elif b == 1: # move down
            if group + 1 == len(self.section_groups): return
            self.move_group_up(group + 1)

        elif b == 2: # remove
            for e in self.section_groups[group][:-1]:
                self.remove_ui_section(e)
            for e in self.section_groups[group][-1]:
                self.remove_ui_section(e)
            self.section_groups.pop(group)
            self.build_back()

    def move_group_up(self, group):
        start = self.section_groups[group - 1][0]
        div = self.section_groups[group][-2]

        for e in self.section_groups[group][:-1]:
            self.move_ui_section(e, start, True)
        for e in self.section_groups[group][-1]:
            self.move_ui_section(e, div, True)

        (self.section_groups[group], self.section_groups[group - 1]) = (self.section_groups[group - 1], self.section_groups[group])

    def on_selected(self, key):
        pass
        #TODO update data type when things change

    def on_array_change(self, info, option, replace_vals = []):
        group = self.find_group(info)
        dimensions = self.section_groups[group][-1]
        divider = self.section_groups[group][-2]

        while len(dimensions) > option:
            self.remove_ui_section(dimensions.pop())

        for i in range(len(dimensions), option):
            d = self.append_value_input(f"{'[]'*i}[{'xyzw'[i]}]", 'uint')
            dimensions.append(d)
            self.move_ui_section(d, divider, True)
            if i < len(replace_vals):
                dimensions[i][1].text = replace_vals[i]
                dimensions[i][1].render(False)

        self.build_back()


    def build_shader(self):
        v = f'struct {self.ui_name[1].text}{{\n'

        for i, g in enumerate(self.section_groups):
            v += g[1][1].text
            for d in g[-1]:
                v += f'[{d[1].text}]'
            v += f' _{i};\n'
        
        v += '};'

        self.manager.build_shader_append('struct', v)

    def save(self): 
        return {
            'name' : self.ui_name[1].text,
            'variables' : [[g[1][1].text] + [d[1].text for d in g[-1]] for g in self.section_groups]
        }

    def load(manager, data):
        node = StructDefinitionNode(parent = manager, manager = manager, name = data['name'])
        for v in data['variables']:
            c = len(v) - 1
            if c: node.add_group(v[0], list(StructDefinitionNode.array_options)[c], v[1:])
            else: node.add_group(v[0], None, None)
        
        return node
        