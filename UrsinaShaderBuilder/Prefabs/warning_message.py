from ursina import *
from ExtraData.extra_models import x_vert

'''
Message that appears that the bottom of the screen and disappears after some time.
'''

class WarningMessage(Entity):

    messages = []
    message_spacing = 0.01
    max_messages = 5

    def __init__(self, message, **kwargs):
        super().__init__(
            parent=camera.ui
            )

        self.color_text = color.white
        self.color_back = color.gray
        self.color_close = color.red

        self.text_scale = 0.8
        self.text_spacing = 0.015
        self.x_size = 0.025

        self.on_click = None

        self.being_removed = False

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.ui_text = Text(message, 
            parent = self,
            x = self.text_spacing,
            z = -0.01,
            color = self.color_text)
        self.ui_text.scale = self.text_scale
        self.ui_text.y = self.ui_text.height * 0.5

        self.ui_close = Entity(parent = self,
            model = Mesh(vertices=x_vert, mode='ngon', static=False), 
            scale = self.x_size * 0.25, 
            collider = 'box',
            z = -0.01,
            x = self.ui_text.width + self.text_spacing * 2,
            origin = (-2,0,0),
            color = self.color_close)
        
        self.height = self.ui_text.height + self.text_spacing * 2
        quadScale = Vec2(self.ui_text.width + self.text_spacing * 3 + self.x_size, self.height)
        self.ui_back = Entity(parent = self, 
            model = Quad(scale = quadScale, radius = quadScale.y * 0.5),
            collider = 'box',
            position = (quadScale.x * 0.5, 0, 0),
            color = self.color_back)

        self.x = -quadScale.x * 0.5

        self.y = window.bottom.y - self.height * 0.5
        self.target = self.y
        
        WarningMessage.messages.append(self)
        for m in WarningMessage.messages:
            m.move_up(self.height + WarningMessage.message_spacing)
        
        for i in range(len(WarningMessage.messages) - WarningMessage.max_messages):
            WarningMessage.messages[i].remove()

        invoke(self.remove, 1, delay = 5)

    
    def input(self, key):
        if key == 'left mouse down':
            if mouse.hovered_entity == self.ui_close:
                self.remove()
            elif mouse.hovered_entity == self.ui_back and self.on_click != None:
                self.on_click()

    def on_destroy(self):
        WarningMessage.messages.remove(self)

    def remove(self, duration = 0.5):
        if self.being_removed: return
        from ursina import curve
        ani = Sequence(
            Func(self.ui_back.fade_out, duration=duration, curve=curve.in_quad),
            Func(self.ui_text.fade_out, duration=duration, curve=curve.in_quad),
            Func(self.ui_close.fade_out, duration=duration, curve=curve.in_quad),
            duration,
            Func(destroy, self))
        ani.start()
        self.being_removed = True

    def move_up(self, amount, duration = 0.5):
        from ursina import curve
        self.target += amount
        ani = Sequence(
            self.animate('y', self.target, duration, curve=curve.in_out_quad)
            )
        ani.start()
        