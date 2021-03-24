"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test case ID : C24134029
# Test Case Title : Mesh groups imported to Atom correctly preserve their spatial structure
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/24134029

# This test case can be run in the Editor:
#       pyRunFile @devroot@/Tests/Atom/Automated/C24134029_MeshGroupImporting.py

import os
import sys

import azlmbr.legacy.general as general
import azlmbr.atom
import azlmbr.math as math
import azlmbr.paths
import azlmbr.asset as asset
import azlmbr.bus as bus
import azlmbr.editor
from azlmbr.entity import EntityId

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.hydra_editor_utils import helper_create_entity_with_mesh


class Tests():
    pass


def run():
    # Create a new test level
    test_level_name = 'MeshGroupingTemporaryLevel'
    result = general.create_level_no_prompt(test_level_name, 128, 1, 128, False)

    helper.init_idle()
    helper.open_level(test_level_name)
    general.idle_wait_frames(1)

    ### test body
    meshes = ["cube_group.azmodel",
              "cube_parent.azmodel",
              "cube_parent_plus_locator.azmodel",
              "cube_parent_plus_locator_rotatez_90.azmodel",
              "cube_parent__rotatez_90_locator.azmodel",
              "cube_parent__scaley_2_locator.azmodel",
              "cube_parent__transx_100_locator.azmodel"]

    offset = math.Vector3()
    offset.x = -15.0
    offset.y = 0.0
    offset.z = 0.0

    meshIndex = 0
    for mesh in meshes:
        meshIndex = meshIndex + 1
        offset.x += 3.0
        entityName = "TestEntity{}".format(meshIndex)
        helper_create_entity_with_mesh("dag_hierarchy/" + mesh, offset, entityName)

    helper.enter_game_mode(["", ""])
    # Example: how to capture a screenshot
    general.set_viewport_size(1280, 720)
    general.set_cvar_integer('r_DisplayInfo', 0)
    general.idle_wait_frames(1)

    from screenshot_utils import ScreenshotHelper
    import azlmbr.legacy.general as general
    ScreenshotHelper(general.idle_wait_frames).capture_screenshot_blocking("screenshot_atom_C24134029.dds")

    helper.exit_game_mode(["", ""])

    helper.close_editor()


if __name__ == "__main__":
    run()
