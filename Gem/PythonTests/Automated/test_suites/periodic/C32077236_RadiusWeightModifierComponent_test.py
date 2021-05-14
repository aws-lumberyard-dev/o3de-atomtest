"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.

For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

import pytest
import os

from Automated.atom_utils import hydra_test_utils as hydra
from Automated.atom_utils.automated_test_base import TestAutomationBase
from Automated.atom_utils.automated_test_base import DEFAULT_SUBFOLDER_PATH

pytest.importorskip("ly_test_tools")
TEST_DIRECTORY = os.path.dirname(__file__)
EDITOR_TIMEOUT = 30


@pytest.mark.parametrize("project", ["AtomTest"])
@pytest.mark.parametrize("launcher_platform", ['windows_editor'])
class TestAutomation(TestAutomationBase):

    @pytest.mark.test_case_id('C32077236')
    def test_C32077236_RadiusWeightModifierComponent(
            self, request, workspace, editor, project, launcher_platform, golden_images_directory):
        golden_screenshots = [
            os.path.join(golden_images_directory, 'Windows', 'RadiusWeightModifierComponent_FullExposure.ppm'),
            os.path.join(golden_images_directory, 'Windows', 'RadiusWeightModifierComponent_HalfExposure.ppm'),
            os.path.join(golden_images_directory, 'Windows', 'RadiusWeightModifierComponent_NoExposure.ppm'),
        ]

        test_screenshots = [
            os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'screenshot_atom_RadiusWeightModifierComponent_FullExposure.ppm'),
            os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'screenshot_atom_RadiusWeightModifierComponent_HalfExposure.ppm'),
            os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'screenshot_atom_RadiusWeightModifierComponent_NoExposure.ppm')
        ]

        self.remove_artifacts(test_screenshots)

        expected_lines = [
            "Radius Weight Modifier Component added to entity.",
            "Property list of component is correct.",
            "Radius property of radius weight modifier is correctly set",
            "Three screenshots taken."
        ]
        unexpected_lines = [
            "Assert",
            "Model material asset property of material is not correctly set",
            "Traceback (most recent call last):",
        ]

        hydra.launch_and_validate_results(
            request,
            TEST_DIRECTORY,
            editor,
            "C32077236_RadiusWeightModifierComponent_test_case.py",
            timeout=EDITOR_TIMEOUT,
            expected_lines=expected_lines,
            unexpected_lines=unexpected_lines,
            halt_on_unexpected=True,
        )
        for test_screenshot, golden_screenshot in zip(test_screenshots, golden_screenshots):
            self.compare_screenshots(test_screenshot, golden_screenshot)
