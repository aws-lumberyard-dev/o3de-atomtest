"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test Case ID: 32077236
# Test Case Title: Radius Weight Modifier
# URL of the test case: https://testrail.agscollab.com/index.php?/cases/view/32077236

import os
import sys

import azlmbr.editor
import azlmbr.legacy.general as general
import azlmbr.paths
from azlmbr.entity import EntityId

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.screenshot_utils import ScreenshotHelper
from Automated.atom_utils.automated_test_utils import TestHelper as helper

COMPONENT_PROPERTIES = [
    'Controller',
    'Controller|Configuration',
    'Controller|Configuration|Radius'
]
RADIUS = 5.0


class Tests():
    pass


def run():
    helper.init_idle()
    helper.open_level("EmptyLevel")

    # Create component with radius weight modifier and high exposure control
    entityWithHighExposureAndRadiusWeightModifier = azlmbr.editor.ToolsApplicationRequestBus(azlmbr.bus.Broadcast, 'CreateNewEntity', EntityId())
    exposure_component = helper.attach_component_to_entity(entityWithHighExposureAndRadiusWeightModifier, 'Exposure Control')
    azlmbr.editor.EditorComponentAPIBus(
        azlmbr.bus.Broadcast,
        'SetComponentProperty',
        exposure_component,
        'Controller|Configuration|Manual Compensation',
        4.0)
    helper.attach_component_to_entity(entityWithHighExposureAndRadiusWeightModifier, 'PostFX Layer')
    radius_weight_modifier_component = helper.attach_component_to_entity(entityWithHighExposureAndRadiusWeightModifier, 'Radius Weight Modifier')
    helper.compare_property_list(radius_weight_modifier_component, COMPONENT_PROPERTIES)
    radius_property_path = 'Controller|Configuration|Radius'
    azlmbr.editor.EditorComponentAPIBus(
        azlmbr.bus.Broadcast,
        'SetComponentProperty',
        radius_weight_modifier_component,
        radius_property_path,
        RADIUS)
    pos = azlmbr.math.Vector3(512.0, 512.0, 34.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", entityWithHighExposureAndRadiusWeightModifier, pos)

    # Create second component with low exposure control
    entityWithLowExposure = azlmbr.editor.ToolsApplicationRequestBus(azlmbr.bus.Broadcast, 'CreateNewEntity', EntityId())
    exposure_component = helper.attach_component_to_entity(entityWithLowExposure, 'Exposure Control')
    azlmbr.editor.EditorComponentAPIBus(
        azlmbr.bus.Broadcast,
        'SetComponentProperty',
        exposure_component,
        'Controller|Configuration|Manual Compensation',
        -2.0)
    postfx_layer_component = helper.attach_component_to_entity(entityWithLowExposure, 'PostFX Layer')
    azlmbr.editor.EditorComponentAPIBus(
        azlmbr.bus.Broadcast,
        'SetComponentProperty',
        postfx_layer_component,
        'Controller|Configuration|Priority',
        1)

    # verify radius weight modifier properties were set correctly
    radius = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', radius_weight_modifier_component, radius_property_path)
    if (radius.GetValue() == RADIUS):
        general.log("Radius property of radius weight modifier is correctly set")

    # Search for entity containing the camera so we can move it around and observe changes in exposure
    searchFilter = azlmbr.entity.SearchFilter()
    searchFilter.names = ['Camera']
    cameraEntityId = azlmbr.entity.SearchBus(azlmbr.bus.Broadcast, 'SearchEntities', searchFilter)[0]

    # Take screenshots on multiple locations to verify lerp effect of radius weight modifier component
    new_position1 = azlmbr.math.Vector3(512.0, 512.0, 34.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", cameraEntityId, new_position1)
    screenshot_helper = ScreenshotHelper(general.idle_wait_frames)
    screenshot_helper.capture_screenshot_blocking_in_game_mode('screenshot_atom_RadiusWeightModifierComponent_FullExposure.ppm')
    new_position2 = azlmbr.math.Vector3(512.0, 514.5, 34.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", cameraEntityId, new_position2)
    screenshot_helper.capture_screenshot_blocking_in_game_mode('screenshot_atom_RadiusWeightModifierComponent_HalfExposure.ppm')
    new_position3 = azlmbr.math.Vector3(512.0, 520.0, 34.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", cameraEntityId, new_position3)
    screenshot_helper.capture_screenshot_blocking_in_game_mode('screenshot_atom_RadiusWeightModifierComponent_NoExposure.ppm')
    general.log("Three screenshots taken.")
    helper.close_editor()

if __name__ == "__main__":
    run()