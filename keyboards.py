# -*- coding: utf-8 -*-


import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

HELP = """
/start
/new_game
/statistika
"""




def create_ikb_1():
    ikb = InlineKeyboardMarkup(row_width=3) # красивый вид  только 1 раз
    ib1=InlineKeyboardButton("НАЧАТЬ ВЕЛИКУЮ ИГРУ!!!", callback_data='new_game')
    ikb.add(ib1)
    return ikb

