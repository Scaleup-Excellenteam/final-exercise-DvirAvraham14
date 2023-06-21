import os
import subprocess
import sys
import time
from unittest import TestCase
from userScript import send_request_with_file, get_status_request

main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SERVER = os.path.join(main_dir, "API", "app.py")
FILE_MONITOR = os.path.join(main_dir, "API", "fileMonitoring.py")
TEST_FILE_PATH = os.path.join(main_dir, "pres.pptx")
SLEEP_TIME = 5

class Test(TestCase):
    def setUp(self) -> None:
        self.server = subprocess.Popen([sys.executable, SERVER])
        self.file_monitor = subprocess.Popen(["python3", FILE_MONITOR])
        print("Waiting for server and file monitor to start...")
        time.sleep(SLEEP_TIME)

    def tearDown(self) -> None:
        print("Killing server and file monitor...")
        self.server.kill()
        self.file_monitor.kill()

    def test_system(self):
        response = send_request_with_file(TEST_FILE_PATH)
        self.assertIsNotNone(response["uuid"], "UUID is None - upload failed")
        time.sleep(SLEEP_TIME*4)
        uuid = response["uuid"]
        response = get_status_request(f"status {uuid}")
        self.assertEqual(response["status"], "done", "Status is not done - processing failed")
