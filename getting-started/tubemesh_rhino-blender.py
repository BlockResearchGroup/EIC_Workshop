#! python3
# venv: eic
# r: compas

import compas
from compas.datastructures import Mesh
from compas.scene import Scene

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

scene = Scene()
scene.clear_context()
scene.add(mesh)
scene.draw()
