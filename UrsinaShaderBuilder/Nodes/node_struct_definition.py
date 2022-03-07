from shader_instructions import DataTypes
from shader_node import ShaderNode
from ExtraData.color_atlas import *

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ui_build_width = 0.26

        self.append_text('Struct Definition', size = 0.8)
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

    def add_group(self):
        ui_name = self.append_value_input('Name', 'var')
        ui_type = self.append_drop_down('Type', dict((v,v) for v in DataTypes), self.on_selected, extra_info = ui_name)
        ui_array = self.append_drop_down('', StructDefinitionNode.array_options, on_select = self.on_array_change, extra_info = ui_name, set_to_key = True)
        ui_div = self.append_divider()

        self.move_ui_section(ui_name, self.button, True)
        self.move_ui_section(ui_type, self.button, True)
        self.move_ui_section(ui_array, self.button, True)
        self.move_ui_section(ui_div, self.button, True)
        self.build_back()

        self.section_groups.append([ui_name, ui_type, ui_array, [None], ui_div])


    def on_selected(self, info, key):
        pass

    def on_array_change(self, info, key):
        pass

    

        
        
        

