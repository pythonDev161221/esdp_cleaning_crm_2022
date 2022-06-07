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
