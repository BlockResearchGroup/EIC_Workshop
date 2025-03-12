import pathlib

import compas
from compas_gmsh.models import MeshModel
from compas_viewer import Viewer

# ==============================================================================
# Define the data files
# ==============================================================================

HERE = pathlib.Path(__file__).parent
SESSION = HERE / "data" / "session.json"

# ==============================================================================
# Import the session
# ==============================================================================

session = compas.json_load(SESSION)

# ==============================================================================
# Construct Mesh Model
# ==============================================================================

filepath = str(HERE / "data" / "waffle.stp")

model = MeshModel.from_step(filepath)

# =============================================================================
# Mesh Options
# =============================================================================

model.options.mesh.meshsize_max = 0.1

# ==============================================================================
# Generate Surface Mesh
# ==============================================================================

model.generate_mesh(2)
model.optimize_mesh(niter=10)

# =============================================================================
# Convert to COMPAS Mesh
# =============================================================================

meshmodel = model.mesh_to_compas()

# ==============================================================================
# Viz
# ==============================================================================

viewer = Viewer()
viewer.renderer.camera.position = [3, -7, 3]
viewer.renderer.camera.target = [0, 0, 2]

viewer.scene.add(meshmodel)

viewer.show()
