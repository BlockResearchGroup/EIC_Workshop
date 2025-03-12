from compas_ifc.model import Model as IFCModel
from compas.geometry import Box
from pathlib import Path


# Create an empty IFC model using template
ifc_model = IFCModel.template()

# # Create a geometry for a slab
geometry = Box.from_width_height_depth(3000, 100, 3000)

# # Create a slab element in the IFC model
ifc_model.create(cls="IfcSlab", parent=ifc_model.building_storeys[0], geometry=geometry, name="My First Slab")

# # Visualize the IFC model
ifc_model.show()

# # Save the IFC model to file
ifc_model.save(Path(__file__).parent.parent / "data" / "simple_slab.ifc")

