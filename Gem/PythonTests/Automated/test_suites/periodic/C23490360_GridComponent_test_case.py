"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test case ID : C23490360
# Test Case Title : Grid
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/23490360

import os
import sys

import azlmbr.editor
import azlmbr.legacy.general as general
from azlmbr.entity import EntityId

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.screenshot_utils import ScreenshotHelper

COMPONENT_PROPERTIES = [
    'Controller|Configuration|Secondary Grid Spacing',
    'Controller|Configuration|Primary Color',
    'Controller|Configuration|Grid Size',
    'Controller|Configuration|Axis Color',
    'Controller|Configuration|Secondary Color',
    'Controller',
    'Controller|Configuration',
    'Controller|Configuration|Primary Grid Spacing'
]

class Tests():
    pass

def run():


    helper.init_idle()
    helper.open_level("MeshTest")

    myEntityId = azlmbr.editor.ToolsApplicationRequestBus(azlmbr.bus.Broadcast, 'CreateNewEntity', EntityId())
    azlmbr.editor.EditorEntityAPIBus(azlmbr.bus.Event, 'SetName', myEntityId, "Grid")
    vec3 = azlmbr.math.Vector3(6.0, 5.0, -1.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", myEntityId, vec3)
    if myEntityId.IsValid():
        general.log("Entity successfully created.")

    component = helper.attach_component_to_entity(myEntityId, 'Grid')

    helper.compare_property_list(component, COMPONENT_PROPERTIES)

    new_grid_size = 20.0
    grid_size_property_path = 'Controller|Configuration|Grid Size'
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, grid_size_property_path, new_grid_size)
    grid_size = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, grid_size_property_path)
    if grid_size.GetValue() == new_grid_size:
        general.log("Grid size property of grid is correctly set")

    new_color = azlmbr.math.Color(0.0, 1.0, 1.0, 1.0)
    axis_color_property_path = 'Controller|Configuration|Axis Color'
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, axis_color_property_path, new_color)
    color = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, axis_color_property_path)
    if color.GetValue() == new_color:
        general.log("Axis color property of grid is correctly set")

    new_primary_grid_spacing = 1.5
    primary_grid_spacing_property_path = 'Controller|Configuration|Primary Grid Spacing'
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, primary_grid_spacing_property_path, new_primary_grid_spacing)
    primary_grid_spacing = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, primary_grid_spacing_property_path)
    if primary_grid_spacing.GetValue() == new_primary_grid_spacing:
        general.log("Primary grid spacing property of grid is correctly set")

    primary_color_property_path = 'Controller|Configuration|Primary Color'
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, primary_color_property_path, new_color)
    color = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, primary_color_property_path)
    if color.GetValue() == new_color:
        general.log("Primary color property of grid is correctly set")

    new_secondary_grid_spacing = 0.5
    secondary_grid_spacing_spacing_property_path = 'Controller|Configuration|Secondary Grid Spacing'
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, secondary_grid_spacing_spacing_property_path, new_secondary_grid_spacing)
    secondary_grid_spacing = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, secondary_grid_spacing_spacing_property_path)
    if secondary_grid_spacing.GetValue() == new_secondary_grid_spacing:
        general.log("Secondary grid spacing property of grid is correctly set")

    secondary_color_property_path = 'Controller|Configuration|Secondary Color'
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, secondary_color_property_path, new_color)
    color = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, secondary_color_property_path)
    if color.GetValue() == new_color:
        general.log("Secondary color property of grid is correctly set")

    # generate screenshot to compare with golden
    ScreenshotHelper(general.idle_wait_frames).capture_screenshot_blocking_in_game_mode('screenshot_atom_GridComponent.ppm')
    helper.close_editor()


if __name__ == "__main__":
    run()
