from pathlib import Path
from compas_grid.models import GridModel
from compas_ifc.model import Model as IFCModel
import compas

model: GridModel = compas.json_load(Path(__file__).parent.parent / "data" / "grid_model_modifiers.json")

# Create an empty IFC model using template
ifc_model = IFCModel.template()


# Create a map between COMPAS model classes and IFC classes
class_map = {
    "BlockElement": "IfcBuildingElementProxy",
    "BeamProfileElement": "IfcBeam",
    "ColumnElement": "IfcColumn",
}

# Insert elements into the IFC model
parent = ifc_model.building_storeys[0]
for element in model.elements():
    geometry = element.modelgeometry
    compas_cls = element.__class__.__name__
    ifc_cls = class_map[compas_cls]
    ifc_model.create(cls=ifc_cls, parent=parent, geometry=geometry, name=compas_cls)


# Visualize the IFC model
ifc_model.show()

# Save the IFC model to file
ifc_model.save(Path(__file__).parent.parent / "data" / "grid_model_modifiers.ifc")
