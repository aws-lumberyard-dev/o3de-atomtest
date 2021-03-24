"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test case ID : C34785692
# Test Case Title : Spot Light Hydra Automated Test
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/34785692

import os
import sys
import math

import azlmbr.bus as bus
import azlmbr.components as components
import azlmbr.editor as editor
import azlmbr.entity as entity
import azlmbr.legacy.general as general
import azlmbr.math
import azlmbr.paths

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.screenshot_utils import ScreenshotHelper
from Automated.atom_utils.hydra_editor_utils import helper_create_entity_with_mesh


COMPONENT_PROPERTIES = [
    'Controller',
    'Controller|Configuration',
    'Controller|Configuration|Color',
    'Controller|Configuration|Intensity Mode',
    'Controller|Configuration|Intensity',
    'Controller|Configuration|Cone Configuration|Inner Cone Angle',
    'Controller|Configuration|Cone Configuration|Outer Cone Angle',
    'Controller|Configuration|Cone Configuration|Penumbra Bias',
    'Controller|Configuration|Attenuation Radius|Radius',
    'Controller|Configuration|Attenuation Radius|Mode',
    'Controller|Configuration|Shadow|Enable Shadow',
    'Controller|Configuration|Shadow|ShadowmapSize',
    'Controller|Configuration|Shadow|Shadow Filter Method',
    'Controller|Configuration|Shadow|Softening Boundary Width',
    'Controller|Configuration|Shadow|Prediction Sample Count',
    'Controller|Configuration|Shadow|Filtering Sample Count'
]


class Tests():
    pass


def rotation_rad(x, y, z):
    return azlmbr.math.Vector3(math.radians(x), math.radians(y), math.radians(z))


def prepare_level_and_prepare_camera():
    helper.init_idle()
    helper.open_level("DefaultLevel")
    general.idle_wait_frames(1)

    # Get Default Atom Environment entity.
    base_entity = helper.find_entities('Default Atom Environment')[0]
    components.TransformBus(bus.Event, 'SetLocalTranslation', base_entity, azlmbr.math.Vector3(64.0, 64.0, 34.0))

    # Place camera to origin relative to Default Atom Environment.
    camera_entity = helper.find_entities('Camera')[0]
    components.TransformBus(bus.Event, 'SetLocalTranslation', camera_entity, azlmbr.math.Vector3(0.0, -3.0, 2.0))
    components.TransformBus(bus.Event, 'SetLocalRotation', camera_entity, rotation_rad(-10.0, 0.0, 0.0))

    return base_entity


def prepare_for_floor_and_bunny(base_entity):
    # 2. Create an entity with a Mesh Component and set plane.azmodel which is used for shadow receiver.
    floor = helper_create_entity_with_mesh('objects/plane.azmodel', azlmbr.math.Vector3(), 'Floor', base_entity)
    components.TransformBus(bus.Event, 'SetLocalTranslation', floor, azlmbr.math.Vector3(0.0, 0.0, 0.8))
    components.TransformBus(bus.Event, 'SetLocalScale', floor, azlmbr.math.Vector3(20.0, 20.0, 1.0))

    # 3. Create an entity with a Mesh Component and set bunny.azmodel which is used for shadow caster.
    # 4. Move the plane to beneath the bunny and scale the plane to be a shadow catcher.
    bunny = helper_create_entity_with_mesh('objects/bunny.azmodel', azlmbr.math.Vector3(), 'Bunny', base_entity)
    components.TransformBus(bus.Event, 'SetLocalTranslation', bunny, azlmbr.math.Vector3(-1.0, 0.0, 1.0))


def prepare_for_red_spot_light_component(base_entity, screenshot_helper, screenshot_filename_base):
    # 5. Create an entity with a Spot Light Component.
    red_light = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', base_entity)
    if red_light.IsValid():
        general.log('Entity for red light is successfully created.')
    editor.EditorEntityAPIBus(bus.Event, 'SetName', red_light, 'RedLight')
    red_light_component = helper.attach_component_to_entity(red_light, 'Spot Light')

    # 6. Verify property list of the spot light component.
    helper.compare_property_list(red_light_component, COMPONENT_PROPERTIES)

    # 7. Set transform of the spot light to lit bunny.
    components.TransformBus(bus.Event, 'SetLocalTranslation', red_light, azlmbr.math.Vector3(-0.4, 1.3, 4.0))
    components.TransformBus(bus.Event, 'SetLocalRotation', red_light, rotation_rad(-112.0, 0.0, 0.0))
    general.log('Positioned red spot light.')

    # 8. Set color red, intensity 100, and outer cone angle 70 to the Spot Light. (Compare Screenshot)
    color_path = 'Controller|Configuration|Color'
    intensity_path = 'Controller|Configuration|Intensity'
    coneAngle_path = 'Controller|Configuration|Cone Configuration|Outer Cone Angle'
    color_value = azlmbr.math.Color(1.0, 0.0, 0.0, 1.0)
    intensity_value = 100.0
    coneAngle_value = 70.0
    helper.set_component_property(red_light_component, color_path, color_value)
    helper.set_component_property(red_light_component, intensity_path, intensity_value)
    helper.set_component_property(red_light_component, coneAngle_path, coneAngle_value)
    general.log('Set red spot light properties.')
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'noshadow.ppm')

    return red_light_component


def enable_shadow(red_light_component, screenshot_helper, screenshot_filename_base):
    color_path = 'Controller|Configuration|Color'
    intensity_path = 'Controller|Configuration|Intensity'
    coneAngle_path = 'Controller|Configuration|Cone Configuration|Outer Cone Angle'
    color_value = azlmbr.math.Color(1.0, 0.0, 0.0, 1.0)
    intensity_value = 100.0
    coneAngle_value = 70.0

    # 9. Enable shadow and set shadomwap size 2048.  (Compare Screenshot)
    enableShadow_path = 'Controller|Configuration|Shadow|Enable Shadow'
    shadowmapSize_path = 'Controller|Configuration|Shadow|ShadowmapSize'
    shadowmapSize_value = 2048
    helper.set_component_property(red_light_component, enableShadow_path, True)
    # [GFX TODO][ATOM-6249] add control of shadowmap size.
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'red.ppm')
    
    # Verify that component contains the expected values
    color_result = helper.get_component_property(red_light_component, color_path)
    if color_result.GetValue() == color_value:
        general.log("Color property of spot light is correctly set.")
    intensity_result = helper.get_component_property(red_light_component, intensity_path)
    if intensity_result.GetValue() == intensity_value:
        general.log("Intensity property of spot light is correctly set.")
    coneAngle_result = helper.get_component_property(red_light_component, coneAngle_path)
    if coneAngle_result.GetValue() == coneAngle_value:
        general.log("Cone Angle property of spot light is correctly set.")
    enableShadow_result = helper.get_component_property(red_light_component, enableShadow_path)
    if enableShadow_result.GetValue() == True:
        general.log("Enable Shadow property of spot light is correctly set.")
    shadowmapSize_result = helper.get_component_property(red_light_component, shadowmapSize_path)
    if shadowmapSize_result.GetValue() == shadowmapSize_value:
        general.log("Shadowmap Size property of spot light is correctly set.")


def add_blue_spot_light(base_entity, screenshot_helper, screenshot_filename_base):
    color_path = 'Controller|Configuration|Color'
    intensity_path = 'Controller|Configuration|Intensity'
    coneAngle_path = 'Controller|Configuration|Cone Configuration|Outer Cone Angle'
    enableShadow_path = 'Controller|Configuration|Shadow|Enable Shadow'

    # 10. Add an entity with a Spot Light Component with blue color, intensity 200, cone angle 50, and shadowmap size 1024.
    blue_light = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', base_entity)
    editor.EditorEntityAPIBus(bus.Event, 'SetName', blue_light, 'BlueLight')
    blue_light_component = helper.attach_component_to_entity(blue_light, 'Spot Light')
    components.TransformBus(bus.Event, 'SetLocalTranslation', blue_light, azlmbr.math.Vector3(-1.5, -1.4, 2.8))
    components.TransformBus(bus.Event, 'SetLocalRotation', blue_light, rotation_rad(-82.0, -50.0, -38.0))
    helper.set_component_property(blue_light_component, color_path, azlmbr.math.Color(0.0, 0.0, 1.0, 1.0))
    helper.set_component_property(blue_light_component, intensity_path, 200.0)
    helper.set_component_property(blue_light_component, coneAngle_path, 50.0)
    # [GFX TODO][ATOM-6249] add control of shadowmap size.

    # 11. Set filtering method PCF to the blue spot light.  (Compare Screenshot)
    filterMethod_None = 0
    filterMethod_Pcf = 1
    filterMethod_Esm = 2
    filterMethod_EsmPcf = 3
    filterMethod_path = 'Controller|Configuration|Shadow|Shadow Filter Method'
    boundaryWidth_path = 'Controller|Configuration|Shadow|Softening Boundary Width'
    helper.set_component_property(blue_light_component, enableShadow_path, True)
    helper.set_component_property(blue_light_component, filterMethod_path, filterMethod_Pcf)
    helper.set_component_property(blue_light_component, boundaryWidth_path, 0.75)
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'redblue.ppm')
    # [GFX TODO][ATOM-6249] add control of shadowmap size.


def add_green_spot_light(base_entity, screenshot_helper, screenshot_filename_base):
    filterMethod_None = 0
    filterMethod_Pcf = 1
    filterMethod_Esm = 2
    filterMethod_EsmPcf = 3
    color_path = 'Controller|Configuration|Color'
    intensity_path = 'Controller|Configuration|Intensity'
    coneAngle_path = 'Controller|Configuration|Cone Configuration|Outer Cone Angle'
    enableShadow_path = 'Controller|Configuration|Shadow|Enable Shadow'
    filterMethod_path = 'Controller|Configuration|Shadow|Shadow Filter Method'
    boundaryWidth_path = 'Controller|Configuration|Shadow|Softening Boundary Width'

    # 12. Add an entity with a Spot Light Component with green color, intensity 300, cone angle 30, and shadowmap size 1024.
    green_light = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', base_entity)
    editor.EditorEntityAPIBus(bus.Event, 'SetName', green_light, 'GreenLight')
    green_light_component = helper.attach_component_to_entity(green_light, 'Spot Light')
    components.TransformBus(bus.Event, 'SetLocalTranslation', green_light, azlmbr.math.Vector3(2.9, 0.6, 4.2))
    components.TransformBus(bus.Event, 'SetLocalRotation', green_light, rotation_rad(26.4, -31.8, 112.6))
    helper.set_component_property(green_light_component, color_path, azlmbr.math.Color(0.0, 1.0, 0.0, 1.0))
    helper.set_component_property(green_light_component, intensity_path, 300.0)
    helper.set_component_property(green_light_component, coneAngle_path, 30.0)

    # 13. Set filtering method ESM to the green spot light.  (Compare Screenshot)
    helper.set_component_property(green_light_component, enableShadow_path, True)
    helper.set_component_property(green_light_component, filterMethod_path, filterMethod_Esm)
    helper.set_component_property(green_light_component, boundaryWidth_path, 0.75)
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'redbluegreen.ppm')


def run():
    screenshot_filename_base = 'screenshot_C34785692_atom_spotlight_'

    base_entity = prepare_level_and_prepare_camera()
    prepare_for_floor_and_bunny(base_entity)

    screenshot_helper = ScreenshotHelper(general.idle_wait_frames)

    red_light_component = prepare_for_red_spot_light_component(base_entity, screenshot_helper, screenshot_filename_base)
    enable_shadow(red_light_component, screenshot_helper, screenshot_filename_base)
    add_blue_spot_light(base_entity, screenshot_helper, screenshot_filename_base)    
    add_green_spot_light(base_entity, screenshot_helper, screenshot_filename_base)    

    helper.close_editor()


if __name__ == "__main__":
    run()
