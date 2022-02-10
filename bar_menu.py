from ursina import *


class BarMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent = camera.ui
            )
        self.position = window.top_left
        
        self.options = {'File':{'New':'New', 'Open':'Open', 'Save':'Save'}, 'Edit':{'Undo':'Undo', 'Redo':'Redo'}}

        self.color_back = hsv(0,0,0.1)
        self.color_text = hsv(0,0,0.7)
        self.color_divider = hsv(0,0,0.3)

        self.text_scale = 0.8
        self.text_spacing = Vec2(0.02,0.01)

        self.on_selected = None

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.texts = []
        start_x = 0
        height = 0
        for key in self.options.keys():
            text = Text(key, parent = self, position = Vec3(start_x + self.text_spacing.x, -self.text_spacing.y, -0.1), scale = self.text_scale, color = self.color_text)
            if start_x > 0:
                Entity(parent = self, position = Vec3(start_x, 0, -0.1), scale = Vec3(0.001, height, 1), origin_y = 0.5, model = 'quad', color = self.color_divider)
            else:
                height = text.height + self.text_spacing.y * 2
            start_x += text.width + self.text_spacing.x * 2
            self.texts.append(text)

        self.back = Entity(parent = self, scale = Vec3(window.aspect_ratio, height, 1), origin = Vec3(-0.5,0.5,0), model = 'quad', color = self.color_back)