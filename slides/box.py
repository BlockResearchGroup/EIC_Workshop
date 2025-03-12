import pathlib

import compas
from compas.geometry import Box
from compas_viewer import Viewer

box = Box(1)

filepath = pathlib.Path(__file__).parent / "data" / "box.json"
compas.json_dump(box, filepath)

viewer = Viewer()
viewer.scene.add(box)
viewer.show()
