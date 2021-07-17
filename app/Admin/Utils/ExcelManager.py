import os
import xlsxwriter

from settings.bot_settings import PROJECT_PATH


class ExcelManager():
    xlsx_files_path: str

    def __init__(self):
        self.xlsx_files_path = PROJECT_PATH + '/app/Admin/xlsx_files'

    async def get_expert_reports_xlsx(self, expert_tg_id, expert_reports):
        xlsx_file_path = self.xlsx_files_path + f'/{expert_tg_id}_reports.xlsx'

        wb = xlsxwriter.Workbook(xlsx_file_path)
        ws = wb.add_worksheet()

        ws.set_column(0, 0, 33)
        ws.set_column(1, 1, 17)
        ws.set_column(2, 2, 14)

        ws.write('A1', 'Название')
        ws.write('B1', 'Дата добавления')
        ws.write('C1', 'Кол-во покупок')

        column_num = 2
        for report in expert_reports:
            ws.write(f"A{column_num}", report.name)
            ws.write(f"B{column_num}", report.create_date.strftime('%d.%m.%Y'))
            ws.write(f"C{column_num}", await report.get_buy_count())
            column_num += 1

        wb.close()

        return xlsx_file_path

    async def get_expert_revenues_xlsx(self, expert_tg_id, revenues):
        xlsx_file_path = self.xlsx_files_path + f'/{expert_tg_id}_revenues.xlsx'

        wb = xlsxwriter.Workbook(xlsx_file_path)
        ws = wb.add_worksheet()

        ws.set_column(0, 0, 15)
        ws.set_column(1, 1, 15)
        ws.set_column(2, 2, 15)
        ws.set_column(3, 3, 15)
        ws.set_column(4, 4, 15)


        ws.write('A1', 'Тип дохода')
        ws.write('B1', 'Клиент')
        ws.write('C1', 'Эксперт')
        ws.write('D1', 'Дата')
        ws.write('E1', 'Сумма')

        column_num = 2
        for revenue in revenues:
            ws.write(f"A{column_num}", 'Продажа отчёта')
            ws.write(f"B{column_num}", revenue.client)
            ws.write(f"C{column_num}", revenue.expert.tg_id)
            ws.write(f"D{column_num}", revenue.date.strftime('%d.%m.%Y'))
            ws.write(f"E{column_num}", revenue.amount)
            column_num += 1

        wb.close()

        return xlsx_file_path

    async def get_expert_expenses_xlsx(self, expert_tg_id, expenses):
        xlsx_file_path = self.xlsx_files_path + f'/{expert_tg_id}_expenses.xlsx'

        wb = xlsxwriter.Workbook(xlsx_file_path)
        ws = wb.add_worksheet()

        ws.set_column(0, 0, 15)
        ws.set_column(1, 1, 15)
        ws.set_column(2, 2, 15)
        ws.set_column(3, 3, 15)
        ws.set_column(4, 4, 15)

        ws.write('A1', 'Тип расхода')
        ws.write('B1', 'Клиент')
        ws.write('C1', 'Эксперт')
        ws.write('D1', 'Дата')
        ws.write('E1', 'Сумма')

        column_num = 2
        for expense in expenses:
            ws.write(f"A{column_num}", 'Покупка отчёта')
            ws.write(f"B{column_num}", expense.client)
            ws.write(f"C{column_num}", expense.expert.tg_id)
            ws.write(f"D{column_num}", expense.date.strftime('%d.%m.%Y'))
            ws.write(f"E{column_num}", expense.amount)
            column_num += 1

        wb.close()

        return xlsx_file_path

    async def get_expert_withdrawals_xlsx(self, expert_tg_id, withdrawals):
        xlsx_file_path = self.xlsx_files_path + f'/{expert_tg_id}_withdrawals.xlsx'

        wb = xlsxwriter.Workbook(xlsx_file_path)
        ws = wb.add_worksheet()

        ws.set_column(0, 0, 15)
        ws.set_column(1, 1, 15)
        ws.set_column(2, 2, 15)
        ws.set_column(3, 3, 25)

        ws.write('A1', 'Эксперт')
        ws.write('B1', 'Дата')
        ws.write('C1', 'Сумма')
        ws.write('D1', 'Баланс на момент вывода')

        column_num = 2
        for withdrawal in withdrawals:
            ws.write(f"A{column_num}", withdrawal.expert.tg_id)
            ws.write(f"B{column_num}", withdrawal.date.strftime('%d.%m.%Y'))
            ws.write(f"C{column_num}", withdrawal.amount)
            ws.write(f"D{column_num}", withdrawal.balance_before_withdrawal)
            column_num += 1

        wb.close()

        return xlsx_file_path

    async def delete_xlsx(self, path):
        os.remove(path)