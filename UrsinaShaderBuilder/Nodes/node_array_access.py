from ursina import destroy
from shader_node_connector import NodeConnector
from shader_node import ShaderNode

'''
Node for accessing a specific element in the array
'''

class ArrayAccessNode(ShaderNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.append_text('Array Access')
        ui_divider = self.append_divider()
        self.append_text('Get a single element\nof a given array', size = 0.7)
        self.ui_back = self.build_back()
        ui_divider.scale_x = self.ui_build_width

        self.array_input = self.build_connector('Array', ['.+(\\[\\d+\\])+'], False, 0.5, on_connect = self.on_connect, regex = True)

        self.index_inputs:list[NodeConnector] = []

    def on_connect(self, connecting):
        if connecting:
            variable = self.array_input.connections[0].get_variable_type()
            size = variable.count('[')
            data_type = variable[:variable.find('[')]
        else:
            size = 0

        if size > len(self.index_inputs):
            for i in range(len(self.index_inputs),size):
                self.index_inputs.append(self.build_connector('xyzw'[i], ['^u?int$'], False, i + 1.5, optional = True, regex = True))
        
        while len(self.index_inputs) > size:
            conn = self.index_inputs.pop()
            self.inputs.remove(conn)
            destroy(conn)

        if connecting:
            if len(self.outputs) > 0 and self.outputs[0].variable != data_type:
                destroy(self.outputs.pop())
            if len(self.outputs) == 0:
                self.build_connector(data_type, [data_type], True, 0.5)

        elif len(self.outputs) > 0:
            destroy(self.outputs.pop())

    def build_shader(self):
        v = self.inputs[0].get_build_variable()
        indices = ''.join(['[' + (i.get_build_variable() if i.any_connected() else '0') + ']' for i in self.index_inputs])
        v2 = self.outputs[0].prepare_build_variable()

        inst = v2 + ' = ' + v + indices + ';'
        self.manager.build_shader_append('main', inst)
    

    def load(manager, data):
        return ArrayAccessNode(parent = manager, manager = manager)
