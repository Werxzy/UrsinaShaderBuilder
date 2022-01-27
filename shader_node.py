from ursina import *
from shader_instructions import *


# color atlas (maybe move to it's own file)
c_node_back = color.rgb(40,40,40)
c_node_dark = color.rgb(25,25,25)
c_text = color.rgb(200,200,200)
c_conn_active = color.rgb(111,211,52)


'''
holds a single instruction and all inputs and puts
will be a child of shader_builder_manager
'''

class ShaderNode(Entity):
    def __init__(self, instruction, **kwargs):
        super().__init__()

        self.instruction = instruction
        self.inputs = []
        self.outputs = []
        self.dragged = False

        self.data_type_common = '' # where all inputs/outputs need to be the same type, like gentype
        self.data_type_set = -1 # nth data type in (gentype, float,)
        # these two need to be checked any time that a connection would be made or removed

        #TODO, line renderer and connecting nodes


        for key, value in kwargs.items():
            setattr(self, key, value)
        
        
        self.ui_build_width = 0.2
        self.ui_build_pos = 0 # to allow appending ui without intersection
        self.ui_spacing = 0.01

        self.ui_name = self.append_text(instruction)
        self.ui_divider1 = self.append_divider()
        self.ui_desc = self.append_text(GLSL[instruction]['description'])
        self.ui_divider2 = self.append_divider()
        self.ui_func = self.append_text(GLSL[instruction]['function'])

        self.ui_back = self.build_back()

        self.build_inputs_outputs_ui()

    def append_divider(self):
        return Entity(parent = self, model = 'quad', position = Vec2(0, self.ui_build_pos), scale = (0.2,0.001), color = c_node_dark)

    def append_text(self, text, text_color = c_text):
        ent = Text(text, parent = self, color = text_color)
        ent.position = Vec2(-ent.width * 0.5, self.ui_build_pos - self.ui_spacing) #adjust based on text width and starting y pos
        self.ui_build_pos -= ent.height + self.ui_spacing * 2 # add the starting y position for next element

        return ent

    def build_back(self):
        quadScale = Vec2(self.ui_build_width, -self.ui_build_pos)
        ent = Entity(parent = self, model = Quad(scale = quadScale, radius=0.02), z = 0.1, origin_y = quadScale.y * 0.5, color = c_node_back, collider='box')
        return ent

    def build_inputs_outputs_ui(self):  
        i = 0.5    
        # build inputs
        for k,v in GLSL[self.instruction]['inputs'].items():
            conn = NodeConnector(parent = self, x_disp = self.ui_build_width * 0.5, yth = i, variable = k, var_types = v, isOutput = False)
            self.inputs.append(conn)
            i += 1
        
        i = 0.5     
        # build output(s)
        for k,v in GLSL[self.instruction]['outputs'].items():
            conn = NodeConnector(parent = self, x_disp = self.ui_build_width * 0.5, yth = i, variable = k, var_types = v)
            self.inputs.append(conn)
            i += 1
    
    def input(self, key):
        if key == 'left mouse down' and self.ui_back.hovered:
            self.dragged = True
        if key == 'left mouse up':
            self.dragged = False

    def update(self):
        if self.dragged:
            self.x += mouse.velocity[0] / self.parent.scale_x
            self.y += mouse.velocity[1] / self.parent.scale_y * window.aspect_ratio

    def on_destroy(self):
        for i in self.inputs:
            i.disconnectAll()
        for o in self.outputs:
            o.disconnectAll()
        

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
        



