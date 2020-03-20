# -*- encoding: utf-8 -*-
import logging
import threading
import pythoncom
import win32process
import win32event
import time


class Services_Runner(threading.Thread):
    def __init__(self, work_dir, process_name, args=None):
        threading.Thread.__init__(self)
        self._handlers = []
        self._thread_stop = False
        self._work_dir = work_dir
        self._process_name = process_name
        self._process_args = args

    def stop(self):
        self._thread_stop = True
        self.join()

    def CreateProcess(self):
        try:
            info = win32process.CreateProcess(self._process_name, self._process_args, None, None, 0,
                                              win32process.CREATE_NO_WINDOW, None,
                                              self._work_dir,
                                              win32process.STARTUPINFO())
            return info[0]
        except Exception as ex:
            logging.exception(ex)
            return None

    def run(self):
        pythoncom.CoInitialize()
        subprocess = self.CreateProcess()
        while not self._thread_stop and subprocess:
            try:
                rc = win32event.WaitForSingleObject(subprocess, 1000)
                logging.debug("{0} WaitForSingleObject: {1}".format(self._process_name, rc))

                if rc == win32event.WAIT_FAILED:
                    logging.warning("{0} wait failed".format(self._process_name))
                    continue

                if rc == win32event.WAIT_TIMEOUT:
                    continue

                if rc == win32event.WAIT_OBJECT_0:
                    exit_code = win32process.GetExitCodeProcess(subprocess)
                    logging.warning("{0} exited with code {1}".format(self._process_name, exit_code))
                    if not self._thread_stop:
                        time.sleep(3)
                        subprocess = self.CreateProcess()
            except Exception as ex:
                logging.exception(ex)
                break

        if subprocess:
            logging.info("TerminateProcess {0}".format(self._process_name))
            win32process.TerminateProcess(subprocess)
