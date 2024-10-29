import time
import subprocess
import logging
from PIL import Image
from io import BytesIO

logger = logging.getLogger('libadb')

class adb(object):

    device_id = '127.0.0.1:16384'

    def __adb(self, args):
        start = time.time()
        p = subprocess.Popen([str(arg)
                              for arg in args], stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        logger.debug("Run (%d - %fs): %s", p.returncode,
                     time.time() - start, args)
        return (p.returncode, stdout, stderr)
    
    def tap(self, x, y):
        _, stdout, _ = self.__adb(
            ["adb", "-s", self.device_id, "shell", "input", "tap", x, y])
    
    def screencap(self):
        _, stdout, _ = self.__adb(
            ["adb", "-s", self.device_id, "exec-out", "screencap", "-p"])
        try:
            image = Image.open(BytesIO(stdout))
            return image
        except OSError as err:
            logger.debug(
                "Screenshot failed, using fallback method: %s", err)