from ursina import *
from shader_builder_manager import ShaderBuilderManager
from panda3d.core import loadPrcFileData
# from panda3d.core import Nodepath as np
# from panda3d.core import AntialiasAttrib

# from shader_node_connector import NodeConnector
# NodeConnector.line_quality = 10

#need to be called before or in Ursina()
loadPrcFileData('', 'framebuffer-multisample 1')
loadPrcFileData('', 'multisamples 2')


app = Ursina(borderless = False, fullscreen = False)

# this appears to do nothing
# camera.render.setAntialias(AntialiasAttrib.MMultisample)

window.x = 200

sbm = ShaderBuilderManager()

app.run()