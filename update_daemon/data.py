import base64
import io

import shutil
import traceback
import zipfile

from pathlib import Path

import pickle

from update_daemon.crypto import crypto


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
            data = pickle.load(file.open('rb'))
            print(data)

            return UpdateObject(data['zip'], data['signature'], data['startup'],
                                data['destination_folder'], data['autostart_file'])
        except:
            traceback.print_exc()
            raise Exception("The file can't be read.")

    def unzip_folder(self):
        if crypto.is_file_verified(self.zip.getvalue(), self.signature):
            # We delete the folder recursively, and then recreate it
            dest = Path(self.destination_folder)
            if dest.exists():
                shutil.rmtree(self.destination_folder)
            dest.mkdir(parents=True, exist_ok=True)

            zip_file = zipfile.ZipFile(self.zip, "r", zipfile.ZIP_DEFLATED)
            zip_file.extractall(path=self.destination_folder)

            zip_file.close()
        else:
            raise Exception("Signature du fichier invalide.")
