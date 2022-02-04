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
        self.ui_build_pos -= self.ui_spacing

        self.ui_back = self.build_back()

        self.build_connector('', [data_type], True, 0.5)
