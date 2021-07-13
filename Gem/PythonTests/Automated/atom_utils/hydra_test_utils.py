"""
Copyright (c) Contributors to the Open 3D Engine Project

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import logging
import os

import ly_test_tools.log.log_monitor
import ly_test_tools.environment.process_utils as process_utils
import ly_test_tools.environment.waiter as waiter
from .network_utils import check_for_listening_port
from ly_remote_console.remote_console_commands import (
    send_command_and_expect_response as send_command_and_expect_response,
)

logger = logging.getLogger(__name__)


def teardown_editor(editor):
    """
    :param editor: Configured editor object
    :return:
    """
    process_utils.kill_processes_named("AssetProcessor.exe")
    logger.debug("Ensuring Editor is stopped")
    editor.ensure_stopped()


def launch_and_validate_results(
    request,
    test_directory,
    editor,
    editor_script,
    expected_lines,
    unexpected_lines=[],
    halt_on_unexpected=False,
    log_file_name="Editor.log",
    cfg_args=[],
    timeout=60,
):
    """
    Creates a temporary config file for Hydra execution, runs the Editor with the specified script, and monitors for
    expected log lines.
    :param request: Special fixture providing information of the requesting test function.
    :param test_directory: Path to test directory that editor_script lives in.
    :param editor: Configured editor object to run test against.
    :param editor_script: Name of script that will execute in the Editor.
    :param expected_lines: Expected lines to search log for.
    :param unexpected_lines: Unexpected lines to search log for. Defaults to none.
    :param halt_on_unexpected: Halts test if unexpected lines are found. Defaults to False.
    :param log_file_name: Name of the log file created by the editor. Defaults to 'Editor.log'
    :param cfg_args: Additional arguments for CFG, such as LevelName.
    :param timeout: Length of time for test to run. Default is 60.
    """
    test_case = os.path.join(test_directory, editor_script)
    request.addfinalizer(lambda: teardown_editor(editor))
    logger.debug("Running automated test: {}".format(editor_script))
    if editor_script != "":
        editor.args.extend(
            [
                "--skipWelcomeScreenDialog",
                "--autotest_mode",
                "--runpython",
                test_case,
                "--runpythonargs",
            ]
        )
    editor.args.extend([" ".join(cfg_args)])
    with editor.start():
        editorlog_file = os.path.join(editor.workspace.paths.project_log(), log_file_name)
        # Log monitor requires the file to exist.
        logger.debug("Waiting until log file <{}> exists...".format(editorlog_file))
        waiter.wait_for(
            lambda: os.path.exists(editorlog_file),
            timeout=60,
            exc=("Log file '{}' was never created by another process.".format(editorlog_file)),
            interval=1,
        )
        logger.debug("Done! log file <{}> exists.".format(editorlog_file))
        log_monitor = ly_test_tools.log.log_monitor.LogMonitor(launcher=editor, log_file_path=editorlog_file)
        log_monitor.monitor_log_for_lines(
            expected_lines=expected_lines,
            unexpected_lines=unexpected_lines,
            halt_on_unexpected=halt_on_unexpected,
            timeout=timeout,
        )


def launch_and_validate_results_launcher(
    launcher,
    level,
    remote_console_instance,
    expected_lines,
    unexpected_lines=[],
    halt_on_unexpected=False,
    port_listener_timeout=120,
    log_monitor_timeout=60,
    remote_console_port=4600,
):
    """
    Runs the launcher with the specified level, and monitors Game.log for expected lines.
    :param launcher: Configured launcher object to run test against.
    :param level: The level to load in the launcher.
    :param remote_console_instance: Configured Remote Console object.
    :param expected_lines: Expected lines to search log for.
    :param unexpected_lines: Unexpected lines to search log for. Defaults to none.
    :param halt_on_unexpected: Halts test if unexpected lines are found. Defaults to False.
    :param port_listener_timeout: Timeout for verifying successful connection to Remote Console.
    :param log_monitor_timeout: Timeout for monitoring for lines in Game.log
    :param remote_console_port: The port used to communicate with the Remote Console.
    """

    with launcher.start():
        gamelog_file = os.path.join(launcher.workspace.paths.project_log(), "Game.log")

        # Ensure Remote Console can be reached
        waiter.wait_for(
            lambda: check_for_listening_port(remote_console_port),
            port_listener_timeout,
            exc=AssertionError("Port {} not listening.".format(remote_console_port)),
        )
        remote_console_instance.start(timeout=30)

        # Load the specified level in the launcher
        send_command_and_expect_response(remote_console_instance, f"map {level}", "LEVEL_LOAD_COMPLETE", timeout=30)

        # Log monitor requires the file to exist
        logger.debug("Waiting until log file <{}> exists...".format(gamelog_file))
        waiter.wait_for(
            lambda: os.path.exists(gamelog_file),
            timeout=60,
            exc=("Log file '{}' was never created by another process.".format(gamelog_file)),
            interval=1,
        )
        logger.debug("Done! log file <{}> exists.".format(gamelog_file))
        log_monitor = ly_test_tools.log.log_monitor.LogMonitor(launcher=launcher, log_file_path=gamelog_file)
        # Workaround fix: Wait for log file to be opened before checking for expected lines. This is done in
        # monitor_log_for_lines as well, but has a low timeout with no way to currently override
        logger.debug("Waiting for log file '{}' to be opened by another process.".format(gamelog_file))
        # Check for expected/unexpected lines
        log_monitor.monitor_log_for_lines(
            expected_lines=expected_lines,
            unexpected_lines=unexpected_lines,
            halt_on_unexpected=halt_on_unexpected,
            timeout=log_monitor_timeout,
        )
