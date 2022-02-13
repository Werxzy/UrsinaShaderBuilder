from shader_node import ShaderNode

'''
Node represents an output that's built into 

Currently don't know what other outputs need to be represented. 
'''

class BuiltInOutputNode(ShaderNode):

    # [0] = in | out | uniform
    # [1] = data type
    # [2:] = tags 
    #       vertex: can be used in vertex shaders
    #       fragment: can be used in fragment shaders
    #       numerable: there can be multiple versions

    build_in_attributes = {
        'p3d_Vertex': ('in', 'vec4', 'vertex'),
        'p3d_Normal': ('in', 'vec3', 'vertex'),
        'p3d_Color': ('in', 'vec4', 'vertex'),

        'p3d_MultiTexCoord0': ('in', 'vec2', 'vertex'),
        'p3d_MultiTexCoord1': ('in', 'vec2', 'vertex'),
        'p3d_MultiTexCoord2': ('in', 'vec2', 'vertex'),
        # 'p3d_MultiTexCoord#': ('in', 'vec2', 'vertex', numerable),

        'p3d_Binormal0': ('in', 'vec3', 'vertex'),
        'p3d_Binormal1': ('in', 'vec3', 'vertex'),
        'p3d_Binormal2': ('in', 'vec3', 'vertex'),

        'p3d_Tangent0': ('in', 'vec3', 'vertex'),
        'p3d_Tangent1': ('in', 'vec3', 'vertex'),
        'p3d_Tangent2': ('in', 'vec3', 'vertex'),

        # 'transform_weight': ('in', 'vec4', 'vertex'),
        # 'transform_index': ('in', 'uvec4', 'vertex'),


        'p3d_ModelViewProjectionMatrix': ('uniform', 'mat4', 'vertex', 'fragment'),

        'p3d_ModelViewMatrix': ('uniform', 'mat4', 'vertex', 'fragment'),
        'p3d_ProjectionMatrix': ('uniform', 'mat4', 'vertex', 'fragment'),

        'p3d_NormalMatrix': ('uniform', 'mat3', 'vertex', 'fragment'),

        'p3d_ModelMatrix': ('uniform', 'mat4', 'vertex', 'fragment'),
        'p3d_ViewMatrix': ('uniform', 'mat4', 'vertex', 'fragment'),
        'p3d_ViewProjectionMatrix': ('uniform', 'mat4', 'vertex', 'fragment'),

        'p3d_ProjectionMatrixInverse': ('uniform', 'mat4', 'vertex', 'fragment'),
        'p3d_ProjectionMatrixTranspose': ('uniform', 'mat4', 'vertex', 'fragment'),
        'p3d_ModelViewMatrixInverseTranspose': ('uniform', 'mat4', 'vertex', 'fragment'),

        # 'p3d_Texture0': ('uniform', 'sampler2D', 'vertex', 'fragment'),


        'gl_Position': ('out', 'vec4', 'vertex'),

        'gl_FragCoord': ('in', 'vec4', 'fragment'),
        'gl_FrontFacing': ('in', 'bool', 'fragment'),
        'gl_PointCoord': ('in', 'vec2', 'fragment'),

        'gl_FragDepth': ('out', 'vec2', 'fragment'),
        'p3d_FragColor': ('out', 'vec4', 'fragment'),



    }

    def __init__(self, variable = 'p3d_FragColor', **kwargs):
        super().__init__(**kwargs)

        self.variable = variable
        att = BuiltInOutputNode.build_in_attributes[variable]

        self.ui_name = self.append_text(self.variable, size = 0.8)
        
        self.ui_back = self.build_back()

        self.main_connector = self.build_connector(att[1], [att[1]], 'out' != att[0], 0.157)

    def valid_mode(self, mode):
        m = BuiltInOutputNode.build_in_attributes[self.variable]
        return (mode in m) or ('all' in m)

    def build_shader(self):
        att = BuiltInOutputNode.build_in_attributes[self.variable]
        v1 = att[0] + ' ' + att[1] + ' ' + self.variable + ';'
        self.manager.build_shader_append('inout', v1)

        if att[0] == 'out':
            v2 = self.variable + ' = ' + self.main_connector.get_build_variable() + ';'
            self.manager.build_shader_append('main', v2)
 
        else:
            self.main_connector.set_build_variable(self.variable)

