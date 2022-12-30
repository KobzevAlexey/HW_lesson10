from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from config import TOKEN
from calc import calc_main
from calc_complex import calc_complex_main
from calc_fraction import calc_fraction_main
from calc_log_reader import log_reader
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nДля вывода списка комманд введите /help")


# Oбъект инлайн-клавиатуры
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
keyboard2: InlineKeyboardMarkup = InlineKeyboardMarkup()
keyboard3: InlineKeyboardMarkup = InlineKeyboardMarkup()

# Oбъекты инлайн-кнопок
button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Калькулятор',
    callback_data='/calculate')

button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='Развлечения',
    callback_data='/fun')

button_3: InlineKeyboardButton = InlineKeyboardButton(
    text='Принятие решений',
    callback_data='/yn_ann')

button_4: InlineKeyboardButton = InlineKeyboardButton(
    text='Cамое важное',
    callback_data='/best')

button_jokes: InlineKeyboardButton = InlineKeyboardButton(
    text='Шутка',
    callback_data='/joke')

button_cats: InlineKeyboardButton = InlineKeyboardButton(
    text='Котики',
    callback_data='/cats')

button_yesno: InlineKeyboardButton = InlineKeyboardButton(
    text='Получить ответ',
    callback_data='/ynn')

# Добавляем кнопки в клавиатуру методом add
keyboard.add(button_1).add(button_2).add(button_3).add(button_4)
keyboard2.add(button_jokes).add(button_cats)
keyboard3.add(button_yesno)


# Этот хэндлер будет срабатывать на команду "/start" и отправлять в чат клавиатуру
@dp.message_handler(commands=['help'])
async def process_help_command(message: Message):
    await message.answer(text='Вот, что у меня есть:',
                         reply_markup=keyboard)


# Этот хэндлер будет срабатывать на кнопку "развлечения" и отправлять в чат другую клавиатуру
async def process_buttons_fun(message: types.Message):
    await bot.send_message(message.from_user.id, text='А из развлечений у нас:',
                           reply_markup=keyboard2)


# Этот хэндлер будет срабатывать на кнопку "Принятие решений" и отправлять в чат другую третью
async def process_buttons_yn_ann(message: types.Message):
    await bot.send_message(message.from_user.id, text='Задай вопрос и нажми кнопку:',
                           reply_markup=keyboard3)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data '/calculate'
async def process_buttons_calc(message: types.Message):
    # await callback.answer('qqq')
    await bot.send_message(message.from_user.id, f'''Есть несколько видов калькуляторов:
      Для простых чисел: /eval <выражение>
      Для комплексных чисел: /complex <a+bj + c-dj>
      Для дробных чисел: /fraction <a/b + c/d>
      Просмотр лога калькулятора: /calc_log''')


# Этот хэндлер будет срабатывать на кнопку "шутка"
async def process_buttons_joke(message: types.Message):
    await bot.send_message(message.from_user.id, joke())


# Этот хэндлер будет срабатывать на кнопку "котики"
async def process_buttons_cats(message: types.Message):
    await bot.send_photo(message.from_user.id, cat())


# Этот хэндлер будет срабатывать на кнопку "Получить ответ"
async def process_buttons_yn(message: types.Message):
    await bot.send_document(message.from_user.id, yesno())


# Этот хэндлер будет делать самую крутую штуку
async def process_buttons_best(message: types.Message):
    await bot.send_message(message.from_user.id, 'https://youtu.be/dQw4w9WgXcQ')


# Регистрируем хэндлеры в диспетчере
dp.register_callback_query_handler(process_buttons_calc,
                                   text='/calculate')

dp.register_callback_query_handler(process_buttons_fun,
                                   text='/fun')

dp.register_callback_query_handler(process_buttons_joke,
                                   text='/joke')

dp.register_callback_query_handler(process_buttons_cats,
                                   text='/cats')

dp.register_callback_query_handler(process_buttons_yn_ann,
                                   text='/yn_ann')

dp.register_callback_query_handler(process_buttons_yn,
                                   text='/ynn')

dp.register_callback_query_handler(process_buttons_best,
                                   text='/best')


# @dp.message_handler(commands=['help'])
# async def process_help_command(message: types.Message):
#     await message.reply('''Калькулятор: /calculate\nРазвлечения: /fun\nПринятие решений: /yn_ann\nИ самое важное: /best
#       Тест кнопок: /test''')


@dp.message_handler(process_buttons_calc, text='/calculate')
async def process_calc_command(message: types.Message):
    await message.reply(f'''Есть несколько видов калькуляторов:
      Для простых чисел: /eval <выражение>
      Для комплексных чисел: /complex <a+bj + c-dj>
      Для дробных чисел: /fraction <a/b + c/d>
      Просмотр лога калькулятора: /calc_log''')


@dp.message_handler(commands=['complex'])
async def process_complex_command(message: types.Message, command: Command):
    await message.reply(f"По моим подсчетам {calc_complex_main(command.args)}")


@dp.message_handler(commands=['fraction'])
async def process_fraction_command(message: types.Message, command: Command):
    await message.reply(f"По моим подсчетам {calc_fraction_main(command.args)}")


@dp.message_handler(commands=['calc_log'])
async def process_calc_log_command(message: types.Message):
    await message.reply(log_reader())


@dp.message_handler(commands=['eval'])
async def process_eval_command(message: types.Message, command: Command):
    await message.reply(f"По моим подсчетам {calc_main(command.args)}")


@dp.message_handler(commands=['fun'])
async def process_fun_command(message: types.Message):
    await message.reply(f'''Есть шутки: /joke\nЕсть котики: /cat\n''')


@dp.message_handler(commands=['joke'])
async def process_joke_command(message: types.Message):
    await message.reply(joke())


@dp.message_handler(commands=['cat'])
async def process_cat_command(message: types.Message):
    image = cat()
    await bot.send_photo(message.chat.id, image)


@dp.message_handler(commands=['yn_ann'])
async def process_yn_ann_command(message: types.Message):
    await message.reply(f'''Не знаешь, делать что-то или нет? Задай вопрос! Я скину гифку с ответом: /Yes_No''')


@dp.message_handler(commands=['Yes_No'])
async def process_yesno_command(message: types.Message):
    image = yesno()
    await bot.send_document(message.chat.id, image)


@dp.message_handler(commands=['best'])
async def proces_best_command(message: types.Message):
    video = 'https://youtu.be/dQw4w9WgXcQ'
    await bot.send_message(message.chat.id, video)


if __name__ == '__main__':
    executor.start_polling(dp)
