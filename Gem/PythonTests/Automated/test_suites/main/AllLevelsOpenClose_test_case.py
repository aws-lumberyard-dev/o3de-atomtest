"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# This module does a bulk test and update of many components at once.
# Each test case is listed below in the format:
#     "Test Case ID: Test Case Title (URL)"

# C34428159: Editor - ActorTest_100Actors (https://testrail.agscollab.com/index.php?/cases/view/34428159)
# C34428160: Editor - ActorTest_MultipleActors (https://testrail.agscollab.com/index.php?/cases/view/34428160)
# C34428161: Editor - ActorTest_SingleActor (https://testrail.agscollab.com/index.php?/cases/view/34428161)
# C34428162: Editor - ColorSpaceTest (https://testrail.agscollab.com/index.php?/cases/view/34428162)
# C34428163: Editor - DefaultLevel (https://testrail.agscollab.com/index.php?/cases/view/34428163)
# C34428165: Editor - Lucy (https://testrail.agscollab.com/index.php?/cases/view/34428165)
# C34428166: Editor - lucy_high (https://testrail.agscollab.com/index.php?/cases/view/34428166)
# C34428167: Editor - macbeth_shaderballs (https://testrail.agscollab.com/index.php?/cases/view/34428167)
# C34428158: Editor - MeshTest (https://testrail.agscollab.com/index.php?/cases/view/34428158)
# C34428172: Editor - NormalMapping (https://testrail.agscollab.com/index.php?/cases/view/34428172)
# C34428173: Editor - PbrMaterialChart (https://testrail.agscollab.com/index.php?/cases/view/34428173)
# C34428174: Editor - ShadowTest (https://testrail.agscollab.com/index.php?/cases/view/34428174)
# C34428175: Editor - TangentSpace (https://testrail.agscollab.com/index.php?/cases/view/34428175)

import os
import sys

import azlmbr.legacy.general as general
import azlmbr.legacy.settings as settings
import azlmbr.paths

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper

# Set up our valid test levels first that can be tested.
LEVELS = os.listdir(os.path.join(azlmbr.paths.devroot, "AtomTest", "Levels"))
INVALID_LEVELS = ["mult-mat-fbx-test", "bentley_test", "ColorSpaceTest", "DefaultLevel"]
for invalid_level in INVALID_LEVELS:
    try:
        LEVELS.remove(invalid_level)
    except ValueError:  # Level doesn't exist already
        continue


class TestAllLevelsOpenClose(object):
    """Reserved for the test name."""
    pass


def run():
    """
    1. Open & close all valid test levels in the Editor.
    2. Every time a level is opened, verify it loads correctly and the Editor remains stable.
    """

    def after_level_load():
        """Function to call after creating/opening a level to ensure it loads."""
        # Give everything a second to initialize.
        general.idle_enable(True)
        general.idle_wait(1.0)
        general.update_viewport()
        general.idle_wait(0.5)  # half a second is more than enough for updating the viewport.

        # Close out problematic windows, FPS meters, and anti-aliasing.
        if general.is_helpers_shown():  # Turn off the helper gizmos if visible
            general.toggle_helpers()
            general.idle_wait(1.0)
        if general.is_pane_visible("Error Report"):  # Close Error Report windows that block focus.
            general.close_pane("Error Report")
        if general.is_pane_visible("Error Log"):  # Close Error Log windows that block focus.
            general.close_pane("Error Log")
        general.idle_wait(1.0)
        general.run_console("r_displayInfo=0")
        general.run_console("r_antialiasingmode=0")
        general.idle_wait(1.0)

        return True

    # Wait for Editor idle loop before executing Python hydra scripts.
    helper.init_idle()

    # Create a new level.
    new_level_name = "tmp_level"  # Specified in AllLevelsOpenClose_test.py
    heightmap_resolution = 512
    heightmap_meters_per_pixel = 1
    terrain_texture_resolution = 412
    use_terrain = False

    # Return codes are ECreateLevelResult defined in CryEdit.h
    return_code = general.create_level_no_prompt(
        new_level_name, heightmap_resolution, heightmap_meters_per_pixel, terrain_texture_resolution, use_terrain)
    if return_code == 1:
        general.log(f"{new_level_name} level already exists")
    elif return_code == 2:
        general.log("Failed to create directory")
    elif return_code == 3:
        general.log("Directory length is too long")
    elif return_code != 0:
        general.log("Unknown error, failed to create level")
    else:
        general.log(f"{new_level_name} level created successfully")
    after_level_load()

    # Open all valid test levels.
    failed_to_open = []
    LEVELS.append(new_level_name)  # Update LEVELS constant for created level.
    for level in LEVELS:
        if general.is_idle_enabled() and (general.get_current_level_name() == level):
            general.log(f"Level {level} already open.")
        else:
            general.log(f"Opening level {level}")
            general.open_level_no_prompt(level)
            helper.wait_for_condition(function=lambda: general.get_current_level_name() == level,
                                      timeout_in_seconds=2.0)
        result = (general.get_current_level_name() == level) and after_level_load()
        if result:
            general.log(f"Successfully opened {level}")
        else:
            general.log(f"{level} failed to open")
            failed_to_open.append(level)

    if failed_to_open:
        general.log(f"The following levels failed to open: {failed_to_open}")


if __name__ == "__main__":
    run()
