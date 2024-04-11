# -*- coding: utf-8 -*-

from copy import deepcopy
import random
import json


directory ='./json_file/'
predmeti_js = './json_file/predmeti.json'
igroki_js = './json_file/igroki.json'
naviki_js = './json_file/naviki.json'
vragi_js = './json_file/vragi.json'
suchet_js = './json_file/suchet.json'
bonusi_js = './json_file/bonusi.json'
maps_js = './json_file/maps.json'
test_js = './json_file/test.json'


def read1_utf8(file_name):
    with open(file_name, 'r',encoding='cp1251') as file: ## encoding='utf-8' encoding='cp1251'
        data = json.load(file)
    with open(file_name, 'w',encoding='cp1251') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


#read1_utf8(naviki_js)



def read_js(file_name):
    try:
        with open(file_name, 'r', encoding='cp1251') as file:
            return json.load(file)
    except:
        print(f'file  {file_name}  not open')
        return -1

def write_js(file_name, data):
    try:
        with open(file_name, 'w', encoding='cp1251') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            return True
    except:
        print(f'file  {file_name}  not write')
        return False

def perezapis(file1):
    data = read_js(file1)
    write_js(file1,data)
perezapis(naviki_js)


import ast
import ast

import re

# Пример функций, которые будут вызваны
def my_function(x, y):
    return x + y

def another_function(a, b):
    return a * b



# Функция для поиска строки по ее ID
def find_step(chapter, id):
    # Предположим, что функция read_js() существует и читает JSON из файла
    story = read_js(suchet_js)
    #print( story["сюжет"][chapter])
    if story["сюжет"][chapter][id]:
        return story["сюжет"][chapter][id]
    else:
        return None
#print(find_step("введение", "1"))

def tab(id):
    data1 = read_js(igroki_js)
    data=data1["игроки"][str(id)]["персонаж"]["вывод"]
    # Форматирование строки
    result = (
        f"<b>имя</b>: {data['имя']}\n"
        f"<b>истинное имя</b>: {data['истинное имя']}\n"
        f"<b>уровень</b>: {data['уровень']}\n"
        f"<b>ранг</b>: {data['ранг']}\n"
        f"<b>ОС</b>: {data['ОС']}/{20*data['уровень']}\n"
        "<b>характеристики</b>: {\n"
    )

    # Добавление характеристик
    for key, value in data['характеристики'].items():
        result += f"    <b>{key}</b>: {value}\n"

    # Добавление навыков
    result += "<b>навыки</b>: [\n"
    for key,skill in data['навыки'].items():
        result += "    {\n"
        result += f"        <b>{skill['название']}</b>: \n"
        result += f"        <b>ранг</b>: {skill['ранг']} {skill['уровень']}\\{skill['предел']}\n"
        result += f"        <b>описание</b>: {skill['описание']}\n"
        result += "    }\n"
    result += "]\n"

    print(result)
    return result
#tab(3)





"""
навыки



"""

def get_navik_from_json_by_id(id):
    print(f"func get_navik_from_json by id {id}")
    data = read_js(naviki_js)
    navik = data["навыки"][id]
    print(f"func get_navik_from_json {navik} by id {id}")
    return navik

def get_weapon_navik_id_start():
    data = read_js(naviki_js)
    weapons=data["навыки"]
    filtered_weapons = []

    for weapon_id, weapon_info in weapons.items():
        if weapon_id[:2] == "or":
            #filtered_weapons.append(weapon_info)
            filtered_weapons.append(weapon_id)


    print(f"Первые навыки из категорий: {filtered_weapons} ")
    return filtered_weapons

# print(get_weapon_start()[1]["id"])

def get_mistic_parametr_id_start():
    data = read_js(naviki_js)
    first_skills = []
    spisok=['mana0','ci0','prana0','vi0']
    for i in spisok:
        first_skills.append(data['навыки'][i])

    probabilities = [1/(i+1) for i in range(len(first_skills))]
    #chosen_skill = random.choices(first_skills, weights=probabilities, k=1)[0]  # not id
    chosen_skill = random.choices(spisok, weights=probabilities, k=1)[0]

    print(f"Первые навыки из категорий: {first_skills}   {chosen_skill}")
    return chosen_skill

#get_mistic_parametr_start()

def parse_navik_to_name(skill_data):
    skill_name = skill_data['название']
    skill_rank = skill_data['ранг']
    skill_level = skill_data['уровень']
    skill_limit = skill_data['предел']
    print(f"{skill_name} ({skill_rank} {skill_level}/{skill_limit})")
    return f"{skill_name} ({skill_rank} {skill_level}/{skill_limit})"

#parse_skill_to_name(get_mistic_parametr_start())

def parse_navik_from_dict(skill):

    name = skill['название']
    rank = skill['ранг']
    level = skill['уровень']
    limit = skill['предел']
    description = skill['описание']

    parsed_skill = f"{name}: \n" \
                   f"<b>ранг: {rank} {level}\\{limit}</b>\n" \
                   f"<b>описание: </b>\n" \
                   f"{description}"

    return parsed_skill
#print(parse_skill(get_mistic_parametr_start())) !!!!

def set_navik_to_igrok_by_id(id, navik_id):
    data = read_js(igroki_js)
    navik =get_navik_from_json_by_id(navik_id)
    print(data)
    data["игроки"][str(id)]["персонаж"]["вывод"]["навыки"][navik_id]= navik
    print(f"func set_navik_by_id {navik} player id {id}")
    write_js(igroki_js, data)

    string ="Внимание! Вы получили навык \n" + parse_navik_from_dict(navik)
    return string

def get_navik_from_igrok_by_id(id, navik_id):
    data = read_js(igroki_js)
    igrok = data["игроки"].get(str(id))
    if igrok:
        naviki = igrok["персонаж"]["вывод"]["навыки"]

        if naviki.get(navik_id):
            return naviki[navik_id]
    return 0


# print(get_navik_from_igrok_by_id(806948129,"or_m"))

def get_navik(id):
    data = read_js(igroki_js)
    navik = data["игроки"][id]["персонаж"]["вывод"]["навыки"]
    print(f"func get_navik  {navik} player id {id}")
    return navik

def get_dar(id):
    data = read_js(igroki_js)
    dar = data["игроки"][id]["персонаж"]["предложенный_дар"]
    print(f"func get_dar get dar  {dar} player id {id}")
    return dar

def set_dar(id, dar):  # ????????????????
    data = read_js(igroki_js)
    data["игроки"]["персонаж"][id]["предложенный_дар"]= dar
    print(f"func set_dar set dar  {dar} player id {id}")
    write_js(igroki_js, data)
# set_name(1, "ssss")




"""
предметы


"""

def get_predmet_name_from_json(id):
    data = read_js(predmeti_js)
    print(f"func get_predmet_name  data {data}")
    return data["предметы"][id]["название"]
#print(get_predmet_name("k_f"))

def get_predmet_name_opisanie_from_json(id):
    data = read_js(predmeti_js)
    predmet = data["предметы"][id]
    string =f'<b>{predmet["название"]} </b> \n {predmet["описание"]} '
    return string
#print(get_predmet_name("k_f"))


def set_weapon_to_slot_into_inventar(id_igrok, id_weapon):
    data = read_js(igroki_js)
    weapon = data["игроки"][str(id_igrok)]["персонаж"]["инвентарь"][id_weapon]
    data["игроки"][str(id_igrok)]["персонаж"]["состояние"]["оружие"] = weapon
    write_js(igroki_js,data)
    print(f"func set_weapon_to_slot_into_inventar set({weapon}) to id {id_igrok}")

#set_weapon_to_slot_into_inventar("2", "m_f")


def get_weapon_from_slot_from_igrok(id_igrok):
    data = read_js(igroki_js)
    weapon = data["игроки"][str(id_igrok)]["персонаж"]["состояние"]["оружие"]
    print(f"get_weapon_from_slot_from_igrok({weapon}) to id {id_igrok}")
#print(get_weapon_from_slot_from_igrok("2"))

def set_predmet_to_igrok(id_igrok,id_predmet, nasichenie=0):
    data = read_js(predmeti_js)
    print(f"set_predmet_to_igrok  data {data}")
    predmet = data["предметы"][id_predmet]

    igrok_data = read_js(igroki_js)
    inventar = igrok_data["игроки"][str(id_igrok)]["персонаж"]["инвентарь"]

    predmet_exists = False
    if id_predmet  in inventar:
        predmet_exists = True
        item = inventar[id_predmet]
        if "количество" in item:
            item["количество"] += 1
        if "насыщение" in item:
            item["насыщение"].append(nasichenie)
            item["насыщение"] = sorted(item["насыщение"], reverse=True)

    if not predmet_exists:
        if "насыщение" in predmet:
            predmet["насыщение"][0] = nasichenie
        inventar[id_predmet]=predmet

    write_js(igroki_js,igrok_data)

def delete_predmet_to_igrok(id_igrok,id_predmet):
    igrok_data = read_js(igroki_js)
    inventar = igrok_data["игроки"][str(id_igrok)]["персонаж"]["инвентарь"]
    predmet_exists = False
    if id_predmet  in inventar:
        predmet_exists = True
        item = inventar[id_predmet]
        if "количество" in item:
            item["количество"] -= 1
        if "насыщение" in item:
            item["насыщение"].pop()

    write_js(igroki_js,igrok_data)
    print(f"func delete_predmet_to_igrok id  {id_predmet}")

    return predmet_exists

#set_predmet_to_igrok("2","m_f", nasichenie=7)

def get_inventar(id):
    data = read_js(igroki_js)
    inventar = data["игроки"][str(id)]["персонаж"]["инвентарь"]
    return inventar


def get_parse_inventar(id):
    data = read_js(igroki_js)
    inventar = data["игроки"][str(id)]["персонаж"]["инвентарь"]
    formatted_text = ""
    for item in inventar.values():
        nasichenie = item.get("насыщение", "")
        if isinstance(nasichenie, list):
            nasichenie = ", ".join(map(str, nasichenie))
            formatted_text += f"<b>{item['название']}</b>\n{item['описание']}\n {nasichenie}\n\n"
        else:
            formatted_text += f"<b>{item['название']}</b>\n{item['описание']}\n*Количество:* {item['количество']} \n\n"
    return formatted_text

"""
сложность и карта!!!

"""

def set_sloshnost(id, sl):
    data =read_js(igroki_js)

    data["игроки"][str(id)]["персонаж"]["сложность"]=sl
    write_js(igroki_js, data)
    print(f"func set_sloshnost {sl} player id {id}")
# set_dost(id, id_dost)

def get_sloscnost(id):
    data = read_js(igroki_js)
    sl = data["игроки"][str(id)]["персонаж"]["сложность"]

    print(f"func get_sloshnost {sl} player id {id}")
    return  sl

"""
игроки!

"""

def new_player(id, message=None):
    data = read_js(igroki_js)
    players = data["игроки"]

    if str(id) in players:
        print("Игрок уже существует.")
        return

    shablon = deepcopy(data["шаблон"]["0"])

    for key in shablon["персонаж"]["вывод"]["характеристики"]:
        shablon["персонаж"]["вывод"]["характеристики"][key] += random.randint(0, 4)
    try:
        name=message.from_user.first_name
        shablon["персонаж"]["вывод"]["имя"]=name
        shablon["персонаж"]["вывод"]["истинное имя"] = name
    except:
        pass

    data["игроки"][id] = shablon
    write_js(igroki_js, data)
    print(f"func new_player write player id {id}")

def reload_player(id,message):
    data = read_js(igroki_js)
    players = data["игроки"]

    if str(id) not in players:
        print("Игрок не найден.")
        return


    personash = deepcopy(data["шаблон"]["0"]["персонаж"])

    for key in personash["вывод"]["характеристики"]:
        personash["вывод"]["характеристики"][key] += random.randint(0, 4)
    try:
        name = message.from_user.first_name
        personash["вывод"]["имя"] = name
        personash["вывод"]["истинное имя"] = name
    except:
        pass

    players[str(id)]["персонаж"] = personash
    write_js(igroki_js, data)
    print(f"func reload_player write player id {id}")

def set_name(id, name):
    try:
        with open(test_js, 'r', encoding='cp1251') as file:
            data = json.load(file)
            data["игроки"] = name
        with open(test_js, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    except:
        data = read_js(igroki_js)
        data["игроки"][str(id)]["персонаж"]["вывод"]["имя"] = "%%%%%%%%"
        write_js(igroki_js, data)
        print(f"func choose_name EXCEPTION player id {id}")
        data={}
        write_js(test_js, data)
    else:
        data = read_js(igroki_js)
        data["игроки"][str(id)]["персонаж"]["вывод"]["имя"] = name
        write_js(igroki_js, data)
        print(f"func choose_name  {name} player id {id}")


# set_name(1, "ssss")

def get_name(id):
    data = read_js(igroki_js)
    print(f"func get_name get name  player id {id}")
    return data["игроки"][str(id)]["персонаж"]["вывод"]["имя"]
# get_name(1)



def set_dost(id, id_dost):
    data =read_js(bonusi_js)
    dost=data[id_dost]

    data = read_js(igroki_js)
    data["игроки"][str(id)]["статистика"]["достижения"][id_dost]=dost
    write_js(igroki_js, data)
    print(f"func set_dost {id_dost} player id {id}")
# set_dost(id, id_dost)

def get_dost_name(id_dost):
    data =read_js(bonusi_js)
    dost=data[id_dost]["название"]
    return dost



"""
местность

"""

def set_mest(id, karta_list):

    data = read_js(igroki_js)
    data["игроки"][str(id)]["персонаж"]["карта"]= karta_list
    write_js(igroki_js, data)
    print(f"func set_mest {karta_list} player id {id}")
# set_dost(id, id_dost)

def get_mest(id):
    data = read_js(igroki_js)
    karta_list = data["игроки"][str(id)]["персонаж"]["карта"]

    print(f"func get_mest {karta_list} player id {id}")
    return karta_list


def change_mest(id, deystvie):
    data_grok = read_js(igroki_js)
    igrok = data_grok["игроки"][str(id)]

    # Получаем текущую позицию игрока
    poziciya = igrok["персонаж"]["позиция"]

    # Получаем карту, на которой находится игрок
    igrok_mest = igrok["персонаж"]["позиция"]
    data_maps = read_js(maps_js)
    mapa = data_maps["maps"][igrok_mest[0]]

    # Получаем размеры карты
    stroka = len(mapa)-1
    stolbec = len(mapa[0])-1
    vibor = {"right": 0, "left": 0, "up": 0, "down": 0,"new":0}

    # Определяем новую позицию игрока в зависимости от действия
    new_poziciya = poziciya.copy()
    y = new_poziciya[1]
    x = new_poziciya[2]

    if deystvie == "up":  # обработка вверх
        if mapa[y][x] == 1 and y==0: # если переход в иной круг
            mapa= data_maps["maps"][igrok_mest[0]-1] # меняем карту
            new_poziciya[0]-=1 # меняем номер карты в позиции
            y,x=len(mapa)-1,0 # меняем координаты
            vibor["new"]=1 # ссобщаем об изменении

        else:
            y -= 1
    elif deystvie == "down":
        if mapa[y][x] == 1 and y==stroka:
            mapa = data_maps["maps"][igrok_mest[0]-1]
            new_poziciya[0] += 1
            y, x = 0,0
            vibor["new"] = 1
        else:
            y += 1
    elif deystvie == "left":
        x -= 1
    elif deystvie == "right":
        x += 1


    if x<0: # зацикливание карты
        x =stolbec
    if x> stolbec:
        x =0

    # Проверяем, можно ли перейти в новую позицию
    if 0 <= y <= stroka:
        igrok["персонаж"]["позиция"] = [new_poziciya[0],y,x]

        write_js(igroki_js, data_grok)
    else:
        pass
        return -1



    if mapa[y][ x]==1:
        if y==0:
            vibor["up"]=1
        if y==stroka:
            vibor["down"]=1

    elif True:
        if y==0:
            vibor["up"]=-1
        if y==stroka:
            vibor["down"]=-1

    return vibor

print(change_mest(2, "up"))







# set_dost(id, id_dost)

def parse_achievements(id ):
    data = read_js(igroki_js)
    json_data = data["игроки"][str(id)]["статистика"]["достижения"]
    result_bad = "<b>Плохие</b>\n"
    result_neutral ="<b>Нейтральные</b>\n"
    result_good = "<b>Хорошие</b>\n"

    for key, value in json_data.items():
        # Получаем тип достижения
        achievement_type = value.get("тип")


        # Формируем строку с названием достижения
        achievement_name = f"<b>{value.get('название')}</b>"
        # Формируем строку с описанием достижения, обрамляем её звёздочками
        achievement_description = f"{value.get('описание')}"
        # Формируем строку с достижением
        achievement = f"{achievement_name}- {achievement_description}\n\n"

        # Добавляем достижение в соответствующий результат в зависимости от типа
        if achievement_type == -1:
            result_bad += achievement
        elif achievement_type == 0:
            result_neutral += achievement
        elif achievement_type == 1:
            result_good += achievement

    # Собираем все строки в одну строку
    result ="Список достижений\n\n" +result_bad +"\n\n" +result_neutral +"\n\n"+ result_good
    return result

#new_player(2)
#reload_player(2,"dd")
#print(parse_achievements("2"))




# Пример использования функции
#new_player(2)
#reload_player(806948129)


# Функция для обработки вызова функции из строки с переменными
def parse_string(string, *args, **kwargs):
    # Паттерн для поиска фигурных скобок с содержимым
    pattern = r'{(.*?)}'
    # Функция для замены совпадений
    def replace(match):
        # Получение содержимого фигурных скобок
        content = match.group(1)
        # Вызов функции с аргументами и переменными
        try:
            return str(eval(content, globals(), kwargs))
        except Exception as e:
            print(f"Error evaluating {content}: {e}")
            return match.group(0)  # Вернуть исходную строку, если возникла ошибка
    # Замена фигурных скобок на результаты вызываемых функций с переменными
    result = re.sub(pattern, replace, string)
    return result


#result = parse_string("Заявленный уровень сложности: {get_sloscnost(id)}", id=806948129)
#print("Result:", result)