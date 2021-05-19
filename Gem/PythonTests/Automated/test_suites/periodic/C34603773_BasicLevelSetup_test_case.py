"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
# Test case ID : C34603773
# Test Case Title : Atom Component - Basic Level Setup
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/34603773

import os
import sys

import azlmbr.math as math
import azlmbr.bus as bus
import azlmbr.paths
import azlmbr.legacy.general as general
import azlmbr.editor as editor

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

import Automated.atom_utils.hydra_editor_utils as hydra
from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.screenshot_utils import ScreenshotHelper

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
DEGREE_RADIAN_FACTOR = 0.0174533


def run():
    def initial_viewport_setup(screen_width, screen_height):
        general.set_viewport_size(screen_width, screen_height)
        general.update_viewport()
        helper.wait_for_condition(
            function=lambda: helper.isclose(a=general.get_viewport_size().x, b=SCREEN_WIDTH, rel_tol=0.1)
            and helper.isclose(a=general.get_viewport_size().y, b=SCREEN_HEIGHT, rel_tol=0.1),
            timeout_in_seconds=4.0
        )
        result = helper.isclose(a=general.get_viewport_size().x, b=SCREEN_WIDTH, rel_tol=0.1) and helper.isclose(
            a=general.get_viewport_size().y, b=SCREEN_HEIGHT, rel_tol=0.1)
        general.log(general.get_viewport_size().x)
        general.log(general.get_viewport_size().y)
        general.log(general.get_viewport_size().z)
        general.log(f"Viewport is set to the expected size: {result}")
        general.log("Basic level created")
        general.run_console("r_DisplayInfo = 0")

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
    new_level_name = "all_components_indepth_level"  # Specified in class TestAllComponentsIndepthTests()
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

    # Basic setup for newly created level.
    after_level_load()
    initial_viewport_setup(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Create default_level entity
    hydra.delete_all_existing_entities()
    default_level = hydra.Entity("default_level")
    position = math.Vector3(0.0, 0.0, 0.0)
    default_level.create_entity(position, ["Grid"])
    default_level.get_set_test(0, "Controller|Configuration|Secondary Grid Spacing", 1.0)

    # Create global_skylight entity and set the properties
    global_skylight = hydra.Entity("global_skylight")
    global_skylight.create_entity(
        components=["HDRi Skybox", "Global Skylight (IBL)"], parent_id=default_level.id
    )
    asset_value = hydra.get_asset_by_path(
        os.path.join("LightingPresets", "greenwich_park_02_4k_iblskyboxcm_iblspecular.exr.streamingimage")
    )
    global_skylight.get_set_test(0, "Controller|Configuration|Cubemap Texture", asset_value)
    global_skylight.get_set_test(1, "Controller|Configuration|Diffuse Image", asset_value)
    global_skylight.get_set_test(1, "Controller|Configuration|Specular Image", asset_value)

    # Create ground_plane entity and set the properties
    ground_plane = hydra.Entity("ground_plane")
    scale = math.Vector3(32.0, 32.0, 1.0)
    ground_plane.create_entity(components=["Material"], parent_id=default_level.id)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetLocalScale", ground_plane.id, scale)
    asset_value = hydra.get_asset_by_path(os.path.join("Materials", "Presets", "PBR", "metal_chrome.azmaterial"))
    ground_plane.get_set_test(0, "Default Material|Material Asset", asset_value)
    # Work around to add the correct Atom Mesh component
    mesh_type_id = azlmbr.globals.property.EditorMeshComponentTypeId
    ground_plane.components.append(
        editor.EditorComponentAPIBus(
            bus.Broadcast, "AddComponentsOfType", ground_plane.id, [mesh_type_id]
        ).GetValue()[0]
    )
    asset_value = hydra.get_asset_by_path(os.path.join("Objects", "plane.azmodel"))
    ground_plane.get_set_test(1, "Controller|Configuration|Mesh asset", asset_value)

    # Create directional_light entity and set the properties
    directional_light = hydra.Entity("directional_light")
    position = math.Vector3(0.0, 0.0, 10.0)
    directional_light.create_entity(
        components=["Directional Light"], entity_position=position, parent_id=default_level.id
    )
    rotation = math.Vector3(DEGREE_RADIAN_FACTOR * -90.0, 0.0, 0.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetLocalRotation", directional_light.id, rotation)

    # Create sphere entity and set the properties
    sphere = hydra.Entity("sphere")
    position = math.Vector3(0.0, 0.0, 1.0)
    sphere.create_entity(
        components=["Material"], entity_position=position, parent_id=default_level.id
    )
    asset_value = hydra.get_asset_by_path(
        os.path.join("Materials", "Presets", "PBR", "metal_brass_polished.azmaterial")
    )
    sphere.get_set_test(0, "Default Material|Material Asset", asset_value)
    # Work around to add the correct Atom Mesh component
    sphere.components.append(
        editor.EditorComponentAPIBus(
            bus.Broadcast, "AddComponentsOfType", sphere.id, [mesh_type_id]
        ).GetValue()[0]
    )
    asset_value = hydra.get_asset_by_path(os.path.join("Objects", "sphere.azmodel"))
    sphere.get_set_test(1, "Controller|Configuration|Mesh asset", asset_value)

    # Create camera component and set the properties
    camera = hydra.Entity("camera")
    position = math.Vector3(5.5, -12.0, 9.0)
    camera.create_entity(components=["Camera"], entity_position=position, parent_id=default_level.id)
    rotation = math.Vector3(
        DEGREE_RADIAN_FACTOR * -27.0, DEGREE_RADIAN_FACTOR * -12.0, DEGREE_RADIAN_FACTOR * 25.0
    )
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetLocalRotation", camera.id, rotation)
    camera.get_set_test(0, "Controller|Configuration|Field of view", 60.0)
    hydra.be_this_camera(camera.id)

    # Save level, enter game mode, take screenshot, & exit game mode.
    general.save_level()
    general.idle_wait(0.5)
    general.enter_game_mode()
    general.idle_wait(1.0)
    helper.wait_for_condition(function=lambda: general.is_in_game_mode(), timeout_in_seconds=2.0)
    ScreenshotHelper(general.idle_wait_frames).capture_screenshot_blocking(f"{'AtomBasicLevelSetup'}.ppm")
    general.exit_game_mode()
    helper.wait_for_condition(function=lambda: not general.is_in_game_mode(), timeout_in_seconds=2.0)
    general.log("Basic level created")


if __name__ == "__main__":
    run()