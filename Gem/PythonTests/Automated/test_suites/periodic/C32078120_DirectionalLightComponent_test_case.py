"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test case ID : C32078120
# Test Case Title : Directional Light Hydra Automated Test
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/32078120

import os
import sys
import math

import azlmbr.bus as bus
import azlmbr.components as components
import azlmbr.editor as editor
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
    'Controller|Configuration|Angular Diameter',
    'Controller|Configuration|Shadow|Camera',
    'Controller|Configuration|Shadow|Shadow Far Clip',
    'Controller|Configuration|Shadow|Shadowmap Size',
    'Controller|Configuration|Shadow|Cascade Count',
    'Controller|Configuration|Shadow|Split Automatic',
    'Controller|Configuration|Shadow|Split Ratio',
    'Controller|Configuration|Shadow|Far Depth Cascade',
    'Controller|Configuration|Shadow|Ground Height',
    'Controller|Configuration|Shadow|Enable Cascade Correction?',
    'Controller|Configuration|Shadow|Enable Debug Coloring?',
    'Controller|Configuration|Shadow|Shadow Filter Method',
    'Controller|Configuration|Shadow|Softening Boundary Width',
    'Controller|Configuration|Shadow|Prediction Sample Count',
    'Controller|Configuration|Shadow|Filtering Sample Count'
]


class Tests():
    pass


def rotation_rad(x, y, z):
    return azlmbr.math.Vector3(x / 180.0 * math.pi, y / 180.0 * math.pi, z / 180.0 * math.pi)


def almost_equal(float0, float1):
    return abs(float0 - float1) < abs(float0) / 1000000.0


def prepare_level_and_prepare_camera():
    helper.init_idle()
    helper.open_level("DefaultLevel")
    general.idle_wait_frames(1)
    
    # Get Default Atom Environment entity.
    base_entity = helper.find_entities('Default Atom Environment')[0]

    # Place camera to origin relative to Default Atom Environment.
    camera_entity = helper.find_entities('Camera')[0]
    components.TransformBus(bus.Event, 'SetLocalTranslation', camera_entity, azlmbr.math.Vector3(0.0, -3.0, 2.0))
    components.TransformBus(bus.Event, 'SetLocalRotation', camera_entity, rotation_rad(-10.0, 0.0, 0.0))

    return base_entity


def prepare_for_floor_and_bunny(base_entity):
    # 2. Create an entity with a Mesh Component and set plane.azmodel which is used for shadow receiver.
    floor = helper_create_entity_with_mesh('objects/plane.azmodel', azlmbr.math.Vector3(), 'Floor')

    # 3. Create an entity with a Mesh Component and set bunny.azmodel which is used for shadow caster.
    bunny = helper_create_entity_with_mesh('objects/bunny.azmodel', azlmbr.math.Vector3(), 'Bunny')
    components.TransformBus(bus.Event, 'SetLocalTranslation', bunny, azlmbr.math.Vector3(-1.0, 0.0, 1.0))

    # 4. Move the plane to beneath the bunny and scale the plane to be a shadow catcher.
    components.TransformBus(bus.Event, 'SetLocalTranslation', floor, azlmbr.math.Vector3(0.0, 0.0, 0.8))
    components.TransformBus(bus.Event, 'SetLocalScale', floor, azlmbr.math.Vector3(20.0, 20.0, 1.0))


def prepare_for_directional_light_component(base_entity):
    # 5. Create an entity with a Directional Light Component
    light = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', base_entity)
    if light.IsValid():
        general.log('Entity for directional light is successfully created.')
    editor.EditorEntityAPIBus(bus.Event, 'SetName', light, 'DirectionalLight')
    light_component = helper.attach_component_to_entity(light, 'Directional Light')

    # 6. Verify property list of component
    helper.compare_property_list(light_component, COMPONENT_PROPERTIES)

    # 7. Set transform of directional light to lit bunny
    components.TransformBus(bus.Event, 'SetLocalRotation', light, Vector3(0.0, math.pi / 6, -math.pi * 2 / 3))
    # directional light component ignore the location of itself.

    return light_component


def set_color_light_green(light_component, screenshot_helper, screenshot_filename_base):
    # 8. Set Color light green, Intensity 1.0, to the Light. (Compare Screenshot)
    color_path = 'Controller|Configuration|Color'
    intensity_path = 'Controller|Configuration|Intensity'
    color_value = azlmbr.math.Color(0.5, 1.0, 0.5, 1.0)
    intensity_value = 1.0
    helper.set_component_property(light_component, color_path, color_value)
    helper.set_component_property(light_component, intensity_path, intensity_value)
    general.log('Set light color and intensity.')
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'nofilter.ppm')

    # 9. Verify component's color and intensity
    color_result = helper.get_component_property(light_component, color_path)
    if color_result.GetValue() == color_value:
        general.log('Color property of light is correctly set.')
    intensity_result = helper.get_component_property(light_component, intensity_path)
    if intensity_result.GetValue() == intensity_value:
        general.log('Intensity of light is correctly set.')


def set_manual_cascade(light_component, screenshot_helper, screenshot_filename_base):
    # 10. Set Cascade Count 3, disable automatic cascade splitting, Far Depth Cascade, and enable Debug Coloring (Compare Screenshot)
    cascadeCount_path = 'Controller|Configuration|Shadow|Cascade Count'
    splitAutomatic_path = 'Controller|Configuration|Shadow|Split Automatic'
    farDepthCascade_path = 'Controller|Configuration|Shadow|Far Depth Cascade'
    enableDebugColoring_path = 'Controller|Configuration|Shadow|Enable Debug Coloring?'
    cascadeCount_value = 3
    splitAutomatic_value = False
    farDepthCascade_value = azlmbr.math.Vector4(2.0, 3.0, 4.0, 20.0)
    enableDebugColoring_value = True
    helper.set_component_property(light_component, cascadeCount_path, cascadeCount_value)
    helper.set_component_property(light_component, splitAutomatic_path, splitAutomatic_value)
    helper.set_component_property(light_component, farDepthCascade_path, farDepthCascade_value)
    helper.set_component_property(light_component, enableDebugColoring_path, enableDebugColoring_value)
    general.log('Set light cascade far depth manually and enabled debug coloring.')
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'manualcascade.ppm')

    # 11. Verify component's cascade count, automatic flag of cascade splitting, far depth cascade, and flag of debug coloring.
    cascadeCount_result = helper.get_component_property(light_component, cascadeCount_path)
    if cascadeCount_result.GetValue() == cascadeCount_value:
        general.log('Cascade Count of light is correctly set.')
    splitAutomatic_result = helper.get_component_property(light_component, splitAutomatic_path)
    if splitAutomatic_result.GetValue() == splitAutomatic_value:
        general.log('Split Automatic of light is correctly set.')
    farDepthCascade_result = helper.get_component_property(light_component, farDepthCascade_path)
    if farDepthCascade_result.GetValue() == farDepthCascade_value:
        general.log('Far Depth Cascade of light is correctly set.')
    enableDebugColoring_result = helper.get_component_property(light_component, enableDebugColoring_path)
    if enableDebugColoring_result.GetValue() == enableDebugColoring_value:
        general.log('Enable Debug Color of light is correctly set.')


def set_automatic_cascade(light_component, screenshot_helper, screenshot_filename_base):
    cascadeCount_path = 'Controller|Configuration|Shadow|Cascade Count'
    splitAutomatic_path = 'Controller|Configuration|Shadow|Split Automatic'
    # 12. Set split ratio 0.98 and cascade count 4 and enable automatic cascade splitting (Compare Screenshot)
    splitRatio_path = 'Controller|Configuration|Shadow|Split Ratio'
    splitRatio_value = 0.98
    helper.set_component_property(light_component, splitRatio_path, splitRatio_value)
    helper.set_component_property(light_component, cascadeCount_path, 4)
    helper.set_component_property(light_component, splitAutomatic_path, True)
    general.log('Set split ratio.')
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'autocascade.ppm')

    # 13. Verify component's split ratio.
    splitRatio_result = helper.get_component_property(light_component, splitRatio_path)
    if almost_equal(splitRatio_result.GetValue(), splitRatio_value):
        general.log('Split Ratio of light is correctly set.')


def set_pcf_low_sample_count(light_component, screenshot_helper, screenshot_filename_base):
    enableDebugColoring_path = 'Controller|Configuration|Shadow|Enable Debug Coloring?'
    # 14. Disable debug coloring and Set Filter method PCF with boundary width 0.07 and low sample count. (Compare Screenshot)
    filterMethod_path = 'Controller|Configuration|Shadow|Shadow Filter Method'
    boundaryWidth_path = 'Controller|Configuration|Shadow|Softening Boundary Width'
    predictionCount_path = 'Controller|Configuration|Shadow|Prediction Sample Count'
    filteringCount_path = 'Controller|Configuration|Shadow|Filtering Sample Count'
    filterMethod_value = 1 # PCF
    boundaryWidth_value = 0.07
    predictionCount_value = 2
    filteringCount_value = 4
    helper.set_component_property(light_component, enableDebugColoring_path, False)
    helper.set_component_property(light_component, filterMethod_path, filterMethod_value)
    helper.set_component_property(light_component, boundaryWidth_path, boundaryWidth_value)
    helper.set_component_property(light_component, predictionCount_path, predictionCount_value)
    helper.set_component_property(light_component, filteringCount_path, filteringCount_value)
    general.log('Set PCF filtering with low sample count.')
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'pcflow.ppm')

    # 15. Verify component's PCF parametes.
    filterMethod_result = helper.get_component_property(light_component, filterMethod_path)
    if filterMethod_result.GetValue() == filterMethod_value:
        general.log('Filter Method of light is correctly set.')
    boundaryWidth_result = helper.get_component_property(light_component, boundaryWidth_path)
    if almost_equal(boundaryWidth_result.GetValue(), boundaryWidth_value):
        general.log('Boundary Width of light is correctly set.')
    predictionCount_result = helper.get_component_property(light_component, predictionCount_path)
    if predictionCount_result.GetValue() == predictionCount_value:
        general.log('Prediction Sample Count of light is correctly set.')
    filteringCount_result = helper.get_component_property(light_component, filteringCount_path)
    if filteringCount_result.GetValue() == filteringCount_value:
        general.log('Filtering Sample Count of light is correctly set.')


def set_pcf_high_sample_count(light_component, screenshot_helper, screenshot_filename_base):
    predictionCount_path = 'Controller|Configuration|Shadow|Prediction Sample Count'
    filteringCount_path = 'Controller|Configuration|Shadow|Filtering Sample Count'
    # 16. Set PCF filtering with high sample count.  (Compare Screenshot)
    helper.set_component_property(light_component, predictionCount_path, 16)
    helper.set_component_property(light_component, filteringCount_path, 64)
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'pcfhigh.ppm')


def set_esm(light_component, screenshot_helper, screenshot_filename_base):
    filterMethod_path = 'Controller|Configuration|Shadow|Shadow Filter Method'
    # 17. Set ESM filtering.  (Compare Screenshot)
    helper.set_component_property(light_component, filterMethod_path, 2) # ESM
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + 'esm.ppm')


def add_2nd_light(base_entity, screenshot_helper, screenshot_filename_base):
    # 18. Add second directional light and confirm non-crashing.  (Compare Screenshot)
    light2nd = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', base_entity)
    if light2nd.IsValid():
        general.log('Entity for second directional light is successfully created.')
    editor.EditorEntityAPIBus(bus.Event, 'SetName', light2nd, 'DirectionalLight 2')
    helper.attach_component_to_entity(light2nd, 'Directional Light')
    components.TransformBus(bus.Event, 'SetLocalRotation', light2nd, rotation_rad(-90.0, 0.0, 0.0))
    screenshot_helper.capture_screenshot_blocking_in_game_mode(screenshot_filename_base + '2ndlight.ppm')


def run():
    screenshot_filename_base = 'screenshot_C32078120_atom_directionallight_'

    base_entity = prepare_level_and_prepare_camera()
    prepare_for_floor_and_bunny(base_entity)
    light_component = prepare_for_directional_light_component(base_entity)

    screenshot_helper = ScreenshotHelper(general.idle_wait_frames)

    set_color_light_green(light_component, screenshot_helper, screenshot_filename_base)
    set_manual_cascade(light_component, screenshot_helper, screenshot_filename_base)
    set_automatic_cascade(light_component, screenshot_helper, screenshot_filename_base)
    set_pcf_low_sample_count(light_component, screenshot_helper, screenshot_filename_base)
    set_pcf_high_sample_count(light_component, screenshot_helper, screenshot_filename_base)
    set_esm(light_component, screenshot_helper, screenshot_filename_base)
    add_2nd_light(base_entity, screenshot_helper, screenshot_filename_base)

    helper.close_editor()


if __name__ == "__main__":
    run()
