from shader_node import ShaderNode

'''
Node represents an output that's built into 

Currently don't know what other outputs need to be represented. 
'''

class BuiltInOutputNode(ShaderNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.variable_name = 'p3d_FragColor'
        #self.variable_name = 'color'

        self.ui_name = self.append_text(self.variable_name, size = 0.8)
        
        self.ui_back = self.build_back()

        self.build_connector('vec4', ['vec4'], False, 0.157)
