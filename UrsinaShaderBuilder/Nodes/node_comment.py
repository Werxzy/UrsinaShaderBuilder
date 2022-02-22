from shader_node import ShaderNode

'''
Node that holds a comment and doesn't affect the shader.
'''

class CommentNode(ShaderNode):

    def __init__(self, text = '', size = [0.3,0.2], **kwargs):
        super().__init__(**kwargs)
        self.append_text('Comment')
        self.ui_text = self.append_expandable_text_field(text, list(size))

    def save(self):
        return {'text' : self.ui_text[0].text, 'size' : self.ui_text[0].node_size}

    def load(manager, data):
        return CommentNode(parent = manager, manager = manager, text = data['text'], size = data['size'])
