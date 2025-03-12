#! python3
# venv: eic
# r: compas

import rhinoscriptsyntax as rs  # noqa: I001
import pathlib

import compas
import compas_rhino.objects
from compas.datastructures import Mesh
from compas.topology import astar_shortest_path
from compas.scene import Scene

HERE = pathlib.Path(__file__).parent
SESSION = HERE / "data" / "session.json"

# =============================================================================
# Session Import
# =============================================================================

session = compas.json_load(SESSION)

mesh: Mesh = session["tubemesh"]

# =============================================================================
# Do
# =============================================================================

scene = Scene()
scene.clear_context()
meshobj = scene.add(mesh, show_vertices=True)
scene.draw()

guids = compas_rhino.objects.select_points("Select Two Points")

start = meshobj._guid_vertex[guids[0]]
end = meshobj._guid_vertex[guids[-1]]

mesh.attributes["path_start"] = start
mesh.attributes["path_end"] = end

path = astar_shortest_path(mesh, start, end)

session["path"] = path

# =============================================================================
# Session Export
# =============================================================================

compas.json_dump(session, SESSION)

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
scene.clear_context()

meshobj = scene.add(mesh, show_vertices=path)
scene.draw()
