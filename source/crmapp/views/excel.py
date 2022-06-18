import datetime
import xlwt
from django.http import HttpResponse
from crmapp.models import ManagerReport, Order, CashManager


def export_manager_report_to_excel(request):
    manager_report = ManagerReport.objects.order_by('created_at')

    rows = []
    for item in manager_report:
        rows.append((item.order_id, item.cleaner, item.salary, item.fine, item.fine_description, item.bonus,
                     item.bonus_description, item.comment, item.created_at.date(), item.get_salary()))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
                                          str(datetime.datetime.now()) + '.xls'
    webhook = xlwt.Workbook(encoding='utf-8')
    web_sheet = webhook.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['№ заказа', 'Клинер', 'Зарплата', 'Штраф', 'Описание', 'Бонус', 'Описание',
                   'Комментарий', 'Дата', 'Итого']

    for col_num in range(len(columns)):
        web_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            web_sheet.write(row_num, col_num, str(row[col_num]), font_style)
    webhook.save(response)

    return response


def export_expense_excel(request):
    orders = Order.objects.order_by('work_start').exclude(is_deleted=True).exclude(
        status='new')
    rows = []
    for order in orders:
        rows.append((order.pk, order.address, order.get_status_display(), order.work_end, order.get_total(),
                                 order.get_all_staff_expenses(), order.get_foreman_expenses(),
                                 order.get_income_outcome()))

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment; filename=Expences" + \
                                      str(datetime.datetime.now()) + ".xls"

    webhook = xlwt.Workbook(encoding="utf-8")
    web_sheet = webhook.add_sheet("Expences")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ["№ Заказа", "Адрес", "Статус", "Дата", "Сумма заказа", "Расходы на клинеров", "Прочие расходы", "Итого"]

    for col_num in range(len(columns)):
        web_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            web_sheet.write(row_num, col_num, str(row[col_num]), font_style)
    webhook.save(response)

    return response


def export_cash_manager_excel(request):
    cash_manager = CashManager.objects.filter(is_nullify=True)
    rows = []
    for cash in cash_manager:
        rows.append((f"{cash.staff.first_name} {cash.staff.last_name}", cash.date, cash.order.pk, cash.order.get_total()))
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment; filename=ManagerCash" + \
                                      str(datetime.datetime.now()) + ".xls"

    webhook = xlwt.Workbook(encoding="utf-8")
    web_sheet = webhook.add_sheet("Expences")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ["Менеджер", "Дата", "Заказ №", "Сумма"]

    for col_num in range(len(columns)):
        web_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            web_sheet.write(row_num, col_num, str(row[col_num]), font_style)
    webhook.save(response)

    return response

