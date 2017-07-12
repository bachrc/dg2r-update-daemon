import io

import shutil
import traceback
import zipfile

import msgpack
from pathlib import Path
from update_daemon import crypto


class UpdateObject:
    def __init__(self, zip, signature, startup, destination_folder, autostart_file):
        self.autostart_file = autostart_file
        self.destination_folder = destination_folder
        self.startup = startup
        self.zip = zip
        self.signature = signature

    @staticmethod
    def load(file_path):
        file = Path(file_path)
        if not file.is_file():
            raise Exception("The path doesn't leads to a file.")
        try:
            data = msgpack.unpack(file.open('rb'))
            return UpdateObject(**data)
        except:
            traceback.print_exc()
            raise Exception("The file can't be read.")

    def unzip_folder(self):
        if crypto.is_file_verified(self.zip, self.signature):
            # We delete the folder recursively, and then recreate it
            dest = Path(self.destination_folder)
            shutil.rmtree(str(dest))
            dest.mkdir(parents=True, exist_ok=True)

            zip = zipfile.ZipFile(io.BytesIO(self.zip), "rb", zipfile.ZIP_DEFLATED)
            zip.extractall(path=dest)

            zip.close()
