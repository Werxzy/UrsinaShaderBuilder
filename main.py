from ursina import *
from shader_builder_manager import ShaderBuilderManager
from panda3d.core import loadPrcFileData
# from panda3d.core import Nodepath as np
from panda3d.core import AntialiasAttrib

#need to be called before or in Ursina()
loadPrcFileData('', 'framebuffer-multisample 1')
loadPrcFileData('', 'multisamples 2')

app = Ursina()

# this appears to do nothing
# camera.render.setAntialias(AntialiasAttrib.MMultisample)

def input(key):
    pass

window.x = 200
window.borderless = False

sbm = ShaderBuilderManager()

app.run()