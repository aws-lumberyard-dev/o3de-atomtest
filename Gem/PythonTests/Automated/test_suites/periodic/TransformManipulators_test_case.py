"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test case ID : C35756266
# Test Case Title : TransformManipulators
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/35756266

import os
import sys

import azlmbr.editor
import azlmbr.legacy.general as general
import azlmbr.paths

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.screenshot_utils import ScreenshotHelper
from Automated.atom_utils.hydra_editor_utils import helper_create_entity_with_mesh


class Tests():
    pass


def set_manipulator_transform_mode(mode):
    azlmbr.editor.EditorTransformComponentSelectionRequestBus(azlmbr.bus.Broadcast, "SetTransformMode", mode)


def set_camera_close(cameraEntityId):
    cameraTransform = azlmbr.math.Transform_CreateRotationZ(azlmbr.math.Math_DegToRad(118.0))
    cameraTransform.SetTranslation(azlmbr.math.Vector3(1.5, 1.0, 0.5))
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTM", cameraEntityId, cameraTransform)


def set_camera_far(cameraEntityId):
    cameraTransform = azlmbr.math.Transform_CreateRotationZ(azlmbr.math.Math_DegToRad(118.0))
    cameraTransform.SetTranslation(azlmbr.math.Vector3(6.0, 4.0, 0.5))
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTM", cameraEntityId, cameraTransform)


def run():
    # open pre-made level
    helper.init_idle()
    helper.open_level("EmptyLevel")

    screenshotHelper = ScreenshotHelper(general.idle_wait_frames)

    # create mesh
    entityId = helper_create_entity_with_mesh('objects/sphere.azmodel')
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", entityId, azlmbr.math.Vector3(0.0, 0.0, 0.0))
        
    cameraEntityId = helper.find_entities('Camera')[0]
    azlmbr.editor.EditorCameraRequestBus(azlmbr.bus.Broadcast, "SetViewAndMovementLockFromEntityPerspective", cameraEntityId, False)

    set_manipulator_transform_mode(azlmbr.editor.TransformMode_Translation)
    set_camera_close(cameraEntityId)
    general.idle_wait_frames(5)
    screenshotHelper.capture_screenshot_blocking('manipulator_translation_close.ppm')
    set_camera_far(cameraEntityId)
    general.idle_wait_frames(1)
    screenshotHelper.capture_screenshot_blocking('manipulator_translation_far.ppm')

    set_manipulator_transform_mode(azlmbr.editor.TransformMode_Rotation)
    set_camera_close(cameraEntityId)
    general.idle_wait_frames(1)
    screenshotHelper.capture_screenshot_blocking('manipulator_rotation_close.ppm')
    set_camera_far(cameraEntityId)
    general.idle_wait_frames(1)
    screenshotHelper.capture_screenshot_blocking('manipulator_rotation_far.ppm')

    set_manipulator_transform_mode(azlmbr.editor.TransformMode_Scale)
    set_camera_close(cameraEntityId)
    general.idle_wait_frames(1)
    screenshotHelper.capture_screenshot_blocking('manipulator_scale_close.ppm')
    set_camera_far(cameraEntityId)
    general.idle_wait_frames(1)
    screenshotHelper.capture_screenshot_blocking('manipulator_scale_far.ppm')

    helper.close_editor()


if __name__ == "__main__":
    run()
