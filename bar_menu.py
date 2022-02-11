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
        self.colliders = []
        start_x = 0
        self._height = 0
        for key in self.options.keys():
            text = Text(key, parent = self, position = Vec3(start_x + self.text_spacing.x, -self.text_spacing.y, -0.1), scale = self.text_scale, color = self.color_text)
            if start_x > 0:
                Entity(parent = self, position = Vec3(start_x, 0, -0.1), scale = Vec3(0.001, self._height, 1), origin_y = 0.5, model = 'quad', color = self.color_divider)
            else:
                self._height = text.height + self.text_spacing.y * 2
            
            width = text.width + self.text_spacing.x * 2

            collider = Entity(parent = self, x = start_x, scale = Vec3(width, self._height, 1), origin = Vec3(-0.5,0.5,0), model = 'quad', collider = 'box', visible = False)

            start_x += width
            self.texts.append(text)
            self.colliders.append(collider)

        self.back = Entity(parent = self, scale = Vec3(window.aspect_ratio, self._height, 1), origin = Vec3(-0.5,0.5,0), model = 'quad', color = self.color_back)
    
    def input(self, key):
        if key == 'left mouse down':
            if mouse.hovered_entity in self.colliders:
                i = self.colliders.index(mouse.hovered_entity)
                op = self.options[self.texts[i].text]
                if isinstance(op, dict):
                    print(op) #TODO dropdown menu here
                else:
                    self.on_selected(op)

    def update(self):
        pass