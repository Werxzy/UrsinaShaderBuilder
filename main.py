from ursina import *
from shader_builder_manager import ShaderBuilderManager
from panda3d.core import loadPrcFileData
# from panda3d.core import Nodepath as np
from panda3d.core import AntialiasAttrib

# from shader_node_connector import NodeConnector
# NodeConnector.line_quality = 10

#need to be called before or in Ursina()
loadPrcFileData('', 'framebuffer-multisample 1')
loadPrcFileData('', 'multisamples 2')


app = Ursina()

# this appears to do nothing
# camera.render.setAntialias(AntialiasAttrib.MMultisample)

window.x = 200
window.borderless = False

sbm = ShaderBuilderManager()

def input(key):
    if key == 'b':
        global sbm
        t = time.time()
        print(sbm.build_shader(sbm.mode))
        print('\nBuild Time:',time.time() - t)
    pass

app.run()