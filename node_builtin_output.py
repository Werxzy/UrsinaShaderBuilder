from shader_node import ShaderNode

'''
Node represents an output that's built into 

Currently don't know what other outputs need to be represented. 
'''

class BuiltInOutputNode(ShaderNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ui_name = self.append_text('p3d_FragColor', size = 0.8)
        # self.ui_name = self.append_text('color', size = 0.8)

        self.ui_back = self.build_back()

        self.build_connector('vec4', ['vec4'], False, 0.157)
