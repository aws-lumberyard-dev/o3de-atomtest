"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
# Test case ID : C30993189
# Test Case Title : Mesh
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/30993189

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
    'Controller|Configuration|Mesh Asset',
    'Controller|Configuration|Sort Key',
    'Controller|Configuration|Lod Override',
    'Controller|Configuration|Exclude from reflection cubemaps'
]

class Tests():
    pass

def run():
    # open test level
    helper.init_idle()
    helper.open_level("MeshTest")

    # Create new entity
    myEntityId = azlmbr.editor.ToolsApplicationRequestBus(azlmbr.bus.Broadcast, 'CreateNewEntity', EntityId())
    azlmbr.editor.EditorEntityAPIBus(azlmbr.bus.Event, 'SetName', myEntityId, "Mesh")
    vec3 = azlmbr.math.Vector3(4.0, 2.0, 0.0)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", myEntityId, vec3)
    if myEntityId.IsValid():
        general.log("Entity successfully created.")

    # Attach the component
    typeIdsList = [azlmbr.globals.property.EditorMeshComponentTypeId]
    componentOutcome = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'AddComponentsOfType', myEntityId, typeIdsList)
    if componentOutcome.IsSuccess():
        general.log("Component added to entity.")
    # save a reference to the component
    component = componentOutcome.GetValue()[0]

    # verify property list of component
    helper.compare_property_list(component, COMPONENT_PROPERTIES)
    # Set component properties
    mesh_asset_property_path = 'Controller|Configuration|Mesh Asset'
    sort_key_property_path = 'Controller|Configuration|Sort Key'
    lod_override_property_path = 'Controller|Configuration|Lod Override'
    exclude_from_reflection_cubemaps_value = True
    exclude_from_reflection_cubemaps_property_path = 'Controller|Configuration|Reflections|Exclude from reflection cubemaps'
    mesh_asset_filepath = 'objects/lucy/lucy_low.azmodel'
    mesh_asset_id = azlmbr.asset.AssetCatalogRequestBus(azlmbr.bus.Broadcast, 'GetAssetIdByPath', mesh_asset_filepath, azlmbr.math.Uuid(), False)
    mesh_asset_path =  azlmbr.asset.AssetCatalogRequestBus(azlmbr.bus.Broadcast, 'GetAssetPathById', mesh_asset_id)

    # check if the asset path is valid
    if mesh_asset_path != None:
        general.log("Mesh asset for mesh component is valid.")

    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, mesh_asset_property_path, mesh_asset_id)
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, sort_key_property_path, 10)
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, lod_override_property_path, 0)
    azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, exclude_from_reflection_cubemaps_property_path, exclude_from_reflection_cubemaps_value)

    # verify that component contains the expected values
    asset_id = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, mesh_asset_property_path)
    if asset_id.GetValue().to_string() == mesh_asset_id.to_string():
        general.log("Mesh asset property of mesh is correctly set")
    sort_key = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, sort_key_property_path)
    if sort_key.GetValue() == 10:
        general.log("Sort key property of mesh is correctly set")
    lod_override = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, lod_override_property_path)
    if lod_override.GetValue() == 0:
        general.log("Lod override property of mesh is correctly set")
    exposure = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, exclude_from_reflection_cubemaps_property_path)
    if exposure.GetValue() == exclude_from_reflection_cubemaps_value:
        general.log("Exclude from reflection cubemaps property of mesh is correctly set")

    # generate screenshot to compare with golden
    ScreenshotHelper(general.idle_wait_frames).capture_screenshot_blocking_in_game_mode('screenshot_atom_MeshComponent.ppm')
    helper.close_editor()


if __name__ == "__main__":
    run()
