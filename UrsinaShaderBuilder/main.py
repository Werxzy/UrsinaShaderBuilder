from ursina import *
from shader_builder_manager import ShaderBuilderManager
from panda3d.core import loadPrcFileData
import json

# default config info
config = {
	'AntiAliasing' : 1,
	'Line Quality' : 26,
	'Start Fullscreen' : 0
}

#loading config
try:
	with open('config.json', 'r') as f:
		config.update(json.load(f))
	with open('config.json', 'w') as f:
		json.dump(config, f) # update any missing information
except FileNotFoundError:
	with open('config.json', 'w') as f:
		json.dump(config, f)
except json.JSONDecodeError:
	with open('config.json', 'w') as f:
		json.dump(config, f)

# - - - setting config info - - -

if config['AntiAliasing'] == 1:
	loadPrcFileData('', 'framebuffer-multisample 1')
	loadPrcFileData('', 'multisamples 2')

from shader_node_connector import NodeConnector
NodeConnector.line_quality = config['Line Quality']

window.title = 'Ursina Shader Builder'

app = Ursina(borderless = False, fullscreen = config['Start Fullscreen'] == 1, vsync = False)

camera.ui_render.set_depth_test(1)
camera.ui_render.set_depth_write(1)
# turns out for instanced rendering, depth writing/testing is important

sbm = ShaderBuilderManager()

app.run()