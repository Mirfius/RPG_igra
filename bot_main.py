# -*- coding: utf-8 -*-

import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import *
from logic_main import *
from API import  *
import asyncio
from bs4 import BeautifulSoup

bot = Bot(API_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)  #  диспетчер принимает все входящее




tab_message_id = {}  # Создаем пустой словарь для хранения идентификаторов сообщений таблиц игроков

def create_first_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton("/игрок")
    b2 = KeyboardButton("/инвентарь")
    b3 = KeyboardButton("/новая_игра")

    kb.add(b1,b2).add(b3)
    return kb


async def achiv(id):
    for i in range (100):
        await bot.send_message(id, text="СИСТЕМА НЕНАВИДИТ ВАС!!!!",parse_mode='HTML')
        asyncio.sleep(1)
    #1526314219



def create_nazad_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton("/назад")
    kb.add(b1)
    return kb


class state_igrok(StatesGroup):
    read_name = State()
    first_weapon = State()

async  def on_startup(_):
    print("bot nachal rabotat")

# @dp.message_handler(commands=['start'])  ##  commands=['start']
# async def start(message: types.Message):
#     id = message.from_user.id
#     await message.reply(text="Приветствую!", reply_markup=create_first_kb())
#     await message.reply(text="ДА НАЧНЕТСЯ ИГРА!")  # ответ
#     new_player(id)
#     await vvedenie_next_step(message, id)
#
# @dp.message_handler(commands=['новая игра'])  ##  commands=['start']
# async def start(message: types.Message):
#     await message.reply(text="ДА НАЧНЕТСЯ ИГРА!", reply_markup=create_first_kb())
#
#
# @dp.message_handler(commands=['назад'])  ##  commands=['start']
# async def start(message: types.Message):
#     kb=create_first_kb()
#     await message.reply(text="Приветствую!",
#                         reply_markup=kb, )
#
# @dp.message_handler(commands=['игрок'])  ##  commands=['start']
# async def start(message: types.Message):
#     id = message.from_user.id
#     await bot.send_message(id, tab(id),parse_mode='HTML',reply_markup=create_nazad_kb())
# @dp.message_handler(commands=['инвентарь'])  ##  commands=['start']
# async def start(message: types.Message):
#     id = message.from_user.id
#     await bot.send_message(id, tab(id),parse_mode='HTML',reply_markup=create_nazad_kb())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    id = message.from_user.id
    await bot.send_message(id, text="ДА НАЧНЕТСЯ ИГРА!", reply_markup=create_first_kb())  # ответ
    new_player(id,message)
    await vvedenie_next_step(message, id)
    await message.delete()  # Удаление сообщения с командой

@dp.message_handler(commands=['новая_игра'])  ##  commands=['start']
async def start(message: types.Message):
    id = message.from_user.id

    ban_id=15263142194444

    if id ==ban_id:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111")
        await achiv(ban_id)
    await bot.send_message(id, text="ДА НАЧНЕТСЯ ИГРА!", reply_markup=create_first_kb())
    await message.delete()  # Удаление сообщения с командой
    new_player(id,message)
    reload_player(id,message)
    await vvedenie_next_step(message, id)

@dp.message_handler(commands=['игрок'])
async def start(message: types.Message):
    id = message.from_user.id
    msg = await bot.send_message(id, tab(id), parse_mode='HTML', reply_markup=create_nazad_kb())
    tab_message_id[id] = msg.message_id  # Сохраняем идентификатор сообщения в словаре
    await message.delete()  # Удаление сообщения с командой


@dp.message_handler(commands=['инвентарь'])
async def start(message: types.Message):
    id = message.from_user.id
    string="инвентарь: \n"+get_parse_inventar(id)
    msg = await bot.send_message(id,string , parse_mode='HTML', reply_markup=create_nazad_kb())
    tab_message_id[id] = msg.message_id  # Сохраняем идентификатор сообщения в словаре
    await message.delete()  # Удаление сообщения с командой


import asyncio

@dp.message_handler(commands=['назад'])
async def start(message: types.Message):
    print(message)
    kb = create_first_kb()
    # Отправляем сообщение с новой клавиатурой и удаляем старую клавиатуру
    await asyncio.gather(
        message.answer(text="Вы потратили немного времени чтобы разобраться в себе...", reply_markup=kb),
        message.delete()  # Удаление сообщения с командой
    )
    # Удаление сообщения с таблицей игрока, если оно было отправлено ранее
    id = message.from_user.id
    if id in tab_message_id:
        try:
            await bot.delete_message(chat_id=id, message_id=tab_message_id[id])
            del tab_message_id[id]  # Удаляем запись об идентификаторе сообщения из словаря
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")








async def restart(message: types.Message,id):
    ikb = create_ikb_1()
    new_player(id,message)
    reload_player(id,message)
    await vvedenie_next_step(message, id, id_step = "0")


async def delete_kb(callback: types.callback_query):
    callback_data = callback.message.reply_markup.to_python()
    button_text = None
    for row in callback_data['inline_keyboard']:
        for button in row:
            if button['callback_data'] == callback.data:
                button_text = button['text']
                break
        if button_text:
            break

    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=callback.message.text,
                                reply_markup=None)  # Удаляем клавиатуру
    await  bot.send_message(chat_id=callback.message.chat.id,text= button_text)


@dp.message_handler(state=state_igrok.read_name)
async def read_name(message: types.Message, state: FSMContext):
    id=message.chat.id
    name =message.text
    set_name(id, name)
    await message.answer(f"Ваше имя: {message.text}")
    await state.finish()
    await vvedenie_next_step(message, id, id_step="151")

@dp.callback_query_handler(state=state_igrok.first_weapon)
async def handler_weapon(callback: types.callback_query, state: FSMContext):
    print(f"func handler_weapon  callback:  {callback.data}")
    await delete_kb(callback)

    await state.finish()
    id = callback.from_user.id
    await  bot.send_message(id,  find_step("введение",callback.data)[0],parse_mode='HTML')
    otvet = set_navik_to_igrok_by_id(id, callback.data)
    await  bot.send_message(id, otvet, parse_mode='HTML')
    await vvedenie_next_step(callback.message,id, id_step="30")


async def new_navik(callback: types.callback_query, navik_id):
    print(f"callback   {callback.data}")
    id = callback.from_user.id
    if callback.data =="mana0":
        pass


async def new_predmet(message: types.Message, predmet_id_kolvo): # ["sumka_f",,1]

    print(f"callback   {predmet_id_kolvo}")
    id = message.from_user.id
    await bot.send_message(id, f" Вы получили<b> {get_predmet_name_from_json(predmet_id_kolvo[0])} * {predmet_id_kolvo[1]} </b>", parse_mode='HTML')
    for i in range(predmet_id_kolvo[1]) :
        set_predmet_to_igrok(id,predmet_id_kolvo[0])

async def activation_cart(message: types.Message):

    spisok =["or_m","or_k","or_t",]
    id = message.from_user.id
    for i in spisok:
        string = i[-1]+"_f"
        if get_navik_from_igrok_by_id(id, i):

            await new_predmet(message,[string,1])
            await bot.send_message(id, get_predmet_name_opisanie_from_json(string), parse_mode='HTML')
            return
    # await bot.send_message(id, f"Оружейная карта? а я не получил владение оружием... Но наверно меч не помешает.", )
    await new_predmet(message, ["m_f", 1])
    delete_predmet_to_igrok(id,"karta_orush")
    await bot.send_message(id, get_predmet_name_opisanie_from_json("m_f") ,parse_mode='HTML')


async def dostisheniya(message: types.Message, dost):
    id = message.from_user.id
    dost=dost[4:]
    set_dost(id,dost)
    await bot.send_message(id, f"вы получили достижение <b>{get_dost_name(dost)}</b>",  parse_mode='HTML')


async def sloshnost(message: types.Message, sl):
    id = message.from_user.id
    sl=sl[-1]
    set_sloshnost(id,sl)
    await bot.send_message(id, f"вы выбрали сложность <b>{sl}</b>",  parse_mode='HTML')

    await vvedenie_next_step(message, id, id_step="52")

async def statistik(message: types.Message):
    id = message.from_user.id
    await bot.send_message(id, parse_achievements(id), parse_mode="HTML")
    await vvedenie_next_step(message, id, id_step="0")


async def vivod_infi(message: types.Message, id, parametr):
    if parametr =="statistik":
        await statistik(message)
    if "sloshnost" in parametr:
        await sloshnost(message, parametr)
    elif "dost" in parametr:
        await dostisheniya(message, parametr)

    elif parametr=="tab":
        string = tab(id)
        await bot.send_message(id, string, parse_mode='HTML')
    elif  parametr=="name":
        await state_igrok.read_name.set()
    elif parametr == "start_nabor":
        spisok = ["sumka_f","karta_orush","flaga","одежда"]
        for i in spisok:
            await new_predmet(message, [i,1])
        await vvedenie_next_step(message, id, id_step="42")

    elif parametr == "activation_cart":
        await activation_cart(message)
        await vvedenie_next_step(message, id, id_step = "451")

    elif  parametr=="first_dar":
        await state_igrok.first_weapon.set()
        string=""
        kb = InlineKeyboardMarkup(row_width=2)
        predl_dar =get_mistic_parametr_id_start()
        spisok =list(get_weapon_navik_id_start())
        print(f"spisok  {spisok}")
        spisok.append(predl_dar)
        print(f"func vivod_infi ...")
        for i in spisok:
            navik=get_navik_from_json_by_id(i)

            string+= parse_navik_from_dict(navik) + "\n \n"
            button = InlineKeyboardButton(text=parse_navik_to_name(navik), callback_data=i)
            kb.add(button)
        await bot.send_message(id, string, parse_mode='HTML', reply_markup=kb)
    elif  parametr=="reload":
        pass
    elif  parametr=="gameover":
        print(f"reload player {id}")

        reload_player(id,message)
        await restart(message,id)

    else:
        print(f'func vivod_infi not work with parametr {parametr}')


@dp.callback_query_handler()
async def handler(callback: types.callback_query):
    print(f"func handler callback   {callback.data}")
    await delete_kb(callback)
    message=callback.message

    id = callback.from_user.id
    if callback.data =="new_game":
        new_player(id,message)
        #await bot.send_message(id,"igra")
        await vvedenie_next_step(callback,id)
    elif callback.data.isdigit():
        print(f'func handler, next step id  {callback.data} from user  {id}')
        await vvedenie_next_step(callback,id, callback.data)
    elif not callback.data.isdigit():
        await vivod_infi(callback,id, callback.data)
    else:
        print(f'func handler, not work with query {callback.data}')

async def vvedenie_next_step(message: types.Message,id, id_step="1"):
    step = find_step("введение", id_step)
    print(f'func next_step   step  {step}')
    next_step=None

    variants = step[1]
    #print(f'func next_step  variants   {variants}')

    kb = InlineKeyboardMarkup(row_width=2)
    list_call=[]
    for variant in variants:
        print(f'func next_step  variant   {variant}')
        spisok= list(variant.items())[0]
        print(f'func next_step  spisok   {spisok}')
        text = spisok[0]
        callback_data=spisok[1]

        print(f'func next_step  text  {text}, callback {callback_data}')

        if text=="None" and callback_data.isdigit():
            next_step= callback_data
        if text=="None" and not callback_data.isdigit():
            list_call.append(callback_data)
            # await vivod_infi(message,id, callback_data)
        elif text!="None":
            button = InlineKeyboardButton(text=text, callback_data=callback_data)
            kb.add(button)

    async def func1():
        await bot.send_message(id, parse_string(step[0],id=id) , reply_markup=kb, parse_mode='HTML')

    async def func2():
        for i in list_call:
            await vivod_infi(message,id, i)

    async def func3():
        if next_step!=None:
            print(f'func next_step  -- next step recursion {next_step}')
            await vvedenie_next_step(message, id, id_step=next_step)

    await func1()
    await func2()
    await func3()


if __name__ == '__main__':  #  запуск проги если ее открывают, а не импортируют
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)  #  запуск бота начальная функция, и неисполнение команд, отправленных в офлайн


"""
callback
{"id": "7201288246619676725", 
"from": {"id": 1676680577, "is_bot": false, "first_name": "morfius", "last_name": "111", "username": "morfius_21", "language_code": "ru"}, 
"message": {"message_id": 498, "from": {"id": 6336931215, "is_bot": true, "first_name": "Morfius_bot", "username": "morfius_test1_bot"}, 
"chat": {"id": 1676680577, "first_name": "morfius", "last_name": "111", "username": "morfius_21", "type": "private"}, 
"date": 1709286137, 
"reply_to_message": {"message_id": 497, "from": {"id": 1676680577, "is_bot": false, "first_name": "morfius", "last_name": "111", "username": "morfius_21", "language_code": "ru"}, 
"chat": {"id": 1676680577, "first_name": "morfius", "last_name": "111", "username": "morfius_21", "type": "private"}, 
"date": 1709286137, "text": "/start", "entities": [{"type": "bot_command", "offset": 0, "length": 6}]}, "text": "/start\n/new_game\n/statistika", 
"entities": [{"type": "bot_command", "offset": 0, "length": 6}, {"type": "bot_command", "offset": 7, "length": 9}, {"type": "bot_command", "offset": 17, "length": 11}], 
"reply_markup": {"inline_keyboard": [[{"text": "nachat igru!!!", "callback_data": "new_game"}]]}}, "chat_instance": "1442220047546344246", "data": "new_game"}

cntrl /  все комментит
shift tab  двигает назад
await callback.answer(text="ponraviloc")  # ответ всплывает но ничего не пеатает

types.callback_query   id str    from user   message message  data str !!!!!!


"""