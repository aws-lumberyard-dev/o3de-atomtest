#
# All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
# its licensors.
#
# For complete copyright and license terms please see the LICENSE at the root of this
# distribution (the "License"). All use of this software is governed by the License,
# or, if provided, by the license below or the license accompanying this file. Do not
# remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#

ly_get_list_relative_pal_filename(pal_dir ${CMAKE_CURRENT_LIST_DIR}/Platform/${PAL_PLATFORM_NAME})

ly_add_target(
    NAME AtomTest ${PAL_TRAIT_MONOLITHIC_DRIVEN_MODULE_TYPE}
    NAMESPACE Gem
    OUTPUT_NAME Gem.AtomTest.bee705a725b94dcc80b73a49922c8cf0.v0.1.0
    FILES_CMAKE
        atomtest_files.cmake
        ../../atomtest_asset_files.cmake
    INCLUDE_DIRECTORIES
        PUBLIC
            Include
    BUILD_DEPENDENCIES
        PRIVATE
            AZ::AzGameFramework
            Gem::Atom_AtomBridge.Static
)

################################################################################
# Gem dependencies
################################################################################
ly_add_project_dependencies(
    PROJECT_NAME
        AtomTest
    TARGETS 
        AtomTest.GameLauncher
    DEPENDENCIES_FILES 
        runtime_dependencies.cmake
        ${pal_dir}/runtime_dependencies.cmake

)

if(PAL_TRAIT_BUILD_HOST_TOOLS)
    ly_add_project_dependencies(
        PROJECT_NAME
            AtomTest
        TARGETS
            AssetBuilder
            AssetProcessor
            AssetProcessorBatch
            Editor
        DEPENDENCIES_FILES
            tool_dependencies.cmake
            tool_dependencies_${PAL_PLATFORM_NAME_LOWERCASE}.cmake
            ${pal_dir}/tool_dependencies.cmake
    )

endif()
