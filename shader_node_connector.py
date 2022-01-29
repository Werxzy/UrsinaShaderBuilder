from ursina import *
from color_atlas import *
from curve_renderer import CurveRenderer

'''
an input or output for a node
'''

class NodeConnector(Entity):

    prepared_node = None
    prepared_line = None

    def __init__(self, x_disp, yth, **kwargs):
        super().__init__()

        self.isOutput = True # if not output, than is input
        self.connections = []
        self.variable = ''
        self.var_types = ('',)

        for key, value in kwargs.items():
            setattr(self, key, value)

        if not self.isOutput:
            self.ui_line = None

        y_spacing = 0.005
        y_height = 0.02 + y_spacing * 2

        self.ui_text = Text(self.variable, parent = self, y = -y_spacing - y_height * yth, color = c_text)
        
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
    
    
    # announce that a connection should be made and check if one can be
    def connect(self, connector):
        if not isinstance(connector, NodeConnector): return
        if self.isOutput == connector.isOutput: return # connectors cannot connect to the same type

        #TODO more checks for if they can connect
        check = self._propagate_check(connector)
        print(check)
        if not check[0]: return # loop detected
            
        if self.connections.count(connector) == 0: #if these two aren't already connected to eachother
            self._apply_connection(connector)
            connector._apply_connection(self)

    # announce that a connection is to be undone
    def disconnect(self, connector):
        if not isinstance(connector, NodeConnector): return

        try:
            i = self.connections.index(connector)
            self._apply_disconnection(i)
            connector._apply_disconnection(self)
        except:
            pass # no connection found

    def disconnect_all(self):
        for i in range(len(self.connections)):
            self.connections[0]._apply_disconnection(self)
            self._apply_disconnection(0)


    #returns if the connection can go through or not and maybe what type all the connections should take
    def _propagate_check(self, start):
        backwards = start.isOutput
        nodes_to_check = [start]

        while len(nodes_to_check) > 0:
            conn = nodes_to_check.pop(0)

            if conn.parent == self.parent: # if an infinite loop is detected
                return (False, '')

            if backwards:
                for i in conn.parent.inputs:
                    nodes_to_check += i.connections
            else:
                for o in conn.parent.outputs:
                    nodes_to_check += o.connections

            

        return (True, '')

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

            self.ui_line = CurveRenderer(length = 26, parent = self, color = c_conn_active)
            self.update_line()

        self.ui_dot.color = c_conn_active

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

    def any_connected(self):
        return self.connections.count() > 0
        

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