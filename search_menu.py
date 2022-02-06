from ursina import *

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
        self.options = options
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



    def input(self, key):
        if (mouse.hovered_entity != self.ui_back) and (mouse.hovered_entity not in self.option_highlights) and (mouse.hovered_entity != self.search_text.bg):
            if key == 'left mouse down':
                destroy(self)


    def update(self):
        for h in self.option_highlights:
            if h.visible != (mouse.hovered_entity == h):
                h.visible = mouse.hovered_entity == h
            
