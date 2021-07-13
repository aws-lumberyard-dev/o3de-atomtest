"""
Copyright (c) Contributors to the Open 3D Engine Project

SPDX-License-Identifier: Apache-2.0 OR MIT

Tests the Physical Sky component inside the Editor.
Utilizes screenshots & log lines printed from a hydra script to verify test results.
"""

import pytest
import os

from Automated.atom_utils import hydra_test_utils as hydra
from Automated.atom_utils.automated_test_base import TestAutomationBase
from Automated.atom_utils.automated_test_base import DEFAULT_SUBFOLDER_PATH

TEST_DIRECTORY = os.path.dirname(__file__)
EDITOR_TIMEOUT = 30


@pytest.mark.parametrize("project", ["AtomTest"])
@pytest.mark.parametrize("launcher_platform", ['windows_editor'])
class TestAutomation(TestAutomationBase):

    def test_PhysicalSkyComponent_DisplaysModifiedProperties(
            self, request, workspace, editor, project, launcher_platform, golden_images_directory):
        """
        Please review the hydra script run by this test for more specific test info.
        Tests that the Physical Sky component functionality is maintained within the Editor.
        """
        golden_screenshot = os.path.join(golden_images_directory, 'Windows', 'PhysicalSkyComponent.ppm')
        test_screenshot = os.path.join(
            workspace.paths.engine_root(), project, DEFAULT_SUBFOLDER_PATH, 'screenshot_atom_PhysicalSkyComponent.ppm')
 
        self.remove_artifacts([test_screenshot])
 
        expected_lines = [
            "Entity successfully created.",
            "Components found = 1",
            "Component added to entity.",
            "Property list of component is correct.",
            "Sky Intensity is correctly set",
            "Sun Intensity is correctly set",
            "Turbidity is correctly set",
            "Sun Radius is correctly set",
            "Screenshot taken."
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
            "PhysicalSkyComponent_test_case.py",
            timeout=EDITOR_TIMEOUT,
            expected_lines=expected_lines,
            unexpected_lines=unexpected_lines,
            halt_on_unexpected=True,
        )
        self.compare_screenshots(test_screenshot, golden_screenshot)
