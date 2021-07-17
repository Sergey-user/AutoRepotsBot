import re

class InvalidVINFormat(Exception):
    pass

class InvalidAutoNumberFormat(Exception):
    pass

class InvalidPhotoExtension(Exception):
    pass

class InvalidDiagnosticDocumentExtension(Exception):
    pass

class InvalidCheckingDatabaseDocumentExtension(Exception):
    pass

class InvalidVoiceExtension(Exception):
    pass

class InvalidPriceFromat(Exception):
    pass


class AddReportFilter():
    @classmethod
    async def VIN_filter(cls, VIN):
        if re.match(
            r'[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F, G, H, J, K, L, M, N, P, R, S, T, U, V, W, X, Y, Z]{17}',
            VIN
        ) and len(VIN) == 17:
            return True
        else:
            raise InvalidVINFormat

    @classmethod
    async def auto_number_filter(cls, auto_number):
        match_pattern = r'[A, B, E, K, M, H, O, P, C, T, Y, X, А, В, Е, К, М, Н, О, Р, С, Т, У, Х]{1}' \
                        '\d{3}[A, B, E, K, M, H, O, P, C, T, Y, X, А, В, Е, К, М, Н, О, Р, С, Т, У, Х]{2}\d{2,3}'
        if re.match(match_pattern, auto_number):
            if len(auto_number) == 8 or len(auto_number) == 9:
                return True
            else:
                raise InvalidAutoNumberFormat
        else:
            raise InvalidAutoNumberFormat

    @classmethod
    async def is_photo_filter(cls, file_extension):
        available_file_extension = ['image/jpg', 'image/jpeg', 'image/png']
        if file_extension in available_file_extension:
            return True
        else:
            raise InvalidPhotoExtension

    @classmethod
    async def odometer_data_filter(cls, odometer_data):
        int(odometer_data)

    @classmethod
    async def computer_diagnostics_filter(cls, file_extension):
        available_file_extension = ['image/jpg', 'image/jpeg', 'image/png', 'text/plain', 'application/pdf']
        if file_extension in available_file_extension:
            return True
        else:
            raise InvalidDiagnosticDocumentExtension

    @classmethod
    async def checking_databases_filter(cls, file_extension):
        print(file_extension)

        available_file_extension = ['image/jpg', 'image/jpeg', 'image/png', 'application/pdf']
        if file_extension in available_file_extension:
            return True
        else:
            raise InvalidCheckingDatabaseDocumentExtension

    @classmethod
    async def only_voice_filter(cls, file_extension):
        if file_extension == 'audio/ogg':
            return True
        else:
            raise InvalidVoiceExtension

    async def price_filter(self, price):
        try:
            int(price)
        except:
            raise InvalidPriceFromat