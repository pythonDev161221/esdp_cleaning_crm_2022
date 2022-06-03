from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_staff_order_keyboard(order_id, staff_id) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Принять", callback_data=f'accept {order_id} {staff_id}'),
            InlineKeyboardButton("Отказатся", callback_data=f"refuse {order_id} {staff_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_refuses_keyboard(order_id, staff_id) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=f'retrue {order_id} {staff_id}'),
            InlineKeyboardButton("Нет", callback_data=f"refalse {order_id} {staff_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_in_place_keyboard(order_id, staff_id) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("На месте", callback_data=f'in_place {order_id} {staff_id}'),
            InlineKeyboardButton("Информация о заказе", callback_data=f'order_info {order_id} {staff_id}'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_order_information_keyboard(order_id, staff_id) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Обновить", callback_data=f'info_update {order_id} {staff_id}'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
