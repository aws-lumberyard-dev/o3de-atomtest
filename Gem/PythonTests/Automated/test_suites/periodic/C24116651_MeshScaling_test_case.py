"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test case ID : C24116651
# Test Case Title : Imported fbx meshes correctly scale in Atom projects
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/24116651

# This test case can be run in the Editor:
#       pyRunFile @devroot@/Tests/Atom/Automated/C24116651_MeshScaling.py

import logging
import os
import sys

import azlmbr.legacy.general as general
import azlmbr.atom
import azlmbr.math as math
import azlmbr.asset as asset
import azlmbr.bus as bus
import azlmbr.editor
import azlmbr.paths
from azlmbr.entity import EntityId

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.hydra_editor_utils import helper_create_entity_with_mesh


class Tests():
    pass


def run():
    # Create a new test level
    test_level_name = 'MeshScalingTemporaryLevel'
    try:
        result = general.create_level_no_prompt(test_level_name, 128, 1, 128, False)
    except:
        logging.error("Failed to create a new level")

    helper.init_idle()
    helper.open_level(test_level_name)
    general.idle_wait_frames(1)

    ### test body
    meshes = ["zup_scene_cm_auto.azmodel",
        "zup_scene_cm_explicit_cm.azmodel",
        "zup_scene_cm_explicit_ft.azmodel",
        "zup_scene_cm_explicit_m.azmodel",
        "zup_scene_ft_auto.azmodel",
        "zup_scene_ft_explicit_cm.azmodel",
        "zup_scene_ft_explicit_ft.azmodel",
        "zup_scene_ft_explicit_m.azmodel",
        "zup_scene_m_auto.azmodel",
        "zup_scene_m_explicit_cm.azmodel",
        "zup_scene_m_explicit_ft.azmodel",
        "zup_scene_m_explicit_m.azmodel" ]

    offset = math.Vector3()
    offset.x = -20.0
    offset.y = 0.0
    offset.z = 0.0

    meshIndex = 0
    for mesh in meshes:
        print(mesh)
        meshIndex = meshIndex + 1
        offset.x += 3.0
        entityName = "TestEntity{}".format(meshIndex)
        helper_create_entity_with_mesh("scale_factor/" + mesh, offset, entityName)

    helper.enter_game_mode(["", ""])
    # Example: how to capture a screenshot
    general.set_viewport_size(1280,720)
    general.set_cvar_integer('r_DisplayInfo', 0)
    general.idle_wait_frames(1)

    from screenshot_utils import ScreenshotHelper
    import azlmbr.legacy.general as general
    ScreenshotHelper(general.idle_wait_frames).capture_screenshot_blocking("screenshot_atom_C24116651.dds")

    helper.exit_game_mode(["", ""])

    helper.close_editor()


if __name__ == "__main__":
    run()
