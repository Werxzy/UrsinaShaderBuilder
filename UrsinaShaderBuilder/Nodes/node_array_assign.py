from ursina import destroy
from shader_node_connector import NodeConnector
from shader_node import ShaderNode

'''
Node for assigning a value to the array
'''

class ArrayAssignNode(ShaderNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.append_text('Array Assign')
        ui_divider = self.append_divider()
        self.append_text('Set a value in\n a given array.', size = 0.7)
        self.ui_back = self.build_back()
        ui_divider.scale_x = self.ui_build_width

        self.array_input = self.build_connector('Array', ['.+(\\[\\d+\\])+'], False, 0.5, on_connect = self.on_connect, regex = True)

        self.assign_input = None
        self.index_inputs:list[NodeConnector] = []

    def on_connect(self, connecting):
        if connecting:
            data_type = self.array_input.connections[0].get_variable_type()
            size = data_type.count('[')
            assign_data_type = data_type[:data_type.find('[')]
        else:
            size = 0

        if size > len(self.index_inputs):
            for i in range(len(self.index_inputs),size):
                self.index_inputs.append(self.build_connector('xyzw'[i], ['^u?int$'], False, i + 2.5, optional = True, regex = True))
        
        while len(self.index_inputs) > size:
            conn = self.index_inputs.pop()
            self.inputs.remove(conn)
            destroy(conn)

        if connecting:
            if len(self.outputs) == 0:
                self.build_connector('Array', [data_type], True, 0.5)
                self.assign_input = self.build_connector(assign_data_type, [assign_data_type], False, 1.5)
            
            elif self.outputs[0].variable_type[0] != data_type:
                self.outputs[0].variable_type[0] = data_type
                if assign_data_type != self.assign_input.variable_type[0]:
                    destroy(self.assign_input)
                    self.assign_input = self.build_connector(assign_data_type, [assign_data_type], False, 1.5)
                         
        elif len(self.outputs) > 0:
            self.inputs.remove(self.assign_input)
            destroy(self.assign_input)
            self.assign_input = None
            destroy(self.outputs.pop())

    def build_shader(self):
        v = self.inputs[0].get_build_variable()
        indices = ''.join(['[' + (i.get_build_variable() if i.any_connected() else '0') + ']' for i in self.index_inputs])
        v2 = self.assign_input.get_build_variable()

        self.outputs[0].set_build_variable(v)

        inst = v + indices + ' = ' + v2 + ';'
        self.manager.build_shader_append('main', inst)

    def load(manager, data):
        return ArrayAssignNode(parent = manager, manager = manager)