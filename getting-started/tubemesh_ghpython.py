#! python3
# venv: eic
# r: compas

import compas
from compas.datastructures import Mesh
from compas_rhino.conversions import mesh_to_rhino

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

a = mesh_to_rhino(mesh)
