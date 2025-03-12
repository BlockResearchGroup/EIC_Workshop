from pathlib import Path
from compas_ifc.model import Model as IFCModel


# Import the IFC model from file
ifc_model = IFCModel(Path(__file__).parent.parent / "data" / "grid_model_modifiers_with_psets.ifc")

# Get the first BlockElement
block = ifc_model.get_entities_by_name("BlockElement")[0]

# Check the property sets
block.print_properties(max_depth=5)

# Validate the property sets using the json schema
block.validate_properties({
    "Pset_ConcreteRecipe": Path(__file__).parent / "recipe_schema.json"
})
