from compas_ifc.model import Model
from pathlib import Path


# Loading an IFC file and print summary
model = Model(Path(__file__).parent.parent / "data" / "Duplex_A_20110907.ifc")
model.print_summary()

# # print the spatial hierarchy
model.print_spatial_hierarchy(max_depth=10)

# # Visualize the model
model.show()
