import compas
from compas.datastructures import Mesh
from compas_viewer import Viewer
from compas_viewer.config import Config

mesh = Mesh.from_obj(compas.get("tubemesh.obj"))

config = Config()
config.camera.position = [2, -5, 1]
config.camera.target = [2, 0, 1]

viewer = Viewer(config=config)
viewer.scene.add(mesh)
viewer.show()
