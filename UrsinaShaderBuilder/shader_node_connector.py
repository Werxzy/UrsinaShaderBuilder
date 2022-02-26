from ursina import *
from ExtraData.color_atlas import *
from Prefabs.curve_renderer import CurveRenderer

'''
The input or output for a ShaderNode.
'''

class NodeConnector(Entity):
    
    line_quality = 26
    prepared_node = None
    prepared_line = None

    def __init__(self, x_disp, yth, **kwargs):
        super().__init__()

        from shader_node import ShaderNode
        self.parent:ShaderNode

        self.isOutput = True # if not output, than is input
        self.connections:list[NodeConnector] = []
        self.variable = ''
        self.variable_type:list[str] = []
        self.optional = False
        self.on_connect = None # function called when a connection is completed (on_connect(connecting:bool) -> None)
        self.regex = False

        for key, value in kwargs.items():
            setattr(self, key, value)

        assert not (self.isOutput and self.regex)

        if not self.isOutput:
            self.ui_line = None

        y_spacing = 0.005
        y_height = 0.02 + y_spacing * 2

        self.ui_text = Text(self.variable.replace('_',' ').strip(), parent = self, scale = 0.7, color = c_text)
        self.ui_text.y = -(y_height - self.ui_text.height) * 0.5 - y_height * yth
        
        ui_back_width = y_height * 2.5 + self.ui_text.width
        self.ui_back = Entity(parent = self, 
            model = Quad(scale = Vec2(ui_back_width, y_height + 0.0003), 
                radius = y_height * 0.5), 
            z = 0.2, 
            y = -y_height * 0.5 - y_height * yth - 0.0003,
            color = c_node_dark,
            collider = 'box')

        self.ui_dot = Entity(parent = self, 
            model = 'circle',
            scale = y_height * 0.8,
            y = -y_height * 0.5 - y_height * yth,
            color = c_node_back)

        if self.optional:
            self.ui_dot2 = Entity(parent = self.ui_dot, 
                model = 'circle',
                scale = 0.7,
                z = -0.01,
                color = c_node_dark)

        if self.isOutput: # right size
            self.ui_text.x = x_disp + 0.01
            self.ui_back.x = x_disp + ui_back_width * 0.5 - y_height
            self.ui_dot.x = self.ui_back.x + ui_back_width * 0.5 - y_height * 0.5

        else: # left side
            self.ui_text.x = - x_disp - self.ui_text.width - 0.01
            self.ui_back.x = - x_disp - ui_back_width * 0.5 + y_height
            self.ui_dot.x = self.ui_back.x - ui_back_width * 0.5 + y_height * 0.5
            

    def input(self, key):
        if key == 'left mouse down':
            if self.ui_back.hovered:
                if NodeConnector.prepared_node:
                    self.connect(NodeConnector.prepared_node)
                    self.destroy_prepared_line()
                else:
                    NodeConnector.prepared_node = self
                    NodeConnector.prepared_line = CurveRenderer(length = 6, parent = self, color = c_conn_active)
                    self.update_prepared_line()
                    
            elif NodeConnector.prepared_node == self and mouse.hovered_entity is None:
                self.destroy_prepared_line()

        if key == 'right mouse down' and self.ui_back.hovered:
            self.disconnect_all()

    def update(self):
        if NodeConnector.prepared_node == self:
            if mouse.velocity[0] != 0 or mouse.velocity[1] != 0:
                self.update_prepared_line()

    def on_destroy(self):
        self.disconnect_all()
    
    
    # announce that a connection should be made and check if one can be
    def connect(self, connector):
        if not isinstance(connector, NodeConnector): return
        if self.isOutput == connector.isOutput: return # connectors cannot connect to the same type
        if self.connections.count(connector) != 0: return # if these two aren't already connected to eachother
        if len(self._matching_connections(connector)) == 0: return # no matching data types

        # check if there is a loop
        check = False
        if self.isOutput: check = connector._propagate_check(self)
        else: check = self._propagate_check(connector)
        if not check: return # loop detected

        # applies the connection
        self._apply_connection(connector)
        connector._apply_connection(self)

        if self.isOutput: self.parent.update_connections()
        else: connector.parent.update_connections()

    # announce that a connection is to be undone
    def disconnect(self, connector):
        if not isinstance(connector, NodeConnector): return

        try:
            i = self.connections.index(connector)
            self._apply_disconnection(i)
            connector._apply_disconnection(self)
            if not self.isOutput: self.parent.update_connections()
            else: connector.parent.update_connections()
        except:
            print('error???')
            pass # no connection found

    def disconnect_all(self):
        for _ in range(len(self.connections)):
            c = self.connections[0]
            c._apply_disconnection(self)
            self._apply_disconnection(0)
            if self.isOutput: 
                c.parent.update_connections()
            
        if not self.isOutput: self.parent.update_connections()


    #returns list of pars of matching variable types's indicies (self, connector)
    def _matching_connections(self, connector):
        if self.regex: return self.regex_matches(self.variable_type, connector.variable_type, False)
        if connector.regex: return self.regex_matches(connector.variable_type, self.variable_type, True)

        matches = []
        self_range = range(len(self.variable_type))
        conn_range = range(len(connector.variable_type))
        for i in self_range:
            for j in conn_range:
                if self.variable_type[i] == connector.variable_type[j]:
                    matches.append((i, j))
        return matches

    def regex_matches(self, a, b, swap):
        import re
        matches = []
        self_range = range(len(a))
        conn_range = range(len(b))
        for i in self_range:
            for j in conn_range:
                if re.match(a[i], b[j]):
                    matches.append((i, j) if not swap else (j, i))
        return matches

    def regex_matches_single(self, a, b, pos):
        import re
        matches = []
        conn_range = range(len(a))
        for i in conn_range:
            if re.match(a[i], b) != None:
                matches.append((i, pos))
        return matches

    # return list of pares of matching variables types's indicies, with respect to nodes' set types (self, connector)
    def get_possible_data_types(self):
        if self.isOutput: return [] # should only be called on inputs
        if len(self.connections) == 0: # any type is possible since there's no connection
            l = len(self.variable_type)
            return list(zip(range(l), l * [-1])) 
        if self.connections[0].parent.data_type_set == -1: return self._matching_connections(self.connections[0])

        self_range = range(len(self.variable_type))
        set_pos = self.connections[0].parent.data_type_set
        var_type = self.connections[0].variable_type[set_pos]

        if self.regex: 
            return self.regex_matches_single(self.variable_type, var_type, set_pos)

        matches = []
        for i in self_range:
            if self.variable_type[i] == var_type:
                matches.append((i, set_pos))
        return matches

    #returns if the connection can go through or not and maybe what type all the connections should take
    def _propagate_check(self, start):
        nodes_to_check:list[NodeConnector] = [start]

        while len(nodes_to_check) > 0:
            conn = nodes_to_check.pop(0)

            if conn.parent == self.parent: # if an infinite loop is detected
                return False

            for i in conn.parent.inputs:
                nodes_to_check += i.connections

        return True

    # apply the connection and any changes required by the conneciton being made 
    # (the apply functions are meant to remove any cyclical function calling)
    def _apply_connection(self, connector):
        if self.isOutput:
            self.connections.append(connector)

        else:
            if len(self.connections) > 0:
                self.connections[0]._apply_disconnection(self)
                self._apply_disconnection(0)
            self.connections.append(connector)

            self.ui_line = CurveRenderer(length = NodeConnector.line_quality, parent = self, color = c_conn_active)
            self.update_line()

        self.ui_dot.color = c_conn_active
        if self.optional: self.ui_dot2.visible = False

        if self.on_connect != None:
            self.on_connect(True)

    # apply the disconnection and any changes required by the conneciton being made
    def _apply_disconnection(self, connector):
        if isinstance(connector, int):
            connector = self.connections.pop(connector)
        else:
            self.connections.remove(connector)

        if not self.isOutput and self.ui_line:
            destroy(self.ui_line)
            self.ui_line = None
    
        if len(self.connections) == 0:
            self.ui_dot.color = c_node_back
            if self.optional: self.ui_dot2.visible = True

        self.parent.disconnection(self)

        if self.on_connect != None:
            self.on_connect(False)

    def any_connected(self):
        return len(self.connections) > 0
        

    def update_prepared_line(self):
        start = Vec3(self.ui_dot.position)
        end = Vec3(mouse.position - self.get_position(camera.ui)) / self.parent.parent.scale
        NodeConnector.prepared_line.set_curve([start, end])
    
    def destroy_prepared_line(self):
        NodeConnector.prepared_node = None
        destroy(NodeConnector.prepared_line)
        NodeConnector.prepared_line = None


    def connector_pos(self):
        return Vec3(self.ui_dot.get_position(camera.ui))

    def update_line(self):
        if self.isOutput:
            for i in self.connections:
                i.update_line()
            return
        if self.ui_line is None: return

        start = self.ui_dot.position
        end = Vec3(self.connections[0].connector_pos() - self.connector_pos()) / self.parent.parent.scale + self.ui_dot.position

        bend = min((start - end).length() * 0.5, 0.1)

        start_bend = start - Vec3(bend, 0, 0)
        end_bend = end + Vec3(bend, 0, 0)

        # path = [start, start_bend, start_bend, end_bend, end_bend, end]
        path = [start, start_bend, end_bend, end]
        self.ui_line.set_curve(path)


# - - - shader builder functions - - -

    # Clears the used variable.
    def clear_build_variable(self):
        self.build_variable = None
        self.build_use_count = 0

    # Returns the variable name.
    # If the number of expected uses is reached, then flag it as being no longer used.
    def get_build_variable(self, decrement = True):
        if not self.isOutput:
            return self.connections[0].get_build_variable(decrement)

        if decrement:
            self.build_use_count -= 1
            if self.build_use_count == 0:
                self.parent.manager.finished_variable(self.get_variable_type(), self.build_variable)

        return self.build_variable
    
    # Returns the type of the variable based on its node's mode.
    def get_variable_type(self):
        if self.parent.data_type_set == -1:
            print_warning('No type specified.')
            return ''
        return self.variable_type[self.parent.data_type_set]

    # Creates the build variable and returns the variable assignment version
    # if there is a free variable to use
    #   _vec3_0
    # otherwise include the type
    #   vec3 _vec3_0
    def prepare_build_variable(self, uses = 0):
        v = self.parent.manager.get_variable(self.get_variable_type())
        self.build_variable = v[0]
        self.build_use_count = uses if uses > 0 else len(self.connections)
        return v[1]

    # Sets the variable to a custom output. (usually a constant or global variable)
    def set_build_variable(self, value):
        self.build_variable = value
        self.build_use_count = -1