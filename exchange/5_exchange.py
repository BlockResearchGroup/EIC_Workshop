#! python3
# venv: eic
# r: compas

import pathlib

import compas
import compas_rhino.conversions
import compas_rhino.objects

HERE = pathlib.Path(__file__).parent
SESSION = HERE / "data" / "session.json"

# =============================================================================
# Session Import
# =============================================================================

session = compas.json_load(SESSION)

# =============================================================================
# Do
# =============================================================================

guid = compas_rhino.objects.select_curve()
curve = compas_rhino.conversions.curveobject_to_compas(guid)

# =============================================================================
# Session Export
# =============================================================================

session["curve"] = curve

compas.json_dump(session, SESSION)

# =============================================================================
# Visualisation
# =============================================================================
