from ursina import *
import json

with open('Example\\Basic Shaders\\basic.ursinashader') as f:
# with open('basic.ursinashader') as f: # location depends on how it's run
    shader_file = json.load(f)

with open('Example\\Basic Shaders\\basicWinputs.ursinashader') as f:
# with open('basicWinputs.ursinashader') as f:
    shader_file2 = json.load(f)

app = Ursina(borderless = False)

shader = Shader(vertex = shader_file['vertex'], fragment = shader_file['fragment'])
shader2 = Shader(vertex = shader_file2['vertex'], fragment = shader_file2['fragment'])
shader2.default_input.update({
    'lightColor' : (1, 0.2, 0.2),
    'lightDir' : (0, -1, 0),
})

sphere = Entity(model = 'sphere', shader = shader, x = -0.7, y = 0.7)
cube = Entity(model = 'cube', shader = shader, x = 0.7, y = 0.7, rotation_y = 20)

sphere2 = Entity(model = 'sphere', shader = shader2, x = -0.7, y = -0.7)
cube2 = Entity(model = 'cube', shader = shader2, x = 0.7, y = -0.7, rotation_y = 20)

EditorCamera()

app.run()