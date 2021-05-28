"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test case ID : C34792869
# Test Case Title : PostFx Shape Weight Modifier
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/34792869

import os
import sys

import azlmbr.editor
import azlmbr.legacy.general as general
import azlmbr.paths

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.screenshot_utils import ScreenshotHelper
from Automated.atom_utils.automated_test_utils import TestHelper as helper
from azlmbr.entity import EntityId

COMPONENT_PROPERTIES = [
    'Controller',
    'Controller|Configuration',
    'Controller|Configuration|Fall-off Distance'
]

FALLOFF_DIST = 0.5


def create_high_exposure_entity_with_sphere_shape():
    entityId = azlmbr.editor.ToolsApplicationRequestBus(azlmbr.bus.Broadcast, 'CreateNewEntity', EntityId())
    exposure_component = helper.attach_component_to_entity(entityId, 'Exposure Control')
    helper.set_component_property(
        exposure_component,
        'Controller|Configuration|Manual Compensation',
        4.0
    )
    sphere_shape_component = helper.attach_component_to_entity(entityId, 'Sphere Shape')
    helper.set_component_property(
        sphere_shape_component,
        'Sphere Shape|Sphere Configuration|Radius',
        5.0
    )
    helper.attach_component_to_entity(entityId, 'PostFX Layer')

    pos = azlmbr.math.Vector3(512.0, 512.0, 34.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", entityId, pos)

    return entityId


def create_low_exposure_entity():
    entityId = azlmbr.editor.ToolsApplicationRequestBus(azlmbr.bus.Broadcast, 'CreateNewEntity', EntityId())
    exposure_component = helper.attach_component_to_entity(entityId, 'Exposure Control')
    helper.set_component_property(
        exposure_component,
        'Controller|Configuration|Manual Compensation',
        -2.0
    )
    postfx_layer_component = helper.attach_component_to_entity(entityId, 'PostFX Layer')
    helper.set_component_property(
        postfx_layer_component,
        'Controller|Configuration|Priority',
        1
    )


def set_and_verify_shape_weight_modifier_component(shape_weight_modifier_component):
    falloff_property_path = 'Controller|Configuration|Fall-off Distance'

    # set properties
    helper.set_component_property(
        shape_weight_modifier_component,
        falloff_property_path,
        FALLOFF_DIST
    )

    # verify component properties
    helper.compare_property_list(shape_weight_modifier_component, COMPONENT_PROPERTIES)
    falloff_dist = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', shape_weight_modifier_component, falloff_property_path)
    if falloff_dist.GetValue() == FALLOFF_DIST:
        general.log('Fall-off distance property of shape weight modifier is correctly set')


def run():
    helper.init_idle()
    helper.open_level("EmptyLevel")

    # create entities
    entityId = create_high_exposure_entity_with_sphere_shape()
    create_low_exposure_entity()

    # attach shape weight modifier component
    shape_weight_modifier_component = helper.attach_component_to_entity(entityId, 'PostFX Shape Weight Modifier')
    set_and_verify_shape_weight_modifier_component(shape_weight_modifier_component)

    # Search for entity containing the camera so we can move it around and observe changes in exposure
    searchFilter = azlmbr.entity.SearchFilter()
    searchFilter.names = ['Camera']
    cameraEntityId = azlmbr.entity.SearchBus(azlmbr.bus.Broadcast, 'SearchEntities', searchFilter)[0]

    # Take screenshots on multiple locations to verify lerp effect of shape weight modifier component
    new_position1 = azlmbr.math.Vector3(512.0, 512.0, 34.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", cameraEntityId, new_position1)
    screenshot_helper = ScreenshotHelper(general.idle_wait_frames)
    screenshot_helper.capture_screenshot_blocking_in_game_mode('screenshot_atom_ShapeWeightModifierComponent_FullExposure.ppm')
    new_position2 = azlmbr.math.Vector3(512.0, 517.25, 34.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", cameraEntityId, new_position2)
    screenshot_helper.capture_screenshot_blocking_in_game_mode('screenshot_atom_ShapeWeightModifierComponent_HalfExposure.ppm')
    new_position3 = azlmbr.math.Vector3(512.0, 520.0, 34.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", cameraEntityId, new_position3)
    screenshot_helper.capture_screenshot_blocking_in_game_mode('screenshot_atom_ShapeWeightModifierComponent_NoExposure.ppm')
    general.log("Three screenshots taken.")
    helper.close_editor()


if __name__ == "__main__":
    run()
