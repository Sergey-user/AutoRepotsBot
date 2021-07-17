import os, shutil
from pydub import AudioSegment

from settings.bot_settings import PROJECT_PATH
from app.Expert.ExpertModels import AutoReportModel
from app.ZipManager import ZipManager


class ExpertAddReportUtil():
    zip: ZipManager
    proxy_path: str

    def __init__(self):
        self.zip = ZipManager()

    async def add_new_report(self, user_tg_id, archive_name_zip):
        await self.__create_state_folder(user_tg_id)
        return await self.zip.create_zip(archive_name_zip)

    async def add_VIN_photo_to_zip(self, bot, photo_data):
        extension = await self.__get_extension(photo_data['mime_type'])
        path = self.proxy_path + f"/VIN_photo.{extension}"
        await bot.download_file_by_id(photo_data['tg_id'], path)

        await self.zip.add_file(f"VIN_photo.{extension}", path)

    async def add_vehicle_condition_to_zip(self, bot, document_data):
        extension = await self.__get_extension(document_data['mime_type'])
        path = self.proxy_path + f"/vehicle_condition.{extension}"
        await bot.download_file_by_id(document_data['tg_id'], path)
        await self.zip.add_file(f"VIN_photo.{extension}", path)

    async def add_file_to_zip(self, bot, zip_file_name: str, file_data: dict):
        extension = await self.__get_extension(file_data['mime_type'])
        path = self.proxy_path + f"/{zip_file_name}.{extension}"
        await bot.download_file_by_id(file_data['tg_id'], path)
        await self.zip.add_file(f"{zip_file_name}.{extension}", path)

    async def add_conver_voice_file_to_zip(self, bot, file_tg_id, file_name, new_file_name):
        path_file_name = self.proxy_path + f"/{file_name}"
        await bot.download_file_by_id(file_tg_id, path_file_name)
        path_new_file_name = self.proxy_path + f"/{new_file_name}"
        audio = AudioSegment.from_ogg(path_file_name)
        audio.export(path_new_file_name, format="mp3")
        await self.zip.add_file(new_file_name, path_new_file_name)

    async def add_files_to_zip_folder(self, bot, folder_name, zip_file_name, files):
        folder_path = self.proxy_path + f"/{folder_name}"

        count = 1
        for file in files:
            file_extension = await self.__get_extension(file['mime_type'])
            file_path = folder_path + f"/{zip_file_name}_{count}.{file_extension}"
            try:
                await bot.download_file_by_id(file['tg_id'], file_path)
            except FileNotFoundError:
                await self.__proxy_create_folder(folder_name)
                await bot.download_file_by_id(file['tg_id'], file_path)

            await self.zip.add_file_to_folder(folder_name, f"/{zip_file_name}_{count}.{file_extension}", file_path)
            count += 1

    async def add_about_auto_txt(self, text):
        path = self.proxy_path + '/opisanie_auto.txt'
        with open(path, 'w', encoding='utf-8') as file:
            file.write(text)
        await self.zip.add_file('about_auto.txt', path)

    async def get_report_name(self, VIN):
        VIN_report_count = AutoReportModel.select().where(AutoReportModel.VIN==VIN).count()
        name = f"{VIN}_{str(VIN_report_count+1)}"
        return name

    async def get_archive_name(self, VIN):
        VIN_report_count = AutoReportModel.select().where(AutoReportModel.VIN==VIN).count()
        name = f"{VIN}_{str(VIN_report_count+1)}.zip"
        return name

    async def delete_proxy_folder(self):
        # print(self.proxy_path)
        # os.rmdir(self.proxy_path)
        shutil.rmtree(self.proxy_path, ignore_errors=True)

    async def __create_state_folder(self, user_tg_id):
        path = PROJECT_PATH + '/archives/proxy/' + str(user_tg_id)
        os.mkdir(path)
        self.proxy_path = path

    async def __get_extension(self, mime_type: str):
        # if mime_type == 'audio/ogg':
        #     return 'ogg'
        split = mime_type.split('/')
        return split[1]

    async def __proxy_create_folder(self, folder_name):
        path = self.proxy_path + f"/{folder_name}"
        os.mkdir(path)