from zipfile import ZipFile
import os

from settings.bot_settings import PROJECT_PATH

class ZipManager():
    path: str
    name: str

    async def create_zip(self, report_name_zip):
        self.name = report_name_zip
        self.path = PROJECT_PATH + '/archives/' + report_name_zip
        with ZipFile(self.path, 'w') as zip:
            pass
        return self.path

    async def add_file(self, name, path):
        with ZipFile(self.path, 'a') as zip:
            zip.write(path, arcname=name)

    async def add_file_to_folder(self, folder_name, file_name, file_path):
        with ZipFile(self.path, 'a') as zip:
            zip.write(file_path, arcname=f"{folder_name}/{file_name}")


    @classmethod
    async def delete_report_zip(cls, name):
        path = PROJECT_PATH + f"/archives/{name}.zip"
        os.remove(path)

    # async def new_folder_download_files(self, folder_name, files):
    #     with ZipFile(self.path, 'a') as zip:
    #         for file in files:
    #             zip.write(file, arcname=f"{folder_name}/{}")