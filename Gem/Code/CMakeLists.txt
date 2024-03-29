#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#

ly_get_list_relative_pal_filename(pal_dir ${CMAKE_CURRENT_LIST_DIR}/Platform/${PAL_PLATFORM_NAME})

ly_add_target(
    NAME AtomTest ${PAL_TRAIT_MONOLITHIC_DRIVEN_MODULE_TYPE}
    NAMESPACE Gem
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

# if enabled, AtomTest gem is used by the Client and Server Launchers as well as Tools
# But it isn't needed in Builders
ly_create_alias(NAME AtomTest.Clients NAMESPACE Gem TARGETS Gem::AtomTest)
ly_create_alias(NAME AtomTest.Servers NAMESPACE Gem TARGETS Gem::AtomTest)
ly_create_alias(NAME AtomTest.Tools   NAMESPACE Gem TARGETS Gem::AtomTest)

################################################################################
# Gem dependencies
################################################################################

ly_enable_gems(PROJECT_NAME AtomTest GEM_FILE enabled_gems.cmake)

# If we build a server, then apply the gems to the server
if(PAL_TRAIT_BUILD_SERVER_SUPPORTED)
    set_property(GLOBAL APPEND PROPERTY LY_LAUNCHER_SERVER_PROJECTS AtomTest)
endif()
