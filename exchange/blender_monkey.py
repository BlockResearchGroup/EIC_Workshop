import pathlib

import bpy
import compas
from compas.colors import Color
from compas.scene import Scene
from compas_blender import conversions

FILE = bpy.context.space_data.text.filepath
MONKEY = pathlib.Path(FILE).resolve().parent / "data" / "monkey.json"

monkey = conversions.monkey_to_compas()

compas.json_dump(monkey, MONKEY)

scene = Scene()
scene.clear_context()

scene.add(monkey, color=Color.from_hex("#0092d2"))
scene.draw()
