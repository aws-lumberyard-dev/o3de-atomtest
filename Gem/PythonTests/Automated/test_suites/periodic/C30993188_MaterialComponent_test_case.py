"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# Test case ID : C30993188
# Test Case Title : Material
# URL of the test case : https://testrail.agscollab.com/index.php?/cases/view/30993188

import os
import sys

import azlmbr.editor
import azlmbr.legacy.general as general
import azlmbr.paths

sys.path.append(os.path.join(azlmbr.paths.devroot, "AtomTest", "Gem", "PythonTests"))

from Automated.atom_utils.automated_test_utils import TestHelper as helper
from Automated.atom_utils.screenshot_utils import ScreenshotHelper
from Automated.atom_utils.hydra_editor_utils import helper_create_entity_with_mesh


COMPONENT_PROPERTIES = [
    'Message',
    'Enable LOD Materials',
    'LOD Materials|LOD 0|[2]',
    'LOD Materials|LOD 0',
    'LOD Materials|LOD 0|[0]',
    'Model Materials|[2]|Material Asset',
    'Model Materials|[3]|Material Asset',
    'LOD Materials',
    'LOD Materials|LOD 0|[1]|Material Asset',
    'LOD Materials|LOD 0|[3]|Material Asset',
    'Model Materials|[1]|Material Asset',
    'Model Materials|[4]',
    'LOD Materials|LOD 0|[0]|Material Asset',
    'LOD Materials|LOD 0|[2]|Material Asset',
    'Model Materials',
    'LOD Materials|LOD 0|[1]',
    'Default Material',
    'Default Material|Material Asset',
    'Model Materials|[0]',
    'Model Materials|[1]',
    'Model Materials|[3]',
    'Model Materials|[4]|Material Asset',
    'LOD Materials|LOD 0|[3]',
    'Controller',
    'Controller|Materials',
    'Model Materials|[0]|Material Asset',
    'Model Materials|[2]',
    'LOD Materials|LOD 0|[4]',
    'LOD Materials|LOD 0|[4]|Material Asset'
]

def create_entity_with_3_lod_model(offset):
    mesh_asset_filepath = 'objects/test/bevelcube_lod_multi-material_1m.azmodel'
    entityId = helper_create_entity_with_mesh(mesh_asset_filepath)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", entityId, offset)
    return entityId

def generate_material_asset_ids(material_asset_filepaths):
    return [azlmbr.asset.AssetCatalogRequestBus(azlmbr.bus.Broadcast, 'GetAssetIdByPath', filepath, azlmbr.math.Uuid(),
                                            False) for filepath in material_asset_filepaths]

def set_and_test_material_property_path(component, model_asset_id_list, property_path_list):
    for asset_id, property_path in zip(model_asset_id_list, property_path_list):
        azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'SetComponentProperty', component, property_path, asset_id)

    general.idle_wait_frames(120)

    for asset_id, property_path in zip(model_asset_id_list, property_path_list):
        current_asset_id = azlmbr.editor.EditorComponentAPIBus(azlmbr.bus.Broadcast, 'GetComponentProperty', component, property_path)
        if current_asset_id.GetValue().to_string() != asset_id.to_string():
            return False

    return True


class Tests():
    pass

def run():
    # open pre-made level
    helper.init_idle()
    helper.open_level("MeshTest")

    # create mesh
    mesh_asset_filepath = 'testdata/multi-mat_fbx/multi-mat_mesh-groups_1m_cubes.azmodel'
    offset = azlmbr.math.Vector3(4.5, 3.0, 0.0)
    myEntityId = helper_create_entity_with_mesh(mesh_asset_filepath)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", myEntityId, offset)
    if myEntityId.IsValid():
        general.log("Entity successfully created.")
        
    # attach material
    component = helper.attach_component_to_entity(myEntityId, 'Material')

    # verify property list
    general.idle_wait_frames(120)
    helper.compare_property_list(component, COMPONENT_PROPERTIES)
  
    material_asset_filepaths = [
        'materials/basic_grey.azmaterial',
        'materials/defaultpbr.azmaterial',
        'materials/defaultpbrtransparent.azmaterial',
        'materials/defaultpbr.azmaterial',
        'materials/basic_grey.azmaterial'
    ]
    material_asset_ids = generate_material_asset_ids(material_asset_filepaths)
    model_asset_property_paths = [f'Model Materials|[{i}]|Material Asset' for i in range(5)]
    if not set_and_test_material_property_path(component, material_asset_ids, model_asset_property_paths):
        general.log("Model material asset property of material is not correctly set")

    # generate screenshot to compare with golden
    screenshotHelper = ScreenshotHelper(general.idle_wait_frames)
    screenshotHelper.capture_screenshot_blocking_in_game_mode('screenshot_atom_MaterialComponent.ppm')

    ####### Test LoD materials ######
    offset = azlmbr.math.Vector3(4.3, 1.45, 1.2)
    entityId = create_entity_with_3_lod_model(offset)
    component = helper.attach_component_to_entity(entityId, 'Material')
    general.idle_wait_frames(120)

    material_asset_filepaths = [
        'materials/red.azmaterial',
        'materials/blue.azmaterial',
        'materials/green.azmaterial',
    ]
    material_asset_ids = generate_material_asset_ids(material_asset_filepaths)
    model_asset_property_paths = [f'LOD Materials|LOD {i}|[0]|Material Asset' for i in range(3)]
    if not set_and_test_material_property_path(component, material_asset_ids, model_asset_property_paths):
        general.log("LOD material asset property of material is not correctly set")

    # screenshot test for each LOD
    cameraEntityId = helper.find_entities('Camera')[0]
    screenshotHelper.capture_screenshot_blocking_in_game_mode('screenshot_atom_MaterialComponent_Lod2.ppm')
    new_position = azlmbr.math.Vector3(4.51, -1.0, 1.13)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", cameraEntityId, new_position)
    screenshotHelper.capture_screenshot_blocking_in_game_mode('screenshot_atom_MaterialComponent_Lod1.ppm')
    new_position = azlmbr.math.Vector3(4.28, 0.35, 1.16)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", cameraEntityId, new_position)
    screenshotHelper.capture_screenshot_blocking_in_game_mode('screenshot_atom_MaterialComponent_Lod0.ppm')

    ####### Test default material ######
    offset = azlmbr.math.Vector3(4.3, 1.45, 2.4)
    entityId = create_entity_with_3_lod_model(offset)
    component = helper.attach_component_to_entity(entityId, 'Material')
    general.idle_wait_frames(120)

    material_asset_filepath = ['materials/white.azmaterial']
    material_asset_id = generate_material_asset_ids(material_asset_filepath)
    model_asset_property_path = ['Default Material|Material Asset']
    if not set_and_test_material_property_path(component, material_asset_id, model_asset_property_path):
        general.log("Default material asset property of material is not correctly set")

    new_position = azlmbr.math.Vector3(4.28, 0.0, 2.43)
    azlmbr.components.TransformBus(azlmbr.bus.Event, "SetWorldTranslation", cameraEntityId, new_position)
    screenshotHelper.capture_screenshot_blocking_in_game_mode('screenshot_atom_MaterialComponent_default.ppm')
    helper.close_editor()

if __name__ == "__main__":
    run()