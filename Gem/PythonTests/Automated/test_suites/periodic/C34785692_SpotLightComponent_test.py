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

    @pytest.mark.test_case_id('C34785692')
    def test_C34785692_SpotLightComponent(self, request, workspace, editor, project, launcher_platform):
        golden_screenshot_base = os.path.join(os.path.dirname(__file__), 'GoldenImages', 'Windows', 'C34785692_atom_spotlight')
        
        test_screenshot_base = os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'screenshot_C34785692_atom_spotlight')

        golden_screenshots = []
        test_screenshots = []
        for fntail in ('noshadow', 'red', 'redblue', 'redbluegreen'):
            golden_fn = f"{golden_screenshot_base}_{fntail}.ppm"
            golden_screenshots.append(golden_fn)
            print(golden_fn)
            test_fn = f"{test_screenshot_base}_{fntail}.ppm"
            test_screenshots.append(test_fn)
            print(test_fn)

        self.remove_artifacts(test_screenshots)

        expected_lines = [
            "Components found = 1",
            "Component added to entity.",
            "Property list of component is correct.",
            "Color property of spot light is correctly set.",
            "Intensity property of spot light is correctly set.",
            "Cone Angle property of spot light is correctly set.",
            "Enable Shadow property of spot light is correctly set.",
            "Screenshot taken."
        ]
        unexpected_lines = [
            "Assert",
            "Traceback (most recent call last):",
        ]

        hydra.launch_and_validate_results(
            request,
            TEST_DIRECTORY,
            editor,
            "C34785692_SpotLightComponent_test_case.py",
            timeout=EDITOR_TIMEOUT,
            expected_lines=expected_lines,
            unexpected_lines=unexpected_lines,
            halt_on_unexpected=True,
        )

        for index in range(4):
            self.compare_screenshots(test_screenshots[index], golden_screenshots[index])
