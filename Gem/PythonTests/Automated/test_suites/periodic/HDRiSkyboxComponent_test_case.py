"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test case ID : C30993187
# Test Case Title : HDRi Skybox
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/30993187

import os
import sys

import azlmbr.editor
import azlmbr.legacy.general as general
import azlmbr.paths
from azlmbr.entity import EntityId

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.screenshot_utils import ScreenshotHelper

COMPONENT_PROPERTIES = [
    'Controller',
    'Controller|Configuration',
    'Controller|Configuration|Cubemap Texture',
    'Controller|Configuration|Exposure'
]


class Tests():
    pass

def run():


    # open pre-made level without hdr skybox component
    helper.init_idle()
    helper.open_level("MeshTest")

    # Create new entity
    myEntityId = azlmbr.editor.ToolsApplicationRequestBus(azlmbr.bus.Broadcast, 'CreateNewEntity', EntityId())
    azlmbr.editor.EditorEntityAPIBus(azlmbr.bus.Event, 'SetName', myEntityId, "Skybox")
    if myEntityId.IsValid():
        general.log("Entity successfully created.")

    # Attach skybox component
    component = helper.attach_component_to_entity(myEntityId, 'HDRi Skybox')

    # verify property list of component
    helper.compare_property_list(component, COMPONENT_PROPERTIES)

    # Set component properties
    exposure_property_path = 'Controller|Configuration|Exposure'
    exposure_value = 1
    cubemap_property_path = 'Controller|Configuration|Cubemap Texture'
    texture_filepath = 'lightingpresets/lowcontrast/artist_workshop_4k_iblskyboxcm.exr.streamingimage'
    texture_asset_id = azlmbr.asset.AssetCatalogRequestBus(azlmbr.bus.Broadcast, 'GetAssetIdByPath', texture_filepath, azlmbr.math.Uuid(), False)
    texture_asset_path =  azlmbr.asset.AssetCatalogRequestBus(azlmbr.bus.Broadcast, 'GetAssetPathById', texture_asset_id)
    # check if the texture path is valid
    if texture_asset_path != None:
        general.log("Cubemap texture for skybox component is valid.")
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, cubemap_property_path, texture_asset_id)
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, exposure_property_path, exposure_value)

    # verify that skybox component contains the expected values
    asset_id = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, cubemap_property_path)
    if asset_id.GetValue().to_string() == texture_asset_id.to_string():
        general.log("Cubemap property of skybox is correctly set")
    exposure = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, exposure_property_path)
    if exposure.GetValue() == exposure_value:
        general.log("Exposure property of skybox is correctly set")

    # generate screenshot and compare with golden
    ScreenshotHelper(general.idle_wait_frames).capture_screenshot_blocking_in_game_mode('screenshot_atom_HDRiSkyboxComponent.ppm')
    helper.close_editor()


if __name__ == "__main__":
    run()
