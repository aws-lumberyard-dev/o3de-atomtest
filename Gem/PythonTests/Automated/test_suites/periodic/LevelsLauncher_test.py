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
# This test is temporarily disabled because it takes too long to run.
# See ATOM-14758 for more info.
pytestmark = pytest.mark.skip

# Bail on the test if ly_test_tools doesn't exist.
pytest.importorskip("ly_test_tools")
from Automated.atom_utils import hydra_test_utils as hydra
from ly_remote_console.remote_console_commands import RemoteConsole as RemoteConsole

log_monitor_timeout = 30


@pytest.mark.parametrize("project", ["AtomTest"])
class TestLevelsLauncher(object):
    @pytest.fixture
    def remote_console_instance(self, request):
        console = RemoteConsole()

        def teardown():
            if console.connected:
                console.stop()

        request.addfinalizer(teardown)
        return console

    @pytest.mark.test_case_id(
        "C34448165",
        "C34448166",
        "C34448167",
        "C34448168",
        "C34448169",
        "C34448170",
        "C34448171",
        "C34448172",
        "C34448173",
        "C34448174",
        "C34448175",
        "C34448176",
        "C34448177",
    )
    @pytest.mark.parametrize(
        "level",
        [
            "ActorTest_100Actors",
            "ActorTest_MultipleActors",
            "ActorTest_SingleActor",
            "ColorSpaceTest",
            "DefaultLevel",
            "Lucy",
            "lucy_high",
            "macbeth_shaderballs",
            "MeshTest",
            "NormalMapping",
            "PbrMaterialChart",
            "ShadowTest",
            "TangentSpace",
        ],
    )
    def test_LevelsLauncher(
        self, request, launcher, workspace, project, level, remote_console_instance
    ):
        expected_lines = []
        unexpected_lines = [
            "Error",
            "Assert",
            "Traceback (most recent call last):",
        ]

        hydra.launch_and_validate_results_launcher(
            launcher,
            level,
            remote_console_instance,
            expected_lines,
            unexpected_lines=unexpected_lines,
            log_monitor_timeout=log_monitor_timeout,
        )
