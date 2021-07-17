import emoji

waiting_VIN_or_autonumber = """
Введите VIN или гос.номер автомобиля, чтобы получить отчёт автоэксперта о проверке автомобиля:
"""

report_does_not_exist = """
По данному VIN (гос. номеру) пока нет отчёта автоэксперта.

Заказать выездную проверку автомобиля автоэкспертом в любом регионе России: +7 (926) 266-42-22». 
"""

# user_report = 'Отчёт: {name}VIN автомобиля: {VIN}\nДата добавления отчёта: {create_date}\nРейтинг автоэксперта: {rating}\nЦена: {price}'


user_report = '''\
Отчёт: {name}

VIN автомобиля: {VIN}
Гос.номер автомобиля: {auto_number}
Дата добавления отчёта: {create_date}
Рейтинг автоэксперта: {rating}

Цена: {price} руб
'''

user_report_for_admin = '''
Отчёт: {name}

VIN автомобиля: {VIN}
Гос.номер автомобиля: {auto_number}
Дата добавления отчёта: {create_date}
Рейтинг автоэксперта: {rating}

Ф.И.О: {FIO}
Номер телефона: {phone}

Цена: {price} руб
'''

expert_my_report = """
Отчёт: {name}
Дата добавления отчёта: {create_date}
Кол-во покупок: {buy_count}
"""

expert_my_account = """
Ваш уникальный id: {id}
Ваш баланс: {balance} руб
Ваш рейтинг: {rating}
Кол-во отчётов: {reports_count}
Кол-во покупок: {buy_count}
"""

expert_not_reports = 'У вас нет отчётов❗️'


# Текста для добавления отчёта
# --------------------------------------------------------
waiting_VIN = """
Шаг 1 из 10

Введите VIN автомобиля:
"""
waiting_auto_number = """
Шаг 2 из 10

Введите гос.номер автомобиля:
"""
waiting_VIN_photo = """
Шаг 3 из 10

Загрузите фотографию VIN на кузове автомобиля
"""
waiting_odometer_data = """
Шаг 4 из 10

Введите пробег на приборной панели:
"""
waiting_vehicle_condition = """
Шаг 5 из 10

Загрузите фотографию разворота автомобиля с отметками об окрасах, ремонтах, замене деталей.

Либо опишите эти данные текстом.

Либо вы можете загрузить одно голосовое сообщение. 
"""
waiting_defects_photo = """
Шаг 6 из 10

Загрузите фотографии дефектов кузова, салона, техники. До 20 файлов.

После завершения нажмите кнопку 'Продолжить' 👇
"""

defects_photos_all = 'Добавлено 20 из 20 файлов!'

waiting_computer_diagnostics = """
Шаг 7 из 10

Загрузите отчёт о компьютерной диагностике в формате PDF, TXT или фото. До 3 файлов.

После завершения нажмите кнопку 'Продолжить' 👇
"""

computer_diagnostics_all = 'Добавлено 3 из 3 файлов!'

waiting_checking_databases = """
Шаг 8 из 10

Загрузите отчёт о проверке по базам данных в формате PDF или фото. До 4 файлов.

После завершения нажмите кнопку 'Продолжить' 👇
"""

checking_databases_all = 'Добавлено 4 из 4 файлов!'

waiting_defects_description = """
Шаг 9 из 10

Опишите текстом кратко выявленные проблемы, состояние автомобиля. До 4000 символов
"""
waiting_voice = """
Шаг 10 из 10

Запишите голосовое сообщение о состоянии автомобиля в целом и что не указали.
"""
# waiting

invalid_VIN_format = 'Неверный формат VIN❗️'
invalid_auto_number_format = 'Неверный формат гос.номера❗️'
invalid_photo = """
Неверное расширение файла❗️

Вы можете загружать только фото!
"""
invalid_odometer_data = """
Неверно введён пробег❗️

Используйте только цифры!
"""
invalid_diagnostic_document_extension = """
Неверное расширение файла❗️

Вы можете загружать только .pdf, .txt, фото
"""
invalid_voice_extension = 'Вы можете использовать только голосовые сообщения❗️'
# invalid_price = 'Вы ввели неверную цену! Используйте только цифры!'

zip_auto_data_text = """
VIN автомобиля: {VIN}
Гос. номер автомобиля: {auto_number}
Пробег автомобиля: {odometer_data}

Состояние автомобиля: {description}
"""

zip_auto_data_with_vehicle_condition_text = """
VIN автомобиля: {VIN}
Гос. номер автомобиля: {auto_number}
Пробег автомобиля: {odometer_data}

Состояние кузова автомобиля: {vehicle_condition}

Состояние автомобиля: {description}
"""

waiting_create_report = 'Формирую отчёт...'
report_created = 'Отчёт успешно добавлен!'

only_one_file = 'Вы можете отправить только 1 файл❗️ Повторите попытку.'
only_three_file = 'Вы можете отправить только 3 файла❗️'
only_four_file = 'Вы можете отправить только 4 файла❗️'
only_one_voice = 'Вы можете отправить только одно голосовое сообщение! Я загрузил первое.'

files_not_add = 'Вы не загрузили ни одного файла❗️'

defects_photos_not_voice = """
Нельзя загрузить голосовое сообщение❗️

Вы можете загружать только фото!
"""
defects_photos_not_text = """
Нельзя загрузить текстовое сообщение❗️

Вы можете загружать только фото!
"""

computer_diagnostics_not_voice = """
Нельзя загрузить голосовое сообщение❗️

Вы можете загружать только .pdf, .txt и фото!
"""
computer_diagnostics_not_text = """
Нельзя загрузить текстовое сообщение❗️

Вы можете загружать только .pdf, .txt и фото!
"""

checking_databases_not_voice = """
Нельзя загрузить голосовое сообщение❗️

Вы можете загружать только .pdf и фото!
"""
checking_databases_not_text = """
Нельзя загрузить текстовое сообщение❗️

Вы можете загружать только .pdf и фото!
"""

admin_panel = 'Панель Администратора 👇'

# find_expert_tg_id = 'Введите уникальный идентификатор эксперта, "telegram id", "telegram username" или номер телефона:'

find_expert_tg_id = '''
Введите:

- уникальный идентификатор эксперта
- telegram id
- telegram username
- номер телефона
- Название его отчёта
'''

find_expert_does_not_exist = 'Автоэксперт не найден❗️'
admin_in_expert_menu = """
Уникальный id: {id}
ФИО: {FIO}
Номер телефона: {phone}
Баланс: {balance} руб
Рейтинг: {rating}
Кол-во отчётов: {reports_count}
Кол-во покупок: {buy_count}
"""
admin_in_expert_menu_with_username = """
Уникальный id: {id}
ФИО: {FIO}
Telegram username: @{tg_username}
Номер телефона: {phone}
Баланс: {balance} руб
Рейтинг: {rating}
Кол-во отчётов: {reports_count}
Кол-во покупок: {buy_count}
"""
admin_in_expert_menu_expert_not_reports = 'У автоэксперта нет отчётов ❗️'

add_expert_waiting_forward = 'Перешлите сообщение от будущего автоэксперта'
add_expert_success = 'Автоэксперт успешно создан!'
add_expert_exist = 'Данный автоэксперт уже существует❗️ Повторите попытку.'

only_text_msg = 'Вы можете отправить только текстовое сообщение❗️'
only_int_msg = 'Вы можете использовать только цифры❗️'
only_photo_msg = 'Вы можете загружать только фото❗️'

change_commission_amount = """
💲 ИЗМЕНЕНИЕ КОММИССИИ 💲

Текущая коммиссия: {now_commission} руб.

Введите новую сумму комиссии:
"""
change_report_price = """
💲 ИЗМЕНЕНИЕ СТОИМОСТИ ОТЧЁТА 💲

Текущая стоимость: {price} руб.

Введите новую стоимость:
"""
change_commission_only_int_msg = 'Вы можете вводить только целые числа❗️'
change_commission_successful = 'Комиссия | Стоимость успешно изменена!'

delete_report_waiting_name = 'Введите название отчёта:'
delete_report_does_not_exist = 'Отчёт с таким названием не найден❗️'
delete_report_confirm = """
Отчёт: {name}
Дата добавления отчёта: {create_date}
Кол-во покупок: {buy_count}

Вы действительно хотите удалить отчёт? 👇 
"""
delete_report_success = 'Отчёт успешно удалён!'

admin_in_expert_menu_not_revenues = 'У эксперта нет доходов❗️'
admin_in_expert_menu_not_expenses = 'У эксперта нет расходов❗️'
admin_in_expert_menu_not_withdrawals = 'Эксперт еще не выводил средства❗️'

not_admin = 'Вы не являетесь администратором❗️'

expert_estimation_or_complaint = 'Оцените насколько отчёт автоэксперта был полон и полезен 👇'
expert_estimation_success = 'Спасибо за оценку!'

expert_complaint = 'Введите текст жалобы:'
expert_complaint_admin = """
😡 ЖАЛОБА НА ЭКСПЕРТА 😡

Текст жалобы: {complaint_text}

Отчёт: {report_name}
Клиент: {client_data}
Эксперт: {expert_data}

Скачать отчёт 👇
"""

expert_complaint_client_not_tg_username = """
У вас нет уникального "telegram username" ❗️

Отправьте свой номер телефона, чтобы администратор смог с вами связаться 👇
"""
expert_complaint_success_send = 'Жалоба успешно отправлена!'

add_expert_phone = "Введите его номер телефона, чтобы вы смогли с ним связаться:"
invalid_phone = 'Неверный формат номера телефона❗️'

withdrawal_amount = 'Введите сумму вывода, минимум 1000 рублей:'
withdrawal_too_expert_balance = 'Сумма вывода превышает баланс❗️'
admin_expert_withdrawal_request = """
💶 ВЫПЛАТА ЭКСПЕРТУ 💶

Уникальный идентификатор: {id}
Баланс: {balance}
Рейтинг: {rating}
Кол-во отчётов: {reports_count}
Кол-во покупок: {buy_count}

Сумма выплаты: {request_amount}
Ф.И.О: {FIO}
Связаться с экспертом: {expert_data}
"""
admin_expert_withdrawal_finish_new_balance = """
💶 ВЫПЛАТА ЭКСПЕРТУ 💶

Уникальный идентификатор: {id}
Баланс: {balance}
Рейтинг: {rating}
Кол-во отчётов: {reports_count}
Кол-во покупок: {buy_count}

Сумма выплаты: {request_amount}
Ф.И.О: {FIO}
Связаться с экспертом: {expert_data}

Введите новый баланс эксперта:
"""
admin_expert_withdrawal_finish_auto_new_balance_success = 'Выплата успешно завершена!'
expert_withdrawal_send_admin = 'Заявка отправлена администратору!'
admin_expert_withdrawal_cancel = 'Выплата успешно отменена!'

expert_blocked = 'Эксперт заблокирован❗️'
expert_unblocked = 'Эксперт разблокирован❗️'

too_file_size = 'Вы можете загружать файлы до 10 МБ❗️'

add_expert_success_with_username = """
Уникальный id: {id}
Telegram id: {tg_id}
ФИО: {FIO}
Telegram username: {tg_username}
Номер телефона: {phone}
"""
add_expert_success_with_phone = """
Уникальный id: {id}
Telegram id: {tg_id}
ФИО: {FIO}
Номер телефона: {phone}
"""
add_expert_FIO = 'Введите имя фамилию эксперта:'

your_account_is_blocked = 'Ваш аккаунт заблокирован❗️'

user_agreement = '''
Совершая платёж, вы принимаете условия пользовательского соглашения.

Свзяь с администратором: support@zanos.ru
'''
# --------------------------------------------------------


MESSAGES = {
    'user_agreement': user_agreement,

    'waiting_VIN_or_autonumber': waiting_VIN_or_autonumber,
    'report_does_not_exist': report_does_not_exist,
    'user_report': user_report,
    'user_report_for_admin': user_report_for_admin,
    'expert_my_report': expert_my_report,
    'expert_my_account': expert_my_account,

    'waiting_VIN': waiting_VIN,
    'waiting_auto_number': waiting_auto_number,
    'waiting_VIN_photo': waiting_VIN_photo,
    'waiting_odometer_data': waiting_odometer_data,
    'waiting_vehicle_condition': waiting_vehicle_condition,
    'waiting_defects_photo': waiting_defects_photo,
    'waiting_computer_diagnostics': waiting_computer_diagnostics,
    'waiting_checking_databases': waiting_checking_databases,
    'waiting_defects_description': waiting_defects_description,
    'waiting_voice': waiting_voice,

    'defects_photos_all': defects_photos_all,
    'computer_diagnostics_all': computer_diagnostics_all,
    'checking_databases_all': checking_databases_all,

    'invalid_VIN_format': invalid_VIN_format,
    'invalid_auto_number_format': invalid_auto_number_format,
    'invalid_photo': invalid_photo,
    'invalid_odometer_data': invalid_odometer_data,
    'invalid_diagnostic_document_extension': invalid_diagnostic_document_extension,
    'invalid_voice_extension': invalid_voice_extension,

    'zip_auto_data_text': zip_auto_data_text,
    'zip_auto_data_with_vehicle_condition_text': zip_auto_data_with_vehicle_condition_text,

    'waiting_create_report': waiting_create_report,
    'report_created': report_created,

    'only_one_file': only_one_file,
    'only_three_file': only_three_file,
    'only_four_file': only_four_file,
    'only_one_voice': only_one_voice,
    'only_photo_msg': only_photo_msg,

    'files_not_add': files_not_add,
    'expert_not_reports': expert_not_reports,
    'defects_photos_not_voice': defects_photos_not_voice,
    'defects_photos_not_text': defects_photos_not_text,

    'computer_diagnostics_not_voice': computer_diagnostics_not_voice,
    'computer_diagnostics_not_text': computer_diagnostics_not_text,

    'checking_databases_not_voice': checking_databases_not_voice,
    'checking_databases_not_text': checking_databases_not_text,

    'admin_panel': admin_panel,

    'find_expert_tg_id': find_expert_tg_id,
    'find_expert_does_not_exist': find_expert_does_not_exist,
    'admin_in_expert_menu': admin_in_expert_menu,
    'admin_in_expert_menu_expert_not_reports': admin_in_expert_menu_expert_not_reports,

    'add_expert_waiting_forward': add_expert_waiting_forward,
    'add_expert_exist': add_expert_exist,
    'add_expert_success': add_expert_success,
    'add_expert_FIO': add_expert_FIO,

    'only_text_msg': only_text_msg,
    'only_int_msg': only_int_msg,

    'not_admin': not_admin,

    'change_commission_amount': change_commission_amount,
    'change_report_price': change_report_price,
    'change_commission_successful': change_commission_successful,

    'delete_report_waiting_name': delete_report_waiting_name,
    'delete_report_does_not_exist': delete_report_does_not_exist,
    'delete_report_confirm': delete_report_confirm,
    'delete_report_success': delete_report_success,

    'admin_in_expert_menu_not_revenues': admin_in_expert_menu_not_revenues,
    'admin_in_expert_menu_not_expenses': admin_in_expert_menu_not_expenses,
    'admin_in_expert_menu_not_withdrawals': admin_in_expert_menu_not_withdrawals,

    'expert_estimation_or_complaint': expert_estimation_or_complaint,
    'expert_estimation_success': expert_estimation_success,
    'expert_complaint': expert_complaint,
    'expert_complaint_admin': expert_complaint_admin,
    'expert_complaint_client_not_tg_username': expert_complaint_client_not_tg_username,
    'expert_complaint_success_send': expert_complaint_success_send,

    'add_expert_phone': add_expert_phone,
    'invalid_phone': invalid_phone,

    'withdrawal_amount': withdrawal_amount,
    'withdrawal_too_expert_balance': withdrawal_too_expert_balance,
    'admin_expert_withdrawal_request': admin_expert_withdrawal_request,
    'admin_expert_withdrawal_finish_new_balance': admin_expert_withdrawal_finish_new_balance,
    'admin_expert_withdrawal_finish_auto_new_balance_success': admin_expert_withdrawal_finish_auto_new_balance_success,
    'expert_withdrawal_send_admin': expert_withdrawal_send_admin,
    'admin_expert_withdrawal_cancel': admin_expert_withdrawal_cancel,

    'expert_blocked': expert_blocked,
    'expert_unblocked': expert_unblocked,

    'too_file_size': too_file_size,

    'add_expert_success_with_username': add_expert_success_with_username,
    'add_expert_success_with_phone': add_expert_success_with_phone,

    'your_account_is_blocked': your_account_is_blocked,

    'admin_in_expert_menu_with_username': admin_in_expert_menu_with_username
}

KEYBOARD = {
    'buy_report': 'Купить отчёт за {price} RUB   💵',
    'download_report': 'Скачать отчёт   📥',
    'find_report_expert_menu': {
        'add_report': 'Добавить запись   🖌',
        'my_account': 'Личный кабинет   👤'
    },
    'find_report_admin_menu': {
        'add_report': 'Добавить запись   🖌',
        'my_account': 'Личный кабинет   👤',
        'menu': 'Админка   💎'
    },
    'expert_my_account_menu': {
        'my_reports': 'Мои отчёты   📋',
        'withdrawal_money': 'Вывести   🏦'
    },
    'admin':
        {
            'main_menu': {
                'find_expert': 'Найти эксперта   🔎',
                'add_expert': 'Добавить эксперта   ✅',
                'delete_report': 'Удалить отчёт   ❌',
                'change_commission': 'Изменить комиссию | Стоимость   💲'
            },
            'in_expert_menu': {
                'expert_reports': 'Отчёты   📋',
                'revenues': 'Доходы   📈',
                'expenses': 'Расходы   📉',
                'withdrawals': 'Выводы средств   🏦',
                'block_unblock_expert': {
                    'block': 'Заблокировать эксперта   ⛔️',
                    'unblock': 'Разблокировать эксперта   ✅'
                }
            }
        },

    'confirm': {
        'true': 'Удалить   ✅',
        'false': 'Отмена   ❌'
    },

    'back': 'Назад   ↪️',
    'cancel': 'Отмена   ↪️',
    'main_menu': 'Главное меню   🏠',
    'download_success': 'Продолжить   📥',
    'next_step': 'Следующий шаг   ➡️',
    'expert_complaint': 'Жалоба   😡',
    'admin_expert_withdrawal_finish': 'Завершить выплату   ✅',
    'admin_expert_withdrawal_cancel': 'Отменить выплату   ❌',
    'admin_expert_withdrawal_finish_auto_new_balance': 'Сделать автоматически   🤖',
    'expert_buy_from_balance': 'Оплатить {price} руб. с баланса   🏦'
    # 'send_phone': 'Отправить номер   📱'
}