import datetime

from telegram import Update
from telegram.ext import CallbackContext
from crmapp.models import Order, ManagerReport, ServiceOrder
from tgbot.handlers.utils import is_staff_in_order
from tgbot.handlers.keyboard import get_refuses_keyboard, get_staff_order_keyboard, get_in_place_keyboard, \
    get_order_information_keyboard, get_brigadier_start_keyboard, get_brigadier_end_keyboard


@is_staff_in_order
def order_staff_accept_callback(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    if call == "accept":
        order = Order.objects.get(pk=order_id)
        staff = order.order_cleaners.get(staff=staff_id)
        if staff.is_accept == False and staff.is_refuse == False:
            staff.is_accept = True
            staff.save()
            text = f'''
Информация о заказе
 ◉ Дата: {order.work_start.date()}
 ◉ Время: {order.work_start.time()}
 ◉ Адрес: {order.address}
 ◉ Время проведения работ: {order.work_end.time()}
 ◉ Вид оплаты: {order.payment_type}
Информация о клиенте
 ◉ Имя: {order.client_info.full_name}
 ◉ Телефон: {order.client_info.phone}\n'''
            keyboard = get_in_place_keyboard(order_id, staff_id)
            context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)


@is_staff_in_order
def order_staff_refuse_callback(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    if call == "refuse":
        text = "Вы уверены что хотите отказаться от заказа?\nВ случае отказа вы получите штраф n сом"
        keyboard = get_refuses_keyboard(order_id, staff_id)
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)


@is_staff_in_order
def refuse_true_callback(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    staff = order.order_cleaners.get(staff=staff_id)
    if call == "retrue":
        if staff.is_accept == False and staff.is_refuse == False:
            staff.is_refuse = True
            staff.save()
            text = f"Вы больше не участвуете в данном заказе №{order_id}"
            context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)

        else:
            text = "Даный запрос не может быть выолнен"
            context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)


@is_staff_in_order
def refuse_false_callback(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    if call == "refalse":
        text = f'''
Информация о заказе
 ◉ Дата: {order.work_start.date()}
 ◉ Время: {order.work_start.time()}
 ◉ Адрес: {order.address}
    '''
        keyboard = get_staff_order_keyboard(order_id, staff_id)
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)


@is_staff_in_order
def order_information(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    if call == "order_info":
        order = Order.objects.get(pk=order_id)
        number_order = f"Информация об заказе №{order.pk}\n" + "_" * 35
        inventory = "Информация об инвентаре\n"
        serviсes = "Информация об услугах\n"
        extra_service = "Информация об доп. услугах\n"

        for invent in order.order_inventories.all():
            inventory += (f' ◉ {invent.inventory.name} - {invent.amount} штук\n')

        for service in order.order_services.filter(service__is_extra=False):
            serviсes += (f''' ◉ {service.service.name}
        - Объем работ: {service.amount}
        - Коэффицент сложности: {service.rate}\n''')

        for service in order.order_services.filter(service__is_extra=True):
            extra_service += (f''' ◉ {service.service.name}
        - Объем работ: {service.amount}
        - Коэффицент сложности: {service.rate}\n''')

        info = '\n'.join(map(str, [number_order, serviсes, extra_service, inventory]))

        keyword = get_order_information_keyboard(order_id, staff_id)
        context.bot.send_message(chat_id=chat_id, text=info, reply_markup=keyword)


@is_staff_in_order
def order_information_update(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    if call == "info_update":
        number_order = f"Информация об заказе №{order.pk}\n" + "_" * 35
        inventory = "Информация об инвентаре\n"
        serviсes = "Информация об услугах\n"
        extra_service = "Информация об доп. услугах\n"

        for invent in order.order_inventories.all():
            inventory += (f' ◉ {invent.inventory.name} | {invent.amount} штук\n')

        for service in order.order_services.filter(service__is_extra=False):
            serviсes += (f''' ◉ {service.service.name}
        - Объем работ: {service.amount}
        - Коэффицент сложности: {service.rate}\n''')

        for service in order.order_services.filter(service__is_extra=True):
            extra_service += (f''' ◉ {service.service.name}
        - Объем работ: {service.amount}
        - Коэффицент сложности: {service.rate}\n''')

        keyword = get_order_information_keyboard(order_id, staff_id)
        try:
            info = '\n'.join(map(str, [number_order, serviсes, extra_service, inventory]))
            context.bot.edit_message_text(chat_id=chat_id, text=info, message_id=message_id, reply_markup=keyword)
        except:
            text = "Обновление информации о заказе отсутвуют!"
            context.bot.send_message(chat_id=chat_id, text=text)


@is_staff_in_order
def in_place_callback(update: Update, context: CallbackContext):
    service_list = []
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    staff = order.order_cleaners.get(staff=staff_id)
    service = ServiceOrder.objects.filter(order=order)
    if call == "in_place":
        staff.in_place = datetime.datetime.now().replace(second=0, microsecond=0)
        staff.save()
        for item in service:
            service_info = f'''◉ {item.service.name}\n --Oбъем: {item.amount} (м2/шт)\n --Сложность: {item.rate}'''
            service_list.append(service_info)
            services = '\n'.join(map(str, service_list))
        text = f"Список услуг заказа №{order.id}:\n{services}\nГотовы начать работу?"
        keyboard = get_brigadier_start_keyboard(order_id, staff_id)
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                      reply_markup=keyboard)


@is_staff_in_order
def work_start_callback(update: Update, context: CallbackContext):
    service_list = []
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    staff = order.order_cleaners.get(staff=staff_id)
    service = ServiceOrder.objects.filter(order=order)
    if call == "work_start":
        staff.work_start = datetime.datetime.now().replace(second=0, microsecond=0)
        staff.save()
        for item in service:
            service_info = f'''◉ {item.service.name}'''
            service_list.append(service_info)
            services = '\n'.join(map(str, service_list))
        text = f'Вы начали выполнять заказ №{order.id}\nУслуги: \n{services}'
        if staff.is_brigadier:
            keyboard = get_brigadier_end_keyboard(order_id, staff_id)
            context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                          reply_markup=keyboard)


@is_staff_in_order
def work_end_callback(update: Update, context: CallbackContext):
    service_list = []
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    staff = order.order_cleaners.get(staff=staff_id)
    service = ServiceOrder.objects.filter(order=order)
    if call == "work_end":
        staff.work_end = datetime.datetime.now().replace(second=0, microsecond=0)
        staff.save()
        for item in service:
            service_info = f'''-{item.service.name} ✔'''
            service_list.append(service_info)
            services = '\n'.join(map(str, service_list))
        text = f'Услуги заказа №{order.id}:\n{services}\nРабота завершена!'
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)


@is_staff_in_order
def photo_before_callback(update: Update, context: CallbackContext):
    service_list = []
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    staff = order.order_cleaners.get(staff=staff_id)
    service = ServiceOrder.objects.filter(order=order)
    if staff.is_brigadier and call == 'photo_before':
        for item in service:
            service_info = f'''◉ {item.service.name}'''
            service_list.append(service_info)
            services = '\n'.join(map(str, service_list))
        text = f'''Заказ №{order.id}\nУслуги: \n{services}\nЧтобы добавить ФОТО ДО,перейдите по ссылке:\nhttp://127.0.0.1:8000/order/{order.id}/'''
        keyboard = get_brigadier_start_keyboard(order_id, staff_id)
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                      reply_markup=keyboard)


@is_staff_in_order
def photo_after_callback(update: Update, context: CallbackContext):
    service_list = []
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    staff = order.order_cleaners.get(staff=staff_id)
    service = ServiceOrder.objects.filter(order=order)
    if staff.is_brigadier and call == 'photo_after':
        for item in service:
            service_info = f'''◉ {item.service.name}'''
            service_list.append(service_info)
            services = '\n'.join(map(str, service_list))
        text = f'''Заказ №{order.id}\nВыполнены услуги: \n{services}\nЧтобы добавить ФОТО ПОСЛЕ,перейдите по ссылке:\nhttp://127.0.0.1:8000/order/{order.id}/'''
        keyboard = get_brigadier_end_keyboard(order_id, staff_id)
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                      reply_markup=keyboard)
