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
from Automated.atom_utils.screenshot_utils import ScreenshotHelper


class Tests():
    pass


def run():

    def after_level_load():
        """Function to call after creating/opening a level to ensure it loads."""
        # Give everything a second to initialize.
        general.idle_enable(True)
        general.update_viewport()
        general.idle_wait(0.5)  # half a second is more than enough for updating the viewport.

        # Close out problematic windows, FPS meters, and anti-aliasing.
        if general.is_helpers_shown():  # Turn off the helper gizmos if visible
            general.toggle_helpers()
        if general.is_pane_visible("Error Report"):  # Close Error Report windows that block focus.
            general.close_pane("Error Report")
        if general.is_pane_visible("Error Log"):  # Close Error Log windows that block focus.
            general.close_pane("Error Log")
        general.run_console("r_displayInfo=0")
        general.run_console("r_antialiasingmode=0")

        return True

    # Create a new test level
    test_level_name = 'MeshScalingTemporaryLevel'
    heightmap_resolution = 128
    heightmap_meters_per_pixel = 1
    terrain_texture_resolution = 128
    use_terrain = False

    # Return codes are ECreateLevelResult defined in CryEdit.h
    return_code = general.create_level_no_prompt(
        test_level_name, heightmap_resolution, heightmap_meters_per_pixel, terrain_texture_resolution, use_terrain)
    if return_code == 1:
        general.log(f"{test_level_name} level already exists")
    elif return_code == 2:
        general.log("Failed to create directory")
    elif return_code == 3:
        general.log("Directory length is too long")
    elif return_code != 0:
        general.log("Unknown error, failed to create level")
    else:
        general.log(f"{test_level_name} level created successfully")
    after_level_load()

    helper.init_idle()
    helper.open_level(test_level_name)
    general.idle_wait(1)

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
        general.log(mesh)
        meshIndex = meshIndex + 1
        offset.x += 3.0
        entityName = "TestEntity{}".format(meshIndex)
        helper_create_entity_with_mesh("scale_factor/" + mesh, offset, entityName)

    helper.enter_game_mode(["", ""])
    # Example: how to capture a screenshot
    general.set_viewport_size(1280,720)
    general.set_cvar_integer('r_DisplayInfo', 0)
    general.idle_wait_frames(1)

    ScreenshotHelper(general.idle_wait_frames).capture_screenshot_blocking("screenshot_atom_C24116651.dds")
    helper.exit_game_mode(["", ""])
    helper.close_editor()


if __name__ == "__main__":
    run()
