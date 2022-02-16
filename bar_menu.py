from ursina import *
from extra_models import right_arrow_vert


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
        self.drop_down = None

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.texts:list[Text] = []
        self.colliders:list[Entity] = []
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
                destroy(self.drop_down)

                i = self.colliders.index(mouse.hovered_entity)
                op = self.options[self.texts[i].text]
                if isinstance(op, dict):
                    self.drop_down = BarMenuDropDown(parent = self, position = self.colliders[i].position + Vec3(0,-self._height,0), options = op)
                else:
                    self.on_selected(op)
            
            elif self.drop_down != None:
                if not self.drop_down.is_hovered():
                    destroy(self.drop_down)

    def clear_options(self):
        destroy(self.drop_down)


class BarMenuDropDown(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.options = {}

        self.color_back = hsv(0,0,0.1)
        self.color_text = hsv(0,0,0.7)
        self.color_divider = hsv(0,0,0.3)

        self.text_scale = 0.8
        self.text_spacing = Vec2(0.02,0.006)

        self.drop_down = None

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.texts:list[Text] = []
        self.colliders:list[Entity] = []
        start_y = 0
        self._max_width = 0
        for key in self.options.keys():
            text = Text(key, parent = self, position = Vec3(self.text_spacing.x, start_y - self.text_spacing.y, -0.1), scale = self.text_scale, color = self.color_text)
            
            height = text.height + self.text_spacing.y * 2
            self._max_width = max(self._max_width, text.width + self.text_spacing.x * 2)

            collider = Entity(parent = self, y = start_y, z = - 0.05, scale = Vec3(1, height, 1), origin = Vec3(-0.5,0.5,0), model = 'quad', collider = 'box', visible = False)
            collider.color = (self.color_divider + self.color_back) * 0.5

            start_y -= height
            self.texts.append(text)
            self.colliders.append(collider)

        self.back = Entity(parent = self, scale = Vec3(self._max_width, -start_y, 1), origin = Vec3(-0.5,0.5,0), model = 'quad', color = self.color_back)

        for i, value in enumerate(self.options.values()):
            self.colliders[i].scale_x = self._max_width

            if isinstance(value, dict):
                self.arrow = Entity(parent = self, 
                    position = Vec3(self._max_width - self.text_spacing.x * 0.1, self.colliders[i].y - self.colliders[i].scale_y * 0.5, -0.1),
                    model = Mesh(vertices=right_arrow_vert, mode='ngon', static=False), 
                    scale = self.text_spacing.x * 0.8 * 0.25, 
                    origin = (2,0,0),
                    color = self.color_divider)
    
    def input(self, key):
        if key == 'left mouse down':
            if mouse.hovered_entity in self.colliders:
                destroy(self.drop_down)

                i = self.colliders.index(mouse.hovered_entity)
                op = self.options[self.texts[i].text]
                if isinstance(op, dict):
                    self.drop_down = BarMenuDropDown(parent = self, position = self.colliders[i].position + Vec3(self._max_width,0,0), options = op)
                else:
                    self.on_selected(op)
                    self.clear_options()
            
            elif self.drop_down != None:
                if not self.drop_down.is_hovered():
                    destroy(self.drop_down)

    def update(self):
        for c in self.colliders:
            c.visible = c.hovered

    def is_hovered(self):
        if mouse.hovered_entity in self.colliders:
            return True
        if self.drop_down != None:
            return self.drop_down.is_hovered()
        return False

    def on_selected(self, op):
        self.parent.on_selected(op)
    
    def clear_options(self):
        self.parent.clear_options()