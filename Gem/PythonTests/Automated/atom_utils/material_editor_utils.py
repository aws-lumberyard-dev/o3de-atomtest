"""
Copyright (c) Contributors to the Open 3D Engine Project

SPDX-License-Identifier: Apache-2.0 OR MIT

import azlmbr.materialeditor will fail with a ModuleNotFound error when using this script with Editor.exe
This is because azlmbr.materialeditor only binds to MaterialEditor.exe and not Editor.exe
You need to launch this script with MaterialEditor.exe in order for azlmbr.materialeditor to appear.
"""

import sys
import time
import azlmbr.atom
import azlmbr.materialeditor as materialeditor
import azlmbr.materialeditor.general as general
import azlmbr.bus as bus
import os


class MaterialEditorHelper:
    def __init__(self, log_prefix: str, args=None) -> None:
        self.log_prefix = log_prefix + ":  "
        self.args = {}
        if args:
            # Get the args from command-line args
            if len(sys.argv) == (len(args) + 1):
                for arg_index in range(len(args)):
                    self.args[args[arg_index]] = sys.argv[arg_index + 1]
            else:
                self.log(f"Expected command-line args:  {args}")
                self.log(f"Check that cfg_args were passed into the test class")

    def log(self, log_line: str) -> None:
        print(self.log_prefix + log_line)

    def run_test(self) -> None:
        self.log("run")

    # TODO: Any additional steps needed for MaterialEditor can be added as setup and teardown
    def setup(self):
        self.log("Test started")

    def teardown(self):
        self.log("Test finished")

    def run(self) -> None:
        self.setup()
        self.run_test()
        self.teardown()

    def is_close(self, actual, expected, buffer=sys.float_info.min):
        return abs(actual - expected) < buffer

    def wait_for_condition(self, function, timeout_in_seconds=1.0):
        # type: (function, float) -> bool
        """
        Function to run until it returns True or timeout is reached
        the function can have no parameters and
        waiting idle__wait_* is handled here not in the function

        :param function: a function that returns a boolean indicating a desired condition is achieved
        :param timeout_in_seconds: when reached, function execution is abandoned and False is returned
        """
        with Timeout(timeout_in_seconds) as t:
            while True:
                try:
                    general.idle_wait_frames(1)
                except Exception:
                    print("WARNING: Couldn't wait for frame")

                if t.timed_out:
                    return False

                ret = function()
                if not isinstance(ret, bool):
                    raise TypeError("return value for wait_for_condition function must be a bool")
                if ret:
                    return True


class Timeout:
    # type: (float) -> None
    """
    contextual timeout
    :param seconds: float seconds to allow before timed_out is True
    """

    def __init__(self, seconds):
        self.seconds = seconds

    def __enter__(self):
        self.die_after = time.time() + self.seconds
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def timed_out(self):
        return time.time() > self.die_after


def open_material(file_path):
    return materialeditor.MaterialDocumentSystemRequestBus(bus.Broadcast, "OpenDocument", file_path)


def is_open(document_id):
    return materialeditor.MaterialDocumentRequestBus(bus.Event, "IsOpen", document_id)


def save_document(document_id):
    return materialeditor.MaterialDocumentSystemRequestBus(bus.Broadcast, "SaveDocument", document_id)


def save_document_as_copy(document_id, target_path):
    return materialeditor.MaterialDocumentSystemRequestBus(
        bus.Broadcast, "SaveDocumentAsCopy", document_id, target_path
    )


def save_document_as_child(document_id, target_path):
    return materialeditor.MaterialDocumentSystemRequestBus(
        bus.Broadcast, "SaveDocumentAsChild", document_id, target_path
    )


def save_all():
    return materialeditor.MaterialDocumentSystemRequestBus(bus.Broadcast, "SaveAllDocuments")


def close_document(document_id):
    return materialeditor.MaterialDocumentSystemRequestBus(bus.Broadcast, "CloseDocument", document_id)


def close_all_documents():
    return materialeditor.MaterialDocumentSystemRequestBus(bus.Broadcast, "CloseAllDocuments")


def close_all_except_selected(document_id):
    return materialeditor.MaterialDocumentSystemRequestBus(bus.Broadcast, "CloseAllDocumentsExcept", document_id)


def get_property(document_id, property_name):
    return materialeditor.MaterialDocumentRequestBus(bus.Event, "GetPropertyValue", document_id, property_name)


def set_property(document_id, property_name, value):
    return materialeditor.MaterialDocumentRequestBus(bus.Event, "SetPropertyValue", document_id, property_name, value)


def is_pane_visible(pane_name):
    return materialeditor.MaterialEditorWindowRequestBus(bus.Broadcast, "IsDockWidgetVisible", pane_name)


def set_pane_visibility(pane_name, value):
    materialeditor.MaterialEditorWindowRequestBus(bus.Broadcast, "SetDockWidgetVisible", pane_name, value)


def select_lighting_config(config_name):
    azlmbr.materialeditor.MaterialViewportRequestBus(azlmbr.bus.Broadcast, "SelectLightingPresetByName", config_name)


def set_grid_enable_disable(value):
    azlmbr.materialeditor.MaterialViewportRequestBus(azlmbr.bus.Broadcast, "SetGridEnabled", value)


def get_grid_enable_disable():
    return azlmbr.materialeditor.MaterialViewportRequestBus(azlmbr.bus.Broadcast, "GetGridEnabled")


def set_shadowcatcher_enable_disable(value):
    azlmbr.materialeditor.MaterialViewportRequestBus(azlmbr.bus.Broadcast, "SetShadowCatcherEnabled", value)


def get_shadowcatcher_enable_disable():
    return azlmbr.materialeditor.MaterialViewportRequestBus(azlmbr.bus.Broadcast, "GetShadowCatcherEnabled")


def select_model_config(configname):
    azlmbr.materialeditor.MaterialViewportRequestBus(azlmbr.bus.Broadcast, "SelectModelPresetByName", configname)


screenshotsFolder = os.path.join(azlmbr.paths.devroot, "AtomTest", "Cache" "pc", "Screenshots")


class ScreenshotHelper:
    """
    A helper to capture screenshots and wait for them.
    """

    def __init__(self, idle_wait_frames_callback):
        super().__init__()
        self.done = False
        self.capturedScreenshot = False
        self.max_frames_to_wait = 60

        self.idle_wait_frames_callback = idle_wait_frames_callback

    def capture_screenshot_blocking(self, filename):
        """
        Capture a screenshot and block the execution until the screenshot has been written to the disk.
        """
        self.handler = azlmbr.atom.FrameCaptureNotificationBusHandler()
        self.handler.connect()
        self.handler.add_callback("OnCaptureFinished", self.on_screenshot_captured)

        self.done = False
        self.capturedScreenshot = False
        success = azlmbr.atom.FrameCaptureRequestBus(azlmbr.bus.Broadcast, "CaptureScreenshot", filename)
        if success:
            self.wait_until_screenshot()
            print("Screenshot taken.")
        else:
            print("screenshot failed")
        return self.capturedScreenshot

    def on_screenshot_captured(self, parameters):
        # the parameters come in as a tuple
        if parameters[0]:
            print("screenshot saved: {}".format(parameters[1]))
            self.capturedScreenshot = True
        else:
            print("screenshot failed: {}".format(parameters[1]))
        self.done = True
        self.handler.disconnect()

    def wait_until_screenshot(self):
        frames_waited = 0
        while self.done == False:
            self.idle_wait_frames_callback(1)
            if frames_waited > self.max_frames_to_wait:
                print("timeout while waiting for the screenshot to be written")
                self.handler.disconnect()
                break
            else:
                frames_waited = frames_waited + 1
        print("(waited {} frames)".format(frames_waited))


def capture_screenshot(file_path):
    return ScreenshotHelper(azlmbr.materialeditor.general.idle_wait_frames).capture_screenshot_blocking(
        os.path.join(file_path)
    )
