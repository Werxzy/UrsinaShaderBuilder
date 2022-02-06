from ursina import *
from ursina import ursinamath
'''
Menu that allows being searched through.

{
    'option name' : 'command',
    'option name' : 'command',
    'sub-menu name' : {
        'option name' : 'command',
        'option name' : 'command',
        ...
    }
    ...
}
'''

class SearchMenu(Entity):
    def __init__(self, options, **kwargs):
        super().__init__()

        self.option_scroll_count = 8
        self.scroll_position = 0
        self.options = options
        self.option_nested_position = []
        self.on_selected = None
        self.scroll_bar_width = 0.015
        self.edge_spacing = 0.02
        self.text_spacing = 0.007
        self.width = 0.2

        self.color_text = color.hsv(0,0,0.7)
        self.color_back = color.hsv(0,0,0.2)
        self.color_highlight = color.hsv(0,0,0.3)
        self.color_search_box = color.hsv(0,0,0.15)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.search_text = TextField(parent = self, scale = 0.8, position = Vec3(-self.width * 0.5, - self.edge_spacing * 0.5, -0.1), scroll_size = (16,1), max_lines = 1, register_mouse_input = True)
        self.search_text.text = 'TEST g test'
        self.search_text.text_entity.color = self.color_text
        self.search_text.render()
        quadScale = Vec2(self.width + self.edge_spacing * 0.5, self.search_text.text_entity.height + self.text_spacing * 0.5)
        self.search_back = Entity(parent = self, model = Quad(scale = quadScale, radius=0.01), z = 0.1, y = -self.edge_spacing * 0.25, origin_y = quadScale.y * 0.5, color = self.color_search_box, collider='box')

        self.option_slots = [
            Text('TEST g test', parent = self, position = Vec3(-self.width * 0.5, -i, 0), color = self.color_text, scale = 0.7)
            for i in range(self.option_scroll_count)
        ]
        text_height = self.option_slots[0].height
        text_start = self.search_back.y + quadScale.y + self.text_spacing
        for t in self.option_slots:
            t.y = t.y * (text_height + self.text_spacing) - self.edge_spacing * 0.5 - text_start
        
        quadScale = Vec2(self.width + self.edge_spacing * 0.5, text_height + self.text_spacing)
        self.option_highlights = [
            Entity(parent = self, model = Quad(scale = quadScale, radius=0.005), position = Vec3(0, s.y + self.text_spacing * 0.5, 0.1), origin_y = quadScale.y * 0.5, color = self.color_highlight, collider='box', visible = False)
            for s in self.option_slots
        ]
        
        quadScale = Vec2(self.width + self.edge_spacing, len(self.option_slots) * (text_height + self.text_spacing) + (self.edge_spacing - self.text_spacing) + text_start)
        self.ui_back = Entity(parent = self, model = Quad(scale = quadScale, radius=0.015), z = 0.2, origin_y = quadScale.y * 0.5, color = self.color_back, collider='box')

        self.update_options()


    def input(self, key):
        if (mouse.hovered_entity != self.ui_back) and (mouse.hovered_entity not in self.option_highlights) and (mouse.hovered_entity != self.search_text.bg):
            if key == 'left mouse down':
                destroy(self)

        elif key == 'left mouse down' and mouse.hovered_entity in self.option_highlights:
            ind = self.option_highlights.index(mouse.hovered_entity)
            current_options = self.get_options(self.option_nested_position)

            if self.option_slots[ind].text == '':
                pass

            elif self.option_slots[ind].text == '< Back':
                self.option_nested_position.pop()
                self.scroll_position = 0
                self.update_options()

            elif isinstance(current_options[self.option_slots[ind].text], dict):
                self.option_nested_position.append(self.option_slots[ind].text)
                self.scroll_position = 0
                self.update_options()

            else:
                self.on_selected(current_options[self.option_slots[ind].text])

        if key == 'scroll down':
            self.update_options(1)
        if key == 'scroll up':
            self.update_options(-1)

    def update(self):
        for h in self.option_highlights:
            if h.visible != (mouse.hovered_entity == h):
                h.visible = mouse.hovered_entity == h
            
    def update_options(self, scroll = 0):
        current_options = self.get_options(self.option_nested_position)
        self.scroll_position = ursinamath.clamp(self.scroll_position + scroll, 0, len(current_options) - self.option_scroll_count)

        keys = list(current_options.keys())
        max = len(current_options)
        for i in range(self.option_scroll_count):
            if i < max:
                self.option_slots[i].text = keys[i + self.scroll_position]
                # if isinstance(current_options[keys[i]], dict):
                #   TODO, show arrow
            else:
                self.option_slots[i].text = ''
            

    # returns a list of options for that position in the tree
    # 'back' is added to the front if 
    def get_options(self, nested_position):
        op = dict(self.options)
        for p in nested_position:
            op = op[p]
        if len(nested_position) > 0:
            new_op = dict({'< Back':'< Back'})
            new_op.update(op)
            return new_op
        return op