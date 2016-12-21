# encoding=utf-8

import openpyxl
import logging


def main():
    wb = openpyxl.Workbook()

    sheet = wb.get_active_sheet()
    sheet.title = 'test'
    wb.create_sheet(index=0, title='first sheet')
    wb.remove_sheet(wb.get_sheet_by_name('test'))
    sheet = wb.get_sheet_by_name('first sheet')
    sheet['A1'] = 'hello excel'

    wb.save('test.xlsx')


if __name__ == '__main__':
    main()
