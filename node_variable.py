from shader_node import ShaderNode

'''
Node that holds a constant variable.
'''

class ConstantNode(ShaderNode):

    data_type_layouts = {
        'float' : {'x':'float'},
        'vec2' : {'x':'float','y':'float'},
        'vec3' : {'x':'float','y':'float','z':'float'},
        'vec4' : {'x':'float','y':'float','z':'float','w':'float'},

        'int' : {'x':'int'},
        'ivec2' : {'x':'int','y':'int'},
        'ivec3' : {'x':'int','y':'int','z':'int'},
        'ivec4' : {'x':'int','y':'int','z':'int','w':'int'},

        'bool' : {'x':'bool'},
        'bvec2' : {'x':'bool','y':'bool'},
        'bvec3' : {'x':'bool','y':'bool','z':'bool'},
        'bvec4' : {'x':'bool','y':'bool','z':'bool','w':'bool'},
    }


    def __init__(self, data_type, **kwargs):
        super().__init__(**kwargs)

        self.data_type = data_type

        self.ui_name = self.append_text(data_type, size = 0.8)
        self.ui_divider1 = self.append_divider()
        self.values = [self.append_value_input(k, v) for k,v in ConstantNode.data_type_layouts[data_type].items()]

        self.ui_back = self.build_back()

        self.build_connector('', [data_type], True, 0.5)

    def build_shader(self):
        if len(self.values) > 1:
            var = self.data_type + '(' + ','.join([v[1].text for v in self.values]) + ')'
        else:
            var = self.values[0][1].text
        self.outputs[0].set_build_variable(var)

    def save(self):
        return {'data type' : self.data_type, 'values' : [v[1].text for v in self.values]}

    def load(manager, data):
        new_node = ConstantNode(parent = manager, manager = manager, data_type = data['data type'])
        for i in range(len(new_node.values)):
            new_node.values[i][1].text = data['values'][i]
            new_node.values[i][1].render()

        return new_node
