"""
All or portions of this file Copyright (c) Amazon.com, Inc. or its affiliates or
its licensors.
​
For complete copyright and license terms please see the LICENSE at the root of this
distribution (the "License"). All use of this software is governed by the License,
or, if provided, by the license below or the license accompanying this file. Do not
remove or modify any license notices. This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
# NOTE: Be careful running this test as it GREATLY increases the time for all tests to complete.
# This is because it swaps between AtomTest and AtomSampleViewer projects and tries to re-process ALL assets for both.
# It will be updated in ATOM-14758 in the future to either be removed or not take as long to run.
# For now, we will skip it, to not block Automated Review verifications.

import logging
import os
import pytest
import shutil

pytestmark = pytest.mark.skip  # See ATOM-14758

pytest.importorskip("ly_test_tools")

import ly_test_tools.environment.waiter as waiter

logger = logging.getLogger(__name__)

LOG_MONITOR_INTERVAL = 0.1  # seconds
LOG_MONITOR_TIMEOUT = 8000  # seconds
TEST_DIRECTORY = os.path.dirname(__file__)


class FailedAssets:
    failed_assets = []


def find_lines(log, log_finished_line, error_line="AssetProcessor~~Failed"):
    for line in log:
        line = line[:-1]
        if error_line in line:
            logger.debug(line)
            FailedAssets.failed_assets.append(line)
        if log_finished_line in line:
            return True
        return False


@pytest.mark.parametrize("project", ["AtomTest"])
@pytest.mark.parametrize("launcher_platform", ["windows_editor"])
class TestAssetProcessorProcessAssets(object):
    @pytest.fixture(autouse=True)
    def setup_teardown(self, request, workspace, editor, project):
        self.ap_gui_log = os.path.join(editor.workspace.paths.build_directory(), "logs", "AP_GUI.log")
        if os.path.exists(self.ap_gui_log):
            os.remove(self.ap_gui_log)
        # Reset Bootstrap.cfg to AtomTest project
        workspace.settings.modify_bootstrap_setting("sys_game_folder", "AtomTest")

    @pytest.mark.test_case_id("C34583161")
    def test_asset_processor(self, request, editor, workspace, project, launcher_platform):
        # Clear Cache
        shutil.rmtree(os.path.join(editor.workspace.paths.dev(), "Cache"), ignore_errors=True)
        shutil.rmtree(os.path.join(editor.workspace.paths.build_directory(), "logs"), ignore_errors=True)
        if os.getcwd() != editor.workspace.paths.dev():
            os.chdir(editor.workspace.paths.dev())
        log_finished_line = 'AssetProcessor~~Processed "bootstrap.cfg"'

        # Launch Editor, Check failed assets and list out failed assets
        with editor.start():
            try:
                with open(self.ap_gui_log, mode="r") as log:
                    waiter.wait_for(
                        lambda: find_lines(log, log_finished_line),
                        timeout=LOG_MONITOR_TIMEOUT,
                        interval=LOG_MONITOR_INTERVAL,
                    )
            except (OSError, FileNotFoundError) as e:
                logger.error(f"Failed to find {log_finished_line} with in {LOG_MONITOR_TIMEOUT} seconds")
                raise e
            finally:
                assert not FailedAssets.failed_assets, f"Failed assets found: {FailedAssets.failed_assets}"

    @pytest.mark.test_case_id("C34583163")
    def test_asset_processor_addasset(self, request, editor, workspace, project, launcher_platform):
        # Make sure Asset Processor has been run and all assets are processed
        with editor.start():
            log_finished_line_ap = 'AssetProcessor~~Processed "bootstrap.cfg"'
            FailedAssets.failed_assets = []
            try:
                with open(self.ap_gui_log, mode="r") as log:
                    waiter.wait_for(
                        lambda: find_lines(log, log_finished_line_ap),
                        timeout=LOG_MONITOR_TIMEOUT,
                        interval=LOG_MONITOR_INTERVAL,
                    )
            except (OSError, FileNotFoundError) as e:
                logger.error(f"Failed to find {log_finished_line_ap} with in {LOG_MONITOR_TIMEOUT} seconds")
                raise e
            finally:
                assert not FailedAssets.failed_assets, f"Failed assets found: {FailedAssets.failed_assets}"

            # Adding new asset in Asset Processor
            asset_file_path = os.path.join(
                editor.workspace.paths.dev(),
                "AtomTest",
                "Gem",
                "PythonTests",
                "Automated",
                "TestAssets",
                "Blue_gradient.png",
            )
            default_materials_path = os.path.join(editor.workspace.paths.dev(), "AtomTest", "Materials", "Default")

            if not os.path.exists(asset_file_path) or not os.path.exists(default_materials_path):
                raise OSError(
                    f"Failed to find asset file paths - asset_file_path: {asset_file_path} - "
                    f"default_materials_path: {default_materials_path}"
                )

            # Make sure newly added asset is processed by Asset Processor
            try:
                shutil.move(asset_file_path, default_materials_path)
                with open(self.ap_gui_log, mode="r") as log:
                    log_finished_line_asset = 'AssetProcessor~~Processed "Materials/Default/Blue_gradient.png"'
                    waiter.wait_for(
                        lambda: find_lines(log, log_finished_line_asset),
                        timeout=LOG_MONITOR_TIMEOUT,
                        interval=LOG_MONITOR_INTERVAL,
                    )

            except (OSError, FileNotFoundError, IOError) as e:
                logger.error(f"Failed to find {log_finished_line_asset} with in {LOG_MONITOR_TIMEOUT} seconds")
                raise e
            finally:
                shutil.move(
                    os.path.join(
                        editor.workspace.paths.dev(), "AtomTest", "Materials", "Default", "Blue_gradient.png"),
                    os.path.join(
                        editor.workspace.paths.dev(), "AtomTest", "Gem", "PythonTests", "Automated", "TestAssets"
                    ),
                )
                assert not FailedAssets.failed_assets, f"Failed assets found: {FailedAssets.failed_assets}"

    @pytest.mark.test_case_id("C34583162")
    def test_asset_processor_clearcache(self, request, editor, workspace, project, launcher_platform):
        log_finished_line = 'AssetProcessor~~Processed "bootstrap.cfg"'

        # Make sure Asset Processor has been run and all assets are processed
        with editor.start():
            FailedAssets.failed_assets = []
            try:
                with open(self.ap_gui_log, mode="r") as log:
                    waiter.wait_for(
                        lambda: find_lines(log, log_finished_line),
                        timeout=LOG_MONITOR_TIMEOUT,
                        interval=LOG_MONITOR_INTERVAL,
                    )
            except (OSError, FileNotFoundError) as e:
                logger.error(f"Failed to find {log_finished_line} with in {LOG_MONITOR_TIMEOUT} seconds")
                raise e
            finally:
                assert not FailedAssets.failed_assets, f"Failed assets found: {FailedAssets.failed_assets}"

        # Clear Cache
        shutil.rmtree(os.path.join(editor.workspace.paths.dev(), "Cache"), ignore_errors=True)
        shutil.rmtree(os.path.join(editor.workspace.paths.build_directory(), "logs"), ignore_errors=True)
        if os.getcwd() != editor.workspace.paths.dev():
            os.chdir(editor.workspace.paths.dev())

        # Launch Editor, Check failed assets and list out failed assets
        with editor.start():
            FailedAssets.failed_assets = []
            try:
                with open(self.ap_gui_log, mode="r") as log:
                    waiter.wait_for(
                        lambda: find_lines(log, log_finished_line),
                        timeout=LOG_MONITOR_TIMEOUT,
                        interval=LOG_MONITOR_INTERVAL,
                    )
            except (OSError, FileNotFoundError) as e:
                logger.error(f"Failed to find {log_finished_line} with in {LOG_MONITOR_TIMEOUT} seconds")
                raise e
            finally:
                assert not FailedAssets.failed_assets, f"Failed assets found: {FailedAssets.failed_assets}"

    @pytest.mark.test_case_id("C34682400")
    def test_asset_processor_atomsampleviewer(self, request, editor, workspace, project, launcher_platform):
        # Set Bootstrap.cfg to AtomSampleViewer project
        workspace.settings.modify_bootstrap_setting("sys_game_folder", "AtomSampleViewer")

        # Clear Cache
        shutil.rmtree(os.path.join(editor.workspace.paths.dev(), "Cache"), ignore_errors=True)
        shutil.rmtree(os.path.join(editor.workspace.paths.build_directory(), "logs"), ignore_errors=True)
        if os.getcwd() != editor.workspace.paths.dev():
            os.chdir(editor.workspace.paths.dev())
        log_finished_line = 'AssetProcessor~~Processed "bootstrap.cfg"'

        # Launch Editor, Check failed assets and list out failed assets
        with editor.start():
            try:
                with open(self.ap_gui_log, mode="r") as log:
                    waiter.wait_for(
                        lambda: find_lines(log, log_finished_line),
                        timeout=LOG_MONITOR_TIMEOUT,
                        interval=LOG_MONITOR_INTERVAL,
                    )
            except (OSError, FileNotFoundError) as e:
                logger.error(f"Failed to find {log_finished_line} with in {LOG_MONITOR_TIMEOUT} seconds")
                raise e
            finally:
                assert not FailedAssets.failed_assets, f"Failed assets found: {FailedAssets.failed_assets}"
