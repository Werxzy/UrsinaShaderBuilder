from ursina import destroy
from shader_node_connector import NodeConnector
from shader_node import ShaderNode

'''
Node that creates a 1 dimensional array with given variables that all the same data type.
'''

class ArrayCreateFilledNode(ShaderNode):

    # considers all possible combinations of supported datatypes
    allowed_data_types = [
        '^(float|int|bool|[iub]?vec[234]|mat[234](x[234])?)(\\[\\d+\\])*$'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.append_text('Create filled Array')
        ui_divider = self.append_divider()
        self.append_text('Creates an array\n from given variables.', size = 0.7)
        ui_divider[0].scale_x = self.ui_build_width
        self.build_back()

        self.update_check = self.update_data_type
        
        self.last_disconnect = (None,0)

        self.build_connector('', ArrayCreateFilledNode.allowed_data_types, False, 0.5, optional = True, regex = True, on_connect = self.new_connection)
    
    # last connector is connected to. adjuste it and
    def new_connection(self, **kwargs):
        if kwargs['connected']:
            kwargs['connector'].on_connect = self.existing_connection
            kwargs['connector'].regex = False

            self.build_connector('', ArrayCreateFilledNode.allowed_data_types, False, len(self.inputs) + 0.5, optional = True, regex = True, on_connect = self.new_connection)
            self.update_data_type(True)

    def existing_connection(self, **kwargs):
        if kwargs['new_connection']:
            if not kwargs['connected']:
                conn = kwargs['connector']
                self.last_disconnect = (conn, self.inputs.index(conn))
                conn.enabled = False
                self.inputs.remove(conn)

            elif kwargs['connector'] == self.last_disconnect[0]:
                self.inputs.insert(self.last_disconnect[1], self.last_disconnect[0])
                self.last_disconnect[0].enabled = True
                self.last_disconnect = (None,0)

            self.update_data_type(True)

    def update_data_type(self, update_conn = False):
        need_to_update = False
        if len(self.inputs) > 1:
            to_disconnect:list[NodeConnector] = []
            data_types = set(self.inputs[0].connections[0].get_usable_variable_types())  

            if len(self.inputs) > 2:
                for i in self.inputs[1:-1]:
                    overlap = data_types & set(i.connections[0].get_usable_variable_types())

                    if len(overlap) == 0:
                        to_disconnect.append(i)
                    else:
                        data_types = overlap
            
            for i in to_disconnect:
                self.inputs.remove(i)
                destroy(i)
                
            for i in self.inputs:
                i.variable_type = list(data_types)
                i.regex = False

            output_types = [d + '[' + str(len(self.inputs) - 1) + ']' for d in data_types]
            if len(self.outputs) == 0:
                self.build_connector('', output_types, True, 0.5)
            else:
                if set(self.outputs[0].variable_type) != set(output_types):
                    self.outputs[0].variable_type = output_types
                    need_to_update = True

        else:
            self.inputs[0].variable_type = ArrayCreateFilledNode.allowed_data_types
            self.inputs[0].regex = True
            if len(self.outputs) > 0:
                destroy(self.outputs[0])
                self.outputs.clear()
                need_to_update = True

        self.update_connector_positions()
        if need_to_update and update_conn:
            self.update_connections()

    def update_connector_positions(self):
        for y, i in enumerate(self.inputs):
            i.set_y(y + 0.5)

    def build_shader(self):
        v = self.outputs[0].prepare_build_variable() + ' = ' + self.outputs[0].get_variable_type() + '('
        v += ', '.join([i.get_build_variable() for i in self.inputs[:-1]])
        v += ');'
        self.manager.build_shader_append('main', v)

    def load(manager, data):
        return ArrayCreateFilledNode(parent = manager, manager = manager)
