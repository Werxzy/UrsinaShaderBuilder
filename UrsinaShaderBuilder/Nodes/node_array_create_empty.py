from ursina import destroy
from shader_instructions import DataTypes
from shader_node import ShaderNode

'''
Node for creating an empty array of a given size and data type.
'''

class ArrayCreateEmptyNode(ShaderNode):

    array_options = {
        '1D Array' : 1,
        '2D Array' : 2,
        '3D Array' : 3,
    }

    def __init__(self, data_type = '', dimensions = '', **kwargs):
        super().__init__(**kwargs)
        
        self.append_text('Create Empty Array')
        ui_divider = self.append_divider()
        self.append_text('Creates an empty array\n of a given size.', size = 0.7)
        ui_divider.scale_x = self.ui_build_width

        self.ui_type = self.append_drop_down('Type', dict((v,v) for v in DataTypes), self.on_selected)
        if data_type != '': self.ui_type[1].text = data_type
        
        self.ui_array_type = self.append_drop_down('', ArrayCreateEmptyNode.array_options, 
            start_value = dimensions if dimensions != '' else '1D Array',
            on_select = self.on_array_change,
            set_to_key = True)

        self.ui_back_start_pos = self.ui_build_pos
        self.ui_back = self.build_back()
        self.ui_dimensions = []

        self.main_connector = self.build_connector('', [self.ui_type[1].text], True, 0.5)

        if dimensions == '':
            self.on_array_change(1)
        else:
            self.on_array_change(ArrayCreateEmptyNode.array_options[dimensions])

    def on_array_change(self, option, replace_vals = []):
        old_vals = []
        for ui in self.ui_dimensions:
            old_vals.append(ui[1].text)
            for sub in ui:
                destroy(sub)
        self.ui_dimensions.clear()
        destroy(self.ui_back)
        self.ui_build_pos = self.ui_back_start_pos

        if len(replace_vals) > 0:
            old_vals = replace_vals

        for i in range(option):
            self.ui_dimensions.append(self.append_value_input('[]'*i + '['+ 'xyzw'[i] +']', 'uint', on_change = self.update_data_type))
            if i < len(old_vals):
                self.ui_dimensions[i][1].text = old_vals[i]
                self.ui_dimensions[i][1].render(False)

        self.ui_back = self.build_back()

        self.update_data_type()

    def on_selected(self, option):
        self.main_connector.variable_type = [option]
        self.update_data_type()

    def update_data_type(self, var = 'required'):
        ind = self.main_connector.variable_type[0].find('[')
        if ind == -1:
            data_type = self.main_connector.variable_type[0]
        else:
            data_type = self.main_connector.variable_type[0][:ind]
        
        for ui in self.ui_dimensions:
            data_type += '[' + ui[1].text + ']'

        self.main_connector.variable_type = [data_type]
        self.update_connections()
    
    def build_shader(self):
        self.manager.build_shader_append('main', self.main_connector.prepare_build_variable() + ';', False)

    def save(self):
        return {'data type' : self.ui_type[1].text, 
            'array type' : self.ui_array_type[1].text,
            'array dimensions' : [ui[1].text for ui in self.ui_dimensions]}

    def load(manager, data):
        new_node = ArrayCreateEmptyNode(parent = manager, manager = manager, data_type = data['data type'], dimensions = data['array type'])
        new_node.on_array_change(ArrayCreateEmptyNode.array_options[data['array type']], data['array dimensions'])

        return new_node
