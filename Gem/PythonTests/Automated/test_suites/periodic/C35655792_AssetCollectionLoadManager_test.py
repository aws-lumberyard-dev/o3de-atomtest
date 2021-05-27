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

pytest.importorskip("ly_test_tools")

from Automated.atom_utils import hydra_test_utils as hydra
from Automated.atom_utils.automated_test_base import TestAutomationBase

TEST_DIRECTORY = os.path.dirname(__file__)
EDITOR_TIMEOUT = 30


@pytest.mark.parametrize("project", ["AtomTest"])
@pytest.mark.parametrize("launcher_platform", ['windows_editor'])
class TestAutomation(TestAutomationBase):
    def test_C35655792_AssetCollectionAsyncLoader(self, request, workspace, editor, project, launcher_platform):
        expected_lines = [
            "Entity successfully created.",
            "SUCCESS: Assets were queued for loading.",
            "SUCCESS: Pending list contains the same asset paths as the original list",
            "SUCCESS: No asset was available",
            "SUCCESS: Cancelled an impossible job",
            "SUCCESS: The AssetCollectionAsyncLoader loaded all requested assets.",
            "SUCCESS: The AssetCollectionAsyncLoader PASSED the test"
        ]
        unexpected_lines = [
            "Trace::Assert",
            "Trace::Error",
            "Traceback (most recent call last):",
            "ERROR: Was expecting 0 pending assets",
            "ERROR: Failed to submit assets for asynchronous loading.",
            "ERROR: Was expecting the same list size.",
            "ERROR: Asset is not present in the pending list:",
            "ERROR: Asset should not be available:",
            "ERROR: Failed to copy temp source asset",
            "ERROR: Failed to load assets asynchronously",
            "ERROR: Asset should be available:",
        ]

        hydra.launch_and_validate_results(
            request,
            TEST_DIRECTORY,
            editor,
            "C35655792_AssetCollectionLoadManager_test_case.py",
            timeout=EDITOR_TIMEOUT,
            expected_lines=expected_lines,
            unexpected_lines=unexpected_lines,
            halt_on_unexpected=True,
        )
