"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

import os
import sys
import math

import azlmbr.editor
import azlmbr.legacy.general as general
import azlmbr.paths
from azlmbr.entity import EntityId

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.screenshot_utils import ScreenshotHelper

COMPONENT_PROPERTIES = [
    'Controller',
    'Controller|Configuration',
    'Controller|Configuration|Intensity Mode',
    'Controller|Configuration|Sky Intensity',
    'Controller|Configuration|Sun Intensity',
    'Controller|Configuration|Turbidity',
    'Controller|Configuration|Sun Radius Factor'
]


class Tests():
    pass


def run():
    # open test level
    helper.init_idle()
    helper.open_level("MeshTest")

    # Create new entity
    myEntityId = azlmbr.editor.ToolsApplicationRequestBus(azlmbr.bus.Broadcast, 'CreateNewEntity', EntityId())
    azlmbr.editor.EditorEntityAPIBus(azlmbr.bus.Event, 'SetName', myEntityId, "Skybox")
    if myEntityId.IsValid():
        general.log("Entity successfully created.")

    # Attach PhysicalSky component
    component = helper.attach_component_to_entity(myEntityId, 'Physical Sky')

    # verify property list of component
    helper.compare_property_list(component, COMPONENT_PROPERTIES)

    # Set component properties
    skyIntensityPath = COMPONENT_PROPERTIES[3]
    sunIntensityPath = COMPONENT_PROPERTIES[4]
    turbidityPath = COMPONENT_PROPERTIES[5]
    sunRadiusPath = COMPONENT_PROPERTIES[6]

    skyIntensityValue = 3 # in EV100
    sunIntensityValue = 4 # in EV100
    turbidityValue = 2
    sunRadiusValue = 2

    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, skyIntensityPath, skyIntensityValue)
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, sunIntensityPath, sunIntensityValue)
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, turbidityPath, turbidityValue)
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, sunRadiusPath, sunRadiusValue)

    # verify that physical sky component contains the expected values
    componentProperty = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, skyIntensityPath)
    if componentProperty.GetValue() == skyIntensityValue:
        general.log("Sky Intensity is correctly set")
    componentProperty = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, sunIntensityPath)
    if componentProperty.GetValue() == sunIntensityValue:
        general.log("Sun Intensity is correctly set")
    componentProperty = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, turbidityPath)
    if componentProperty.GetValue() == turbidityValue:
        general.log("Turbidity is correctly set")
    componentProperty = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, sunRadiusPath)
    if componentProperty.GetValue() == sunRadiusValue:
        general.log("Sun Radius is correctly set")

    # Set transform of physical sky
    eulerAngle = azlmbr.math.Vector3( math.pi/8.0, 0.0, math.pi)
    azlmbr.components.TransformBus(azlmbr.bus.Event, 'SetLocalRotation', myEntityId, eulerAngle)

    # generate screenshot and compare with golden
    ScreenshotHelper(general.idle_wait_frames).capture_screenshot_blocking_in_game_mode('screenshot_atom_PhysicalSkyComponent.ppm')
    helper.close_editor()

if __name__ == "__main__":
    run()
