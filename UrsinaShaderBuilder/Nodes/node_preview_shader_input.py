from ursina import *
from pathlib import Path
from shader_instructions import DataTypeLayouts
from shader_node import ShaderNode

'''
Not actually a shader node, but helps set values for previewing changes in the shader.
'''

class PreviewShaderInputNode(ShaderNode):

    def __init__(self, input_list:dict, preview_entity:Entity, **kwargs):
        super().__init__(parent = camera.ui, draggable = False, **kwargs)

        self.shader_inputs = dict()
        self.preview_entity = preview_entity

        self.append_text('Shader Inputs')
        self.append_divider(3)
        self.append_text('Model', size = 0.8)
        self.append_drop_down(
            '', 
            {
                'load model' : '!load file!',
                'sphere' : 'sphere',
                'cube' : 'cube',
                'plane' : 'plane',
                'cube uv top' : 'cube_uv_top',
                'icosphere' : 'icosphere',
                'quad' : 'quad',
                'circle' : 'circle',
            },
            self.update_shader_model, 
            start_value = 'sphere')

        for k,v in input_list.items():
            data_type = v['data type']

            self.append_divider()
            self.append_text(k, size = 0.8)
            self.append_text(data_type, size = 0.5)

            if data_type in DataTypeLayouts.keys():
                self.shader_inputs.update({
                    k : {
                        'data_type' : data_type,
                        'inputs' : [self.append_value_input(k2, v2, on_change = self.update_shader_input, on_change_att = str(k)) for k2,v2 in DataTypeLayouts[data_type].items()]
                    }
                })
            elif data_type == 'sampler2D':
                self.append_drop_down(
                    '', 
                    {
                        'load texture' : '!load file!',
                        'None' : 'None',
                        'brick' : 'brick',
                        'circle' : 'circle',
                        'grass' : 'grass',
                        'white_cube' : 'white_cube',
                        'noise' : 'noise',
                        'radial_gradient' : 'radial_gradient',
                        'reflection_map_3' : 'reflection_map_3',
                        'shore' : 'shore',
                        'sky_default' : 'sky_default',
                        'sky_sunset' : 'sky_sunset',
                        'horizontal_gradient' : 'horizontal_gradient',
                        'vertical_gradient' : 'vertical_gradient',
                        'rainbow' : 'rainbow',
                        'vignette' : 'vignette',
                    },
                    self.update_shader_sampler2D, 
                    start_value = 'None', 
                    extra_info = k)
            else:
                self.append_text('Type not supported yet.', size = 0.5)

        self.ui_back = self.build_back()
        
        self.x = window.left.x + self.ui_build_width * 0.5 + self.ui_spacing
        
        max = window.bottom.y - self.ui_build_pos + self.ui_spacing * 2
        min = window.top.y - self.ui_spacing * 5
        if max > min:
            self.add_script(Scrollable(min = min, max = max))
        self.y = min

    def update_shader_input(self, name):
        data_type = self.shader_inputs[name]['data_type']
        inp = self.shader_inputs[name]['inputs']

        if data_type in DataTypeLayouts.keys():
            vals = ()

            for i in inp:
                vals += ((i[1].text == 'true') if data_type[0] == 'b' else float(i[1].text),)
                
            self.preview_entity.set_shader_input(name, vals)


    def update_shader_sampler2D(self, name, tex): 
        if tex == 'None':
            self.preview_entity.texture = None
        if tex == '!load file!':
            from ursina.texture_importer import file_types
            p = self.manager.load_file(file_types)
            if p != '': tex = Texture(p)
            else: return

        if isinstance(tex, str):
            tex = load_texture(tex)

        if name == 'p3d_Texture0':
            self.preview_entity.texture = tex
        else:
            self.preview_entity.set_shader_input(name, tex)

    def update_shader_model(self, mesh): 
        if mesh == '!load file!':
            p = self.manager.load_file(['.bam', '.ursinamesh', '.obj', '.glb', '.gltf', '.blend'])
            if p != '':
                p = p.split('/')
                mesh = load_model(p[-1], Path('/'.join(p[:-1])))
            else: return

        if isinstance(mesh, str):
            mesh = load_model(mesh)

        self.preview_entity.model = mesh
        self.preview_entity.origin = (0,0,0)
