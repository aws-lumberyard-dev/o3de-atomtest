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

    @pytest.mark.test_case_id('C32078120')
    def test_C32078120_DirectionalLightComponent(
            self, request, workspace, editor, project, launcher_platform, golden_images_directory):
        golden_screenshot_base = os.path.join(
            golden_images_directory, 'Windows', 'C32078120_atom_directionallight')
        
        test_screenshot_base = os.path.join(workspace.paths.engine_root(), project, DEFAULT_SUBFOLDER_PATH, 'screenshot_C32078120_atom_directionallight')
        
        golden_screenshots = []
        test_screenshots = []
        for fntail in ('nofilter', 'manualcascade', 'autocascade', 'pcflow', 'pcfhigh', 'esm', '2ndlight'):
            golden_fn = f"{golden_screenshot_base}_{fntail}.ppm"
            golden_screenshots.append(golden_fn)
            print(golden_fn)
            test_fn = f"{test_screenshot_base}_{fntail}.ppm"
            test_screenshots.append(test_fn)
            print(test_fn)

        self.remove_artifacts(test_screenshots)

        expected_lines = [
            'Entity for directional light is successfully created.',
            'Components found = 1',
            'Component added to entity.',
            'Property list of component is correct.',
            'Color property of light is correctly set.',
            'Intensity of light is correctly set.',
            'Cascade Count of light is correctly set.',
            'Split Automatic of light is correctly set.',
            'Far Depth Cascade of light is correctly set.',
            'Enable Debug Color of light is correctly set.',
            'Split Ratio of light is correctly set.',
            'Filter Method of light is correctly set.',
            'Boundary Width of light is correctly set.',
            'Prediction Sample Count of light is correctly set.',
            'Entity for second directional light is successfully created.',
            'Screenshot taken.'
        ]
        unexpected_lines = [
            "Trace::Assert",
            "Trace::Error",
            "Traceback (most recent call last):",
        ]

        hydra.launch_and_validate_results(
            request,
            TEST_DIRECTORY,
            editor,
            "C32078120_DirectionalLightComponent_test_case.py",
            timeout=EDITOR_TIMEOUT,
            expected_lines=expected_lines,
            unexpected_lines=unexpected_lines,
            halt_on_unexpected=True,
        )

        for index in range(len(golden_screenshots)):
            self.compare_screenshots(test_screenshots[index], golden_screenshots[index])
