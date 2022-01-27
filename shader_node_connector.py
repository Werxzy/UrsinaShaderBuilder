from ursina import *
from color_atlas import *


'''
an input or output for a node
'''

class NodeConnector(Entity):
    def __init__(self, x_disp, yth, **kwargs):
        super().__init__()

        self.isOutput = True # if not output, than is input
        self.connections = []
        self.variable = ''
        self.var_types = ('',)

        for key, value in kwargs.items():
            setattr(self, key, value)

        y_spacing = 0.005
        y_height = 0.02 + y_spacing * 2

        self.ui_text = Text(self.variable, parent = self, y = -y_spacing - y_height * yth, color = c_text)
        
        ui_back_width = y_height * 2.5 + self.ui_text.width
        self.ui_back = Entity(parent = self, 
            model = Quad(scale = Vec2(ui_back_width, y_height + 0.0003), 
                radius = y_height * 0.5), 
            z = 0.2, 
            y = -y_height * 0.5 - y_height * yth - 0.0003,
            color = c_node_dark)

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
            

    def connector_pos(self):
        return self.ui_dot.world_position(camera.ui) # !!! this may be incorrect

    # announce that a connection should be made
    def connect(self, connector):
        if not isinstance(connector, NodeConnector): return
        if self.isOutput == connector.isOutput: return #inputs and outputs cannot connect
            
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

    def disconnectAll(self):
        for c in self.connections:
            self._apply_disconnection(c)
            c._apply_disconnection(self)

    # apply the connection and any changes required by the conneciton being made 
    # (the apply functions are meant to remove any cyclical function calling)
    def _apply_connection(self, connector):
        if self.isOutput:
            self.connections.append(connector)
            #add new line?

        else:
            if len(self.connections) > 0:
                self._apply_disconnection(self, connector)
            self.connections.append(connector)

    # apply the disconnection and any changes required by the conneciton being made
    def _apply_disconnection(self, connector):
        if isinstance(connector, int):
            connector = self.connections.pop(connector)
        else:
            self.connections.remove(connector)

        # remove line

    def any_connected(self):
        return self.connections.count() > 0
        