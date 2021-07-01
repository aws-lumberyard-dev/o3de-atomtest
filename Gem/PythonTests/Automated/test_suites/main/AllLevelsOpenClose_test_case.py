"""
Copyright (c) Contributors to the Open 3D Engine Project

SPDX-License-Identifier: Apache-2.0 OR MIT

Hydra script that is used to open all AtomTest levels inside its "Levels" directory, verifying they don't crash.

See the run() function for more in-depth test info.
"""

import os
import sys

import azlmbr.legacy.general as general
import azlmbr.paths

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper

LEVELS = os.listdir(os.path.join(azlmbr.paths.devroot, "AtomTest", "Levels"))


def run():
    """
    Scans the AtomTest "Levels" directory for any levels and for each level it:
    1. Opens & closes the level in the Editor.
    2. Utilizes Editor.log to find the general.log(f"Successfully opened {level}") call for the level to pass the test.
    3. If general.log(f"Successfully opened {level}") is failed to be called for the level, the test will fail.
    4. Any Trace::Assert, Trace::Error, or "Traceback (most recent call last):" indicate a crash & will fail the test.
    """

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
