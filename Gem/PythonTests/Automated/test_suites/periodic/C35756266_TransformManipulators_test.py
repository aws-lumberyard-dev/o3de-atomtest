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
from Automated.atom_utils import registry_utils

pytest.importorskip("ly_test_tools")
REG_PATH = os.path.join('Software', 'Amazon', 'Lumberyard', 'Settings')
TEST_DIRECTORY = os.path.dirname(__file__)
EDITOR_TIMEOUT = 30


@pytest.mark.parametrize("project", ["AtomTest"])
@pytest.mark.parametrize("launcher_platform", ['windows_editor'])
class TestAutomation(TestAutomationBase):
    @classmethod
    def setup_class(cls):
        cls.vim_value = registry_utils.get_ly_registry_value(REG_PATH, 'ViewportInteractionModel')
        if cls.vim_value != 1:
            registry_utils.set_ly_registry_value(REG_PATH, 'ViewportInteractionModel', 1)
        cls.show_grid = registry_utils.get_ly_registry_value(REG_PATH, 'ShowGridGuide')
        if cls.show_grid != 0:
            registry_utils.set_ly_registry_value(REG_PATH, 'ShowGridGuide', 0)

    @classmethod
    def teardown_class(cls):
        registry_utils.set_ly_registry_value(REG_PATH, 'ViewportInteractionModel', cls.vim_value)
        registry_utils.set_ly_registry_value(REG_PATH, 'ShowGridGuide', cls.show_grid)

    @pytest.mark.test_case_id('C35756266')
    def test_C35756266_TransformManipulators(self, request, workspace, editor, project, launcher_platform):
        golden_screenshots = [
            os.path.join(os.path.dirname(__file__), 'GoldenImages', 'Windows', 'C35756266_TransformManipulators', 'manipulator_rotation_close.ppm'),
            os.path.join(os.path.dirname(__file__), 'GoldenImages', 'Windows', 'C35756266_TransformManipulators', 'manipulator_rotation_far.ppm'),
            os.path.join(os.path.dirname(__file__), 'GoldenImages', 'Windows', 'C35756266_TransformManipulators', 'manipulator_scale_close.ppm'),
            os.path.join(os.path.dirname(__file__), 'GoldenImages', 'Windows', 'C35756266_TransformManipulators', 'manipulator_scale_far.ppm'),
            os.path.join(os.path.dirname(__file__), 'GoldenImages', 'Windows', 'C35756266_TransformManipulators', 'manipulator_translation_close.ppm'),
            os.path.join(os.path.dirname(__file__), 'GoldenImages', 'Windows', 'C35756266_TransformManipulators', 'manipulator_translation_far.ppm')
        ]

        test_screenshots = [
            os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'manipulator_rotation_close.ppm'),
            os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'manipulator_rotation_far.ppm'),
            os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'manipulator_scale_close.ppm'),
            os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'manipulator_scale_far.ppm'),
            os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'manipulator_translation_close.ppm'),
            os.path.join(workspace.paths.platform_cache(), DEFAULT_SUBFOLDER_PATH, 'manipulator_translation_far.ppm')
        ]

        self.remove_artifacts(test_screenshots)

        expected_lines = [
            "Screenshot taken."
        ]
        unexpected_lines = [
            "Assert",
            "screenshot failed",
            "Traceback (most recent call last):",
        ]

        hydra.launch_and_validate_results(
            request,
            TEST_DIRECTORY,
            editor,
            "C35756266_TransformManipulators_test_case.py",
            timeout=EDITOR_TIMEOUT,
            expected_lines=expected_lines,
            unexpected_lines=unexpected_lines,
            halt_on_unexpected=True,
        )
        for test_screenshot, golden_screenshot in zip(test_screenshots, golden_screenshots):
            self.compare_screenshots(test_screenshot, golden_screenshot)
