from ursina import *
from ursina import ursinamath
from extra_models import right_arrow_vert
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
    
    back_text = '    Back'
    clear_text = '    Clear Search'

    def __init__(self, options, **kwargs):
        super().__init__()

        self.option_scroll_count = 8
        self.scroll_position = 0
        self.options = options
        self.option_nested_position = []
        self.on_selected = None
        self.scroll_bar_radius = 0.015
        self.edge_spacing = 0.02
        self.text_spacing = 0.007
        self.width = 0.2
        self.ignore_next_input = True

        self.color_text = color.hsv(0,0,0.7)
        self.color_text_highlight = color.hsv(0,0,0.7, 0.3)
        self.color_back = color.hsv(0,0,0.2)
        self.color_highlight = color.hsv(0,0,0.3)
        self.color_search_box = color.hsv(0,0,0.15)

        self.disable_search = False
        self.disable_scroll_bar = False

        for key, value in kwargs.items():
            setattr(self, key, value)

        if not self.disable_search:
            self.search_text = TextField(parent = self, scale = 0.8, position = Vec3(-self.width * 0.5, - self.edge_spacing * 0.5, -0.1), scroll_size = (16,1), max_lines = 1, register_mouse_input = True)
            self.search_text.text = ' '
            self.search_text.text_entity.color = self.color_text
            self.search_text.cursor.color = self.color_text
            self.search_text.highlight_color = self.color_text_highlight
            self.search_text.render()
            quadScale = Vec2(self.width + self.edge_spacing * 0.5, self.search_text.text_entity.height + self.text_spacing * 0.5)
            self.search_back = Entity(parent = self, model = Quad(scale = quadScale, radius=0.01), z = 0.1, y = -self.edge_spacing * 0.25, origin_y = quadScale.y * 0.5, color = self.color_search_box)
            start_y = self.search_back.y
            self.search_text.text = ''
            self.search_text_input = self.search_text.input
            self.search_text.input = self.search_input
            self.search_text_keystroke = self.search_text.keystroke
            self.search_text.keystroke = self.search_keystroke
            self.search_text.active = True
            self.search_text.shortcuts['indent', 'dedent'] = ('',)
        else:
            quadScale = Vec2(self.width + self.edge_spacing * 0.5, self.text_spacing * 0.5)
            start_y = - self.edge_spacing * 0.5 

        self.option_slots = [
            Text(' ', parent = self, position = Vec3(-self.width * 0.5, -i, 0), color = self.color_text, scale = 0.7)
            for i in range(self.option_scroll_count)
        ]
        text_height = self.option_slots[0].height
        text_start = start_y + quadScale.y + self.text_spacing
        for t in self.option_slots:
            t.y = t.y * (text_height + self.text_spacing) - self.edge_spacing * 0.5 - text_start
        
        quadScale = Vec2(self.width + self.edge_spacing * 0.5, text_height + self.text_spacing)
        self.option_highlights = [
            Entity(parent = self, model = Quad(scale = quadScale, radius=0.005), position = Vec3(0, s.y + self.text_spacing * 0.5, 0.1), origin_y = quadScale.y * 0.5, color = self.color_highlight, collider='box', visible = False)
            for s in self.option_slots
        ]

        self.option_arrows = [
            Entity(parent = self, 
                position = Vec3(self.width * 0.5, s.y, 0), 
                model = Mesh(vertices=right_arrow_vert, mode='ngon', static=False), 
                scale = s.height * 0.25, 
                origin = (2,2,0), 
                color = self.color_text,
                visible = False)
            for s in self.option_slots
        ]

        self.back_arrow = Entity(parent = self, 
                position = Vec3(self.width * -0.5, self.option_slots[0].y, 0), 
                model = Mesh(vertices=right_arrow_vert, mode='ngon', static=False), 
                scale = self.option_slots[0].height * 0.25, 
                origin = (2,-2,0), 
                rotation_z = 180,
                color = self.color_text)

        quadScale = Vec2(self.width + self.edge_spacing, len(self.option_slots) * (text_height + self.text_spacing) + (self.edge_spacing - self.text_spacing) + text_start)
        self.ui_back = Entity(parent = self, model = Quad(scale = quadScale, radius=0.015), z = 0.2, origin_y = quadScale.y * 0.5, color = self.color_back, collider='box')

        quadScale = Vec2(self.scroll_bar_radius * 2, quadScale.y)
        self.scroll_back = Entity(
            parent = self, 
            model = Quad(scale = quadScale, radius=self.scroll_bar_radius), 
            x = self.scroll_bar_radius + self.width * 0.5 + self.edge_spacing * 1, 
            origin_y = quadScale.y * 0.5, 
            color = self.color_back, 
            z = 0.1,
            collider='box')
        self.scroll_height = quadScale.y

        inner_radius = self.scroll_bar_radius / 3
        quadScale = Vec2(inner_radius * 2, quadScale.y - inner_radius * 4)
        self.scroll_rail = Entity(
            parent = self.scroll_back, 
            model = Quad(scale = quadScale, radius=inner_radius), 
            origin_y = quadScale.y * 0.5 + self.scroll_bar_radius - inner_radius, 
            color = self.color_search_box,
            z = -0.1)

        self.scroll_bar = Entity(
            parent = self.scroll_back, 
            model = 'circle', 
            scale = self.scroll_bar_radius * 2,
            origin_y = 0.5, 
            color = self.color_highlight,
            z = -0.2)

        if self.disable_scroll_bar:
            self.scroll_back.disable()
            self.scroll_rail.disable()
            self.scroll_bar.disable()

        self.options_all = dict(self.options)
        finished = False
        while not finished:
            finished = True
            for k,v in self.options_all.items():
                if isinstance(v, dict):
                    finished = False
                    self.options_all.pop(k)
                    self.options_all.update(v)
                    break

        self.update_options()


    def input(self, key):
        if self.ignore_next_input: return
        if key == 'left mouse down':
            if self.disable_search:
                if (mouse.hovered_entity not in (self.ui_back, self.scroll_back)) and (mouse.hovered_entity not in self.option_highlights):
                    destroy(self)
                    return
            elif (mouse.hovered_entity not in (self.ui_back, self.search_text.bg, self.scroll_back)) and (mouse.hovered_entity not in self.option_highlights):
                destroy(self)
                return

            if mouse.hovered_entity in self.option_highlights:
                ind = self.option_highlights.index(mouse.hovered_entity)
                current_options = self.get_current_options()

                if self.option_slots[ind].text == ' ':
                    pass

                elif self.option_slots[ind].text == SearchMenu.clear_text:
                    self.end_search()

                elif self.option_slots[ind].text == SearchMenu.back_text:
                    self.option_nested_position.pop()
                    self.scroll_position = 0
                    self.update_options()

                elif isinstance(current_options[self.option_slots[ind].text], dict):
                    self.option_nested_position.append(self.option_slots[ind].text)
                    self.scroll_position = 0
                    self.update_options()

                elif self.on_selected != None:
                    self.on_selected(current_options[self.option_slots[ind].text])

        if key == 'scroll down':
            self.update_options(1)
        if key == 'scroll up':
            self.update_options(-1)

        if key == 'enter' and not self.disable_search and self.search_text.text != '':
            current_options = self.get_current_options()
            if self._current_option_count > 1:
                self.on_selected(current_options[self.option_slots[1].text])
    
    
    def update(self):
        self.ignore_next_input = False
        if mouse.left and mouse.hovered_entity == self.scroll_back:
            amount = ursinamath.clamp((-mouse.point.y - self.scroll_bar_radius) / (self.scroll_height - self.scroll_bar_radius * 2), 0, 1)
            total = self._current_option_count - self.option_scroll_count
            new_scroll_position = round(ursinamath.clamp(amount * (total), 0, total))
            if self.scroll_position != new_scroll_position:
                self.scroll_position = new_scroll_position
                self.update_options()
            
            self.update_options()

        for i in range(len(self.option_highlights)):
            s = mouse.hovered_entity == self.option_highlights[i] and self.option_slots[i].text != ' '
            if self.option_highlights[i].visible != s:
                self.option_highlights[i].visible = s
            
    def update_options(self, scroll = 0):
        current_options = self.get_current_options()
        self.scroll_position = ursinamath.clamp(self.scroll_position + scroll, 0, self._current_option_count - self.option_scroll_count)
        
        if self._current_option_count > self.option_scroll_count:
            self.scroll_bar.y = -self.scroll_position / (self._current_option_count - self.option_scroll_count) * (self.scroll_height - self.scroll_bar_radius * 2)
            self.scroll_bar.visible = True
        else:
            self.scroll_bar.visible = False

        keys = list(current_options.keys())
        for i in range(self.option_scroll_count):
            if i < self._current_option_count:
                self.option_slots[i].text = keys[i + self.scroll_position]
                self.option_arrows[i].visible = isinstance(current_options[keys[i + self.scroll_position]], dict)
            else:
                self.option_slots[i].text = ' '
                self.option_arrows[i].visible = False
        self.back_arrow.visible = (self.option_slots[0].text in [SearchMenu.clear_text, SearchMenu.back_text])
            

    def get_current_options(self):
        if self.disable_search or self.search_text.text == '':
            op = self.get_options(self.option_nested_position)
        else:
            op = self.search_options(self.search_text.text)
        self._current_option_count = len(op)
        return op

    # returns a list of options for that position in the tree
    # 'back' is added to the front if 
    def get_options(self, nested_position):
        op = dict(self.options)
        for p in nested_position:
            op = op[p]
        if len(nested_position) > 0:
            new_op = dict({SearchMenu.back_text:SearchMenu.back_text})
            new_op.update(op)
            return new_op
        return op


# - - - search functions - - -

    def search_options(self, query):
        query = query.lower()
        op = dict({SearchMenu.clear_text:SearchMenu.clear_text})
        op.update([(k,v) for k,v in self.options_all.items() if query in k.lower()])
        return op

    def search_keystroke(self, key):
        if not self.disable_search:
            self.search_check(self.search_text_keystroke, key)

    def search_input(self, key):
        if not self.disable_search:
            self.search_check(self.search_text_input, key)

    def search_check(self, func, key):
        old_text = str(self.search_text.text)
        func(key)
        if old_text != self.search_text.text:
            if self.search_text.text == '':
                self.end_search()
            else:
                self.update_options()
        

    def end_search(self):
        self.search_text.text = ''
        self.search_text.render()
        self.option_nested_position = []
        self.scroll_position = 0
        self.update_options()
