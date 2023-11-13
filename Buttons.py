from aiogram import types


# Клавиатура
kb = [[types.KeyboardButton(text='🔐 Зашифровать сообщение'),
       types.KeyboardButton(text='🔓 Расшифровать сообщение')],
      [types.KeyboardButton(text='💰 Подписка'),
       types.KeyboardButton(text='🛠 Обратная связь')],
      [types.KeyboardButton(text='📄 Описание'),
      types.KeyboardButton(text='❌ Удалить переписку')]
      ]
keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                     resize_keyboard=True,
                                     input_field_placeholder="Введите сообщение#ключ шифрования")