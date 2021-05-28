"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""


# Test case ID : C34896059
# Test Case Title : Exposure
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/34896059

import os
import sys
import time

import azlmbr.editor
import azlmbr.legacy.general as general
import azlmbr.paths
from azlmbr.entity import EntityId

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.screenshot_utils import ScreenshotHelper

EXPOSURE_COMPONENT_PROPERTIES = [
    'Controller|Configuration|Overrides|EyeAdaptationSpeedDown Override', 
    'Controller|Configuration|Eye Adaptation|Speed Up', 
    'Controller|Configuration|Eye Adaptation|Enable Heatmap', 
    'Controller|Configuration|Overrides|ManualCompensation Override', 
    'Controller|Configuration|Eye Adaptation|Minimum Exposure', 
    'Controller|Configuration|Overrides|EyeAdaptationSpeedUp Override', 
    'Controller|Configuration|Eye Adaptation|Speed Down', 
    'Controller|Configuration|Manual Compensation', 
    'Controller|Configuration|Overrides|EyeAdaptationExposureMin Override', 
    'Controller|Configuration|Eye Adaptation|Maximum Exposure', 
    'Controller|Configuration|Overrides|HeatmapEnabled Override', 
    'Controller|Configuration|Control Type', 
    'Controller|Configuration|Enable', 
    'Controller', 
    'Controller|Configuration', 
    'Controller|Configuration|Overrides|Enabled Override', 
    'Controller|Configuration|Overrides|ExposureControlType Override', 
    'Controller|Configuration|Overrides|EyeAdaptationExposureMax Override'
]

ExposureControlTypes = {"Manual":0, "Eye Adaptation":1}


class Tests():
    pass


def run():
    # open pre-made level
    helper.init_idle()
    helper.open_level("MeshTest")

    # Create new entity
    myEntityId = azlmbr.editor.ToolsApplicationRequestBus(azlmbr.bus.Broadcast, 'CreateNewEntity', EntityId())
    azlmbr.editor.EditorEntityAPIBus(azlmbr.bus.Event, 'SetName', myEntityId, "Exposure control")
    if myEntityId.IsValid():
        general.log("Entity successfully created.")

    # PostFX Layer
    pfx_component = helper.attach_component_to_entity(myEntityId, 'PostFX Layer')
    # Exposure Control
    exposure_component = helper.attach_component_to_entity(myEntityId, 'Exposure Control')

    # verify property list of component
    helper.compare_property_list(exposure_component, EXPOSURE_COMPONENT_PROPERTIES)
    
    exposureEnabled = 'Controller|Configuration|Enable'
    exposureControlType = 'Controller|Configuration|Control Type'

    # Enable exposure control
    helper.set_component_property(exposure_component, exposureEnabled, True) 
    # Manual exposure
    helper.set_component_property(exposure_component, exposureControlType, ExposureControlTypes["Manual"])
    
    # Verify settings
    enabledProperty = helper.get_component_property(exposure_component, exposureEnabled)
    if enabledProperty.GetValue() == True:
        general.log("Exposure enabled correctly set")
    exposureType = helper.get_component_property(exposure_component, exposureControlType)
    if exposureType.GetValue() == ExposureControlTypes["Manual"]:
        general.log("Manual exposure type enabled correctly set")
    # Capture sceenshot
    screenshot_helper = ScreenshotHelper(general.idle_wait_frames)
    screenshot_helper.capture_screenshot_blocking_in_game_mode('screenshot_atom_ExposureComponent_Manual.ppm')

    # Eye adaptation
    azlmbr.editor.EditorComponentAPIBus(
        azlmbr.bus.Broadcast,
        'SetComponentProperty',
        exposure_component,
        exposureControlType,
        ExposureControlTypes["Eye Adaptation"])
    
    # Verify eye adaptation set
    exposureType = helper.get_component_property(exposure_component, exposureControlType)
    if exposureType.GetValue() == ExposureControlTypes["Eye Adaptation"]:
        general.log("Eye adaptation exposure type enabled correctly set")
        
    # Wait for a while for the eye adaptation to settle
    general.idle_wait_frames(300)
    # Capture screenshot
    screenshot_helper.capture_screenshot_blocking_in_game_mode('screenshot_atom_ExposureComponent_EyeAdaptation.ppm')
    helper.close_editor()


if __name__ == "__main__":
    run()
