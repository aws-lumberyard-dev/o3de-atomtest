"""
Copyright (c) Contributors to the Open 3D Engine Project

SPDX-License-Identifier: Apache-2.0 OR MIT

Tests FBX mesh group import scaling by modifying the x, y, z scaling on a list of meshes attached to entities.
Utilizes screenshots & log lines printed from a hydra script to verify test results.
"""

import os
import pytest

from Automated.atom_utils import hydra_test_utils as hydra
from Automated.atom_utils.automated_test_base import DEFAULT_SUBFOLDER_PATH, TestAutomationBase

TEST_DIRECTORY = os.path.dirname(__file__)
EDITOR_TIMEOUT = 30


@pytest.mark.parametrize("project", ["AtomTest"])
@pytest.mark.parametrize("launcher_platform", ['windows_editor'])
class TestAutomation(TestAutomationBase):

    def test_MeshGroupScaling_AllMeshesScaleTheSame(
            self, request, workspace, editor, project, launcher_platform, golden_images_directory):
        """
        Please review the hydra script run by this test for more specific test info.
        Tests that FBX group meshes scale correctly.
        """
        golden_screenshot = os.path.join(golden_images_directory, 'Windows', 'FBXMeshGroupImportScaling.ppm')
        test_screenshot = os.path.join(
            workspace.paths.engine_root(), project, DEFAULT_SUBFOLDER_PATH,
            "screenshot_atom_FBXMeshGroupImportScaling.dds")
        self.remove_artifacts([test_screenshot])

        expected_lines = ["FBX mesh group scaling test has completed."]
        unexpected_lines = [
            "Trace::Assert",
            "Trace::Error",
            "Traceback (most recent call last):",
        ]

        hydra.launch_and_validate_results(
            request,
            TEST_DIRECTORY,
            editor,
            "MeshGroupImporting_test_case.py",
            timeout=EDITOR_TIMEOUT,
            expected_lines=expected_lines,
            unexpected_lines=unexpected_lines,
            halt_on_unexpected=True,
        )

        self.compare_screenshots(test_screenshot, golden_screenshot)
