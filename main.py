#попробовать сначала загрущить все фотографии на сервер чтобы было быстрее!!!!!!!!!!!!!
#при необходимстои спец программа будет эти логи считывать и формировать в список систематизированный по участникам!!!!!!!!!!!
#сделать напоминания об оплате хз
#возможность отправлять гифки и презы хз
#проверить что прога не отключается чрез время!!!!!!!!!!!!!
#разобраться со временем отклика и задержками!!!!!!!!!!!!
#бан ща спам
import json
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload
#подключение к сессии
token = "vk1.a.KUBo0_Odxv_FDMkct7yUIRlAR5qaOLzz6-N8j_5u3Jcf-l9xhZPKFY6GdQv53It1JFk4NZAYdvAhdAIJkxi4_i0NFmB9ISybgWZbGGbnOvlYLDTt1k4blBlcT4K5GgQ2I-EI_fgnvQeIdTUJnpvpDH8VP4pzx5-SSVNVNfRcNAsR4hn6aeq70NUQFv-hh2YO"
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, "214807798")
upload = vk_api.VkUpload(vk)
print("yep")
#подгрущка файлов
log_ans = open("log_ans.txt", "a")
list_of_users = open("list_of_users.txt", 'a+')
curr_ans = open("curr_ans.txt", "a+")
#основные функции
def SendPhoto (photo_yep):
    attachment = []
    if len(photo_yep)<=10:
        for i in photo_yep:
            photo = upload.photo_messages(i)
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment.append(f'photo{owner_id}_{photo_id}_{access_key}')
        vk.messages.send(peer_id=event.object.peer_id,messages='вот', random_id=0, attachment=attachment)
    else:
        attachment = []
        kl = 0
        for i in photo_yep:
            kl+=1
            photo = upload.photo_messages(i)
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment.append(f'photo{owner_id}_{photo_id}_{access_key}')
            if kl%10==0 or kl==len(photo_yep):
                vk.messages.send(peer_id=event.object.peer_id, messages='вот', random_id=0, attachment=attachment)
                attachment = []
'''
def send_file (file_yep):
    file = upload.document_message(file_yep)
    #owner_id = file[0]['owner_id']
    #photo_id = file[0]['id']
    #access_key = file[0]['access_key']
    #№attachment=(f'file{owner_id}_{photo_id}_{access_key}')
    #vk.messages.send(peer_id=event.object.peer_id, messages='вот', random_id=0, attachment=attachment)'''
def SendMessage( text):
    if event.type == VkBotEventType.MESSAGE_NEW:
        vk.messages.send(peer_id=event.object.message["peer_id"], message=text, random_id=randint(1, 100))
    else:
        vk.messages.send(peer_id=event.object.peer_id, message=text, random_id=randint(1, 100), time=5)
def SendKeyboard (keyboard):
    vk.messages.send(peer_id=event.object.message["peer_id"], message="вот", random_id=randint(1, 100), keyboard=keyboard.get_keyboard())

def keyboard_cr (array, last):
    keyb = VkKeyboard(one_time=False, inline=True)
    if len(array)>5:
        k=0
    for i in array:
        if len(i)==2:
            keyb.add_callback_button(label=i[0], color=VkKeyboardColor.POSITIVE, payload={"type": i[1]})
        else:
            keyb.add_callback_button(label=i[0], color=VkKeyboardColor.PRIMARY,
                                              payload={"type": "open_link", "link": i[1]})
        if len(array)>5:
            if k%2==1 :
                keyb.add_line()
            k+=1
        else:
            keyb.add_line()
    keyb.add_callback_button(label="Назад", color=VkKeyboardColor.PRIMARY, payload={"type": last})
    return keyb

#создвние основных меню
keyboard_menu = VkKeyboard(one_time=False, inline=True)
keyboard_menu.add_callback_button(label='Вся информация по курсу', color=VkKeyboardColor.PRIMARY, payload={"type": "info"})
keyboard_menu.add_line()
keyboard_menu.add_callback_button(label='Бесплатный файл', color=VkKeyboardColor.PRIMARY, payload={"type": "open_link", "link": "https://vk.com/s/v1/doc/2YEsIO7A5RpuzGWRE5Vx8C1WwKo-manGIkm-RzldVkiZRKmLEjA"})
keyboard_menu.add_line()
keyboard_menu.add_callback_button(label='Курс по русскому', color=VkKeyboardColor.POSITIVE, payload={"type": "russ_menu"})
keyboard_menu.add_line()
keyboard_menu.add_callback_button(label='Курс по математике', color=VkKeyboardColor.POSITIVE, payload={"type": "math_menu"})
keyboard_menu.add_line()
keyboard_menu.add_callback_button(label='Поддержка', color=VkKeyboardColor.NEGATIVE, payload={"type": "open_link", "link": "https://vk.com/bumega"})

#соответствие кнопок и сигналов которые отправляются при их нажатии
keyboard_math_menu = keyboard_cr([["задания 1-9", "math_1_9"], ["задания 10-18", "math_10_18"]], "back_to_menu")
keyboard_math_1_9 = keyboard_cr([["задание 1", "math_1"], ["задание 2", "math_2"], ["задание 3", "math_3"], ["задание 4", "math_4"], ["задание 5", "math_5"], \
                                 ["задание 6", "math_6"], ["задание 7", "math_7"], ["задание 8", "math_8"], ["задание 9", "math_9"] \
                                 ], "back_to_math_menu")
keyboard_math_10_18 = keyboard_cr([["задание 10", "math_10"], ["задание 11", "math_11"], ["задание 12-14", "math_12_14"], ["задание 15", "math_15"], \
                                ["задание 17", "math_17"], ["задание 18", "math_18"], ["задание 16", "math_16"], ["задание 13", "math_13"] \
                                 ], "back_to_math_menu")

keyboard_russ_menu = keyboard_cr([["задания 2-8", "russ_2_8"], ["задания 9-15", "russ_9_15"], ["задания 16-21", "russ_16_21"],\
                                  ["задания 1, 22-26", "russ_22_26"], ["сочинение", "russ_27"]], "back_to_menu")
keyboard_russ_2_8 = keyboard_cr([["задание 2", "russ_2"], ["задание 3", "russ_3"], ["задание 4", "russ_4"], ["задание 5", "russ_5"], ["задание 6", "russ_6"], \
                                 ["задание 7", "russ_7"], ["задание 8", "russ_8"]], "back_to_russ_menu")
keyboard_russ_9_15 = keyboard_cr([["задание 9", "russ_9"], ["задание 10", "russ_10"], ["задание 11", "russ_11"], ["задание 12", "russ_12"], \
                                 ["задание 13", "russ_13"], ["задание 14", "russ_14"], ["задание 15", "russ_15"]], "back_to_russ_menu")
keyboard_russ_16_21 = keyboard_cr([["задание 16", "russ_16"], ["задание 17", "russ_17"], ["задание 18", "russ_18"], ["задание 19", "russ_19"], \
                                 ["задание 20", "russ_20"], ["задание 21", "russ_21"]], "back_to_russ_menu")
keyboard_russ_22_26 = keyboard_cr([["задание 1", "russ_1"],["задание 22", "russ_22"], ["задание 23", "russ_23"], ["задание 24", "russ_24"], ["задание 25", "russ_25"], \
                                 ["задание 26", "russ_26"]], "back_to_russ_menu")
keyboard_russ_27 = keyboard_cr([["материалы урока", "russ_mater_27"], ["домашнее задание", "russ_zd_27"]], "back_to_russ_menu")



keyboard_russ_1 = keyboard_cr([["материалы урока", "russ_mater_1"], ["домашнее задание", "russ_zd_1"]], "back_to_russ_22_26")
keyboard_russ_2 = keyboard_cr([["материалы урока", "russ_mater_2"], ["домашнее задание", "russ_zd_2"]], "back_to_russ_2_8")
keyboard_russ_3 = keyboard_cr([["материалы урока", "russ_mater_3"], ["домашнее задание", "russ_zd_3"]], "back_to_russ_2_8")
keyboard_russ_4 = keyboard_cr([["материалы урока", "russ_mater_4"], ["домашнее задание", "russ_zd_4"]], "back_to_russ_2_8")
keyboard_russ_5 = keyboard_cr([["материалы урока", "russ_mater_5"], ["домашнее задание", "russ_zd_5"]], "back_to_russ_2_8")
keyboard_russ_6 = keyboard_cr([["материалы урока", "russ_mater_6"], ["домашнее задание", "russ_zd_6"]], "back_to_russ_2_8")
keyboard_russ_7 = keyboard_cr([["материалы урока", "russ_mater_7"], ["домашнее задание", "russ_zd_7"]], "back_to_russ_2_8")
keyboard_russ_8 = keyboard_cr([["материалы урока", "russ_mater_8"], ["домашнее задание", "russ_zd_8"]], "back_to_russ_2_8")
keyboard_russ_9 = keyboard_cr([["материалы урока", "russ_mater_9"], ["домашнее задание", "russ_zd_9"]], "back_to_russ_9_15")
keyboard_russ_10 = keyboard_cr([["материалы урока", "russ_mater_10"], ["домашнее задание", "russ_zd_10"]], "back_to_russ_9_15")
keyboard_russ_11 = keyboard_cr([["материалы урока", "russ_mater_11"], ["домашнее задание", "russ_zd_11"]], "back_to_russ_9_15")
keyboard_russ_12 = keyboard_cr([["материалы урока", "russ_mater_12"], ["домашнее задание", "russ_zd_12"]], "back_to_russ_9_15")
keyboard_russ_13 = keyboard_cr([["материалы урока", "russ_mater_13"], ["домашнее задание", "russ_zd_13"]], "back_to_russ_9_15")
keyboard_russ_14 = keyboard_cr([["материалы урока", "russ_mater_14"], ["домашнее задание", "russ_zd_14"]], "back_to_russ_9_15")
keyboard_russ_15 = keyboard_cr([["материалы урока", "russ_mater_15"], ["домашнее задание", "russ_zd_15"]], "back_to_russ_9_15")
keyboard_russ_16 = keyboard_cr([["материалы урока", "russ_mater_16"], ["домашнее задание", "russ_zd_16"]], "back_to_russ_16_21")
keyboard_russ_17 = keyboard_cr([["материалы урока", "russ_mater_17"], ["домашнее задание", "russ_zd_17"]], "back_to_russ_16_21")
keyboard_russ_18 = keyboard_cr([["материалы урока", "russ_mater_18"], ["домашнее задание", "russ_zd_18"]], "back_to_russ_16_21")
keyboard_russ_19 = keyboard_cr([["материалы урока", "russ_mater_19"], ["домашнее задание", "russ_zd_19"]], "back_to_russ_16_21")
keyboard_russ_20 = keyboard_cr([["материалы урока", "russ_mater_20"], ["домашнее задание", "russ_zd_20"]], "back_to_russ_16_21")
keyboard_russ_21 = keyboard_cr([["материалы урока", "russ_mater_21"], ["домашнее задание", "russ_zd_21"]], "back_to_russ_16_21")
keyboard_russ_22 = keyboard_cr([["материалы урока", "russ_mater_22"], ["домашнее задание", "russ_zd_22"]], "back_to_russ_22_26")
keyboard_russ_23 = keyboard_cr([["материалы урока", "russ_mater_23"], ["домашнее задание", "russ_zd_23"]], "back_to_russ_22_26")
keyboard_russ_24 = keyboard_cr([["материалы урока", "russ_mater_24"], ["домашнее задание", "russ_zd_24"]], "back_to_russ_22_26")
keyboard_russ_25= keyboard_cr([["материалы урока", "russ_mater_25"], ["домашнее задание", "russ_zd_25"]], "back_to_russ_22_26")
keyboard_russ_26 = keyboard_cr([["материалы урока", "russ_mater_26"], ["домашнее задание", "russ_zd_26"]], "back_to_russ_22_26")



keyboard_math_1 = keyboard_cr([["материалы урока", "math_mater_1"], ["домашнее задание", "https://ege.sdamgia.ru/test?id=47702058", "callb"]], "back_to_math_1_9")
keyboard_math_2 = keyboard_cr([["материалы урока", "math_mater_2"], ["домашнее задание", "math_zd_2"]], "back_to_math_1_9")
keyboard_math_3 = keyboard_cr([["материалы урока", "math_mater_3"], ["домашнее задание", "math_zd_3"]], "back_to_math_1_9")
keyboard_math_4 = keyboard_cr([["материалы урока", "math_mater_4"], ["домашнее задание", "math_zd_4"]], "back_to_math_1_9")
keyboard_math_5 = keyboard_cr([["материалы урока", "math_mater_5"], ["домашнее задание", "math_zd_5"]], "back_to_math_1_9")
keyboard_math_6 = keyboard_cr([["материалы урока", "math_mater_6"], ["домашнее задание", "math_zd_6"]], "back_to_math_1_9")
keyboard_math_7 = keyboard_cr([["материалы урока", "math_mater_7"], ["домашнее задание", "math_zd_7"]], "back_to_math_1_9")
keyboard_math_8 = keyboard_cr([["материалы урока", "math_mater_8"], ["домашнее задание", "math_zd_8"]], "back_to_math_1_9")
keyboard_math_9 = keyboard_cr([["материалы урока", "math_mater_9"], ["домашнее задание", "math_zd_9"]], "back_to_math_1_9")
keyboard_math_10 = keyboard_cr([["материалы урока", "math_mater_10"], ["домашнее задание", "math_zd_10"]], "back_to_math_10_18")
keyboard_math_11 = keyboard_cr([["материалы урока", "math_mater_11"], ["домашнее задание", "math_zd_11"]], "back_to_math_10_18")
keyboard_math_12_14 = keyboard_cr([["урок 1", "math_12_14_ur1"], ["урок 2", "math_12_14_ur2"], ["урок 3", "math_12_14_ur3"], \
                                   ["урок 4", "math_12_14_ur4"], ["урок 5", "math_12_14_ur5"]], "back_to_math_10_18")
keyboard_math_15 = keyboard_cr([["урок 1", "math_15_ur1"], ["урок 2", "math_15_ur2"], ["урок 3", "math_15_ur3"]], "back_to_math_10_18")
keyboard_math_17 = keyboard_cr([["урок 1", "math_17_ur1"], ["урок 2", "math_17_ur2"], ["урок 3", "math_17_ur3"], \
                                ["урок 4", "math_17_ur4"], ["урок 5", "math_17_ur5"], \
                                ["урок 6", "math_17_ur6"]], "back_to_math_10_18")
keyboard_math_18 = keyboard_cr([["урок 1", "math_18_ur1"], ["урок 2", "math_18_ur2"], ["урок 3", "math_18_ur3"], \
                                ["урок 4", "math_18_ur4"], ["урок 5", "math_18_ur5"], \
                                ["урок 6", "math_18_ur6"]], "back_to_math_10_18")
keyboard_math_16 = keyboard_cr([["урок 1", "math_16_ur1"], ["урок 2", "math_16_ur2"], ["урок 3", "math_16_ur3"], \
                                ["урок 4", "math_16_ur4"], ["урок 5", "math_16_ur5"], \
                                ["урок 6", "math_16_ur6"]], "back_to_math_10_18")
keyboard_math_13 = keyboard_cr([["урок 1", "math_13_ur1"], ["урок 2", "math_13_ur2"], ["урок 3", "math_13_ur3"], \
                                ["урок 4", "math_13_ur4"], ["урок 5", "math_13_ur5"], \
                                ["урок 6", "math_13_ur6"]], "back_to_math_10_18")

keyboard_math_12_14_ur1 =  keyboard_cr([["материалы урока", "math_mater_12_14_ur1"], ["домашнее задание", "math_zd_12_14_ur1"]], "back_to_math_12_14")
keyboard_math_12_14_ur2 =  keyboard_cr([["материалы урока", "math_mater_12_14_ur2"], ["домашнее задание", "math_zd_12_14_ur2"]], "back_to_math_12_14")
keyboard_math_12_14_ur3 =  keyboard_cr([["материалы урока", "math_mater_12_14_ur3"], ["домашнее задание", "math_zd_12_14_ur3"]], "back_to_math_12_14")
keyboard_math_12_14_ur4 =  keyboard_cr([["материалы урока", "math_mater_12_14_ur4"], ["домашнее задание", "math_zd_12_14_ur4"]], "back_to_math_12_14")
keyboard_math_12_14_ur5 =  keyboard_cr([["материалы урока", "math_mater_12_14_ur5"], ["домашнее задание", "math_zd_12_14_ur5"]], "back_to_math_12_14")

keyboard_math_13_ur1 =  keyboard_cr([["материалы урока", "math_mater_13_ur1"], ["домашнее задание", "math_zd_13_ur1"]], "back_to_math_13")
keyboard_math_13_ur2 =  keyboard_cr([["материалы урока", "math_mater_13_ur2"], ["домашнее задание", "math_zd_13_ur2"]], "back_to_math_13")
keyboard_math_13_ur3 =  keyboard_cr([["материалы урока", "math_mater_13_ur3"], ["домашнее задание", "math_zd_13_ur3"]], "back_to_math_13")
keyboard_math_13_ur4 =  keyboard_cr([["материалы урока", "math_mater_13_ur4"], ["домашнее задание", "math_zd_13_ur4"]], "back_to_math_13")
keyboard_math_13_ur5 =  keyboard_cr([["материалы урока", "math_mater_13_ur5"], ["домашнее задание", "math_zd_13_ur5"]], "back_to_math_13")
keyboard_math_13_ur6 =  keyboard_cr([["материалы урока", "math_mater_13_ur6"], ["домашнее задание", "math_zd_13_ur6"]], "back_to_math_13")

keyboard_math_15_ur1 =  keyboard_cr([["материалы урока", "math_mater_15_ur1"], ["домашнее задание", "math_zd_15_ur1"]], "back_to_math_15")
keyboard_math_15_ur2 =  keyboard_cr([["материалы урока", "math_mater_15_ur2"], ["домашнее задание", "math_zd_15_ur2"]], "back_to_math_15")
keyboard_math_15_ur3 =  keyboard_cr([["материалы урока", "math_mater_15_ur3"], ["домашнее задание", "math_zd_15_ur3"]], "back_to_math_15")

keyboard_math_16_ur1 =  keyboard_cr([["материалы урока", "math_mater_16_ur1"], ["домашнее задание", "math_zd_16_ur1"]], "back_to_math_16")
keyboard_math_16_ur2 =  keyboard_cr([["материалы урока", "math_mater_16_ur2"], ["домашнее задание", "math_zd_16_ur2"]], "back_to_math_16")
keyboard_math_16_ur3 =  keyboard_cr([["материалы урока", "math_mater_16_ur3"], ["домашнее задание", "math_zd_16_ur3"]], "back_to_math_16")
keyboard_math_16_ur4 =  keyboard_cr([["материалы урока", "math_mater_16_ur4"], ["домашнее задание", "math_zd_16_ur4"]], "back_to_math_16")
keyboard_math_16_ur5 =  keyboard_cr([["материалы урока", "math_mater_16_ur5"], ["домашнее задание", "math_zd_16_ur5"]], "back_to_math_16")
keyboard_math_16_ur6 =  keyboard_cr([["материалы урока", "math_mater_16_ur6"], ["домашнее задание", "math_zd_16_ur6"]], "back_to_math_16")

keyboard_math_17_ur1 =  keyboard_cr([["материалы урока", "math_mater_17_ur1"], ["домашнее задание", "math_zd_17_ur1"]], "back_to_math_17")
keyboard_math_17_ur2 =  keyboard_cr([["материалы урока", "math_mater_17_ur2"], ["домашнее задание", "math_zd_17_ur2"]], "back_to_math_17")
keyboard_math_17_ur3 =  keyboard_cr([["материалы урока", "math_mater_17_ur3"], ["домашнее задание", "math_zd_17_ur3"]], "back_to_math_17")
keyboard_math_17_ur4 =  keyboard_cr([["материалы урока", "math_mater_17_ur4"], ["домашнее задание", "math_zd_17_ur4"]], "back_to_math_17")
keyboard_math_17_ur5 =  keyboard_cr([["материалы урока", "math_mater_17_ur5"], ["домашнее задание", "math_zd_17_ur5"]], "back_to_math_17")
keyboard_math_17_ur6 =  keyboard_cr([["материалы урока", "math_mater_17_ur6"], ["домашнее задание", "math_zd_17_ur6"]], "back_to_math_17")

keyboard_math_18_ur1 =  keyboard_cr([["материалы урока", "math_mater_18_ur1"], ["домашнее задание", "math_zd_18_ur1"]], "back_to_math_18")
keyboard_math_18_ur2 =  keyboard_cr([["материалы урока", "math_mater_18_ur2"], ["домашнее задание", "math_zd_18_ur2"]], "back_to_math_18")
keyboard_math_18_ur3 =  keyboard_cr([["материалы урока", "math_mater_18_ur3"], ["домашнее задание", "math_zd_18_ur3"]], "back_to_math_18")
keyboard_math_18_ur4 =  keyboard_cr([["материалы урока", "math_mater_18_ur4"], ["домашнее задание", "math_zd_18_ur4"]], "back_to_math_18")
keyboard_math_18_ur5 =  keyboard_cr([["материалы урока", "math_mater_18_ur5"], ["домашнее задание", "math_zd_18_ur5"]], "back_to_math_18")
keyboard_math_18_ur6 =  keyboard_cr([["материалы урока", "math_mater_18_ur6"], ["домашнее задание", "math_zd_18_ur6"]], "back_to_math_18")


#соответствие сигналов и кнопок меню которые они открывают
sl = {"russ_menu": ["русский", keyboard_russ_menu], "math_menu": ["матеша", keyboard_math_menu], "back_to_menu": ["главное меню", keyboard_menu], \
      "math_1_9": ["1-9", keyboard_math_1_9], "math_10_18": ["10-18", keyboard_math_10_18], "russ_2_8": ["2-8", keyboard_russ_2_8],\
      "russ_9_15": ["9-15", keyboard_russ_9_15], "russ_16_21": ["16-21", keyboard_russ_16_21],"russ_22_26": ["22-26", keyboard_russ_22_26],\
      "russ_27":["сочинение", keyboard_russ_27],"back_to_math_menu": ["матеша", keyboard_math_menu],\
      "back_to_russ_menu" : ["русский", keyboard_russ_menu], "back_to_russ_2_8": ["задания 2-8", keyboard_russ_2_8], \
      "back_to_russ_9_15": ["задания 9-15", keyboard_russ_9_15], "back_to_russ_16_21": ["задания 16-21", keyboard_russ_16_21], \
      "back_to_russ_22_26": ["задания 1, 22-26", keyboard_russ_22_26], \
      "russ_1" : ["задание 1", keyboard_russ_1], "russ_2" : ["задание 2", keyboard_russ_2], "russ_3" : ["задание 3", keyboard_russ_3], \
      "russ_4" : ["задание 4", keyboard_russ_4], "russ_5" : ["задание 5", keyboard_russ_5], "russ_6" : ["задание 6", keyboard_russ_6], \
      "russ_7" : ["задание 7", keyboard_russ_7], "russ_8" : ["задание 8", keyboard_russ_8], "russ_9" : ["задание 9", keyboard_russ_9], \
      "russ_10" : ["задание 10", keyboard_russ_10], "russ_11" : ["задание 11", keyboard_russ_11], "russ_12" : ["задание 12", keyboard_russ_12], \
      "russ_13" : ["задание 13", keyboard_russ_13], "russ_14" : ["задание 14", keyboard_russ_14], "russ_15" : ["задание 15", keyboard_russ_15], \
      "russ_16" : ["задание 16", keyboard_russ_16], "russ_17" : ["задание 17", keyboard_russ_17], "russ_18" : ["задание 18", keyboard_russ_18], \
      "russ_19" : ["задание 19", keyboard_russ_19], "russ_20" : ["задание 20", keyboard_russ_20], "russ_21" : ["задание 21", keyboard_russ_21], \
      "russ_22" : ["задание 22", keyboard_russ_22], "russ_23" : ["задание 23", keyboard_russ_23], "russ_24" : ["задание 24", keyboard_russ_24], \
      "russ_25" : ["задание 25", keyboard_russ_25], "russ_26" : ["задание 26", keyboard_russ_26], \
      "back_to_math_1_9" : ["задания 1-9", keyboard_math_1_9], "back_to_math_10_18" : ["задания 10-18", keyboard_math_10_18], \
      "math_1": ["задание 1", keyboard_math_1], "math_2": ["задание 2", keyboard_math_2], "math_3": ["задание 3", keyboard_math_3], \
      "math_4": ["задание 4", keyboard_math_4], "math_5": ["задание 5", keyboard_math_5], "math_6": ["задание 6", keyboard_math_6], \
      "math_7": ["задание 7", keyboard_math_7], "math_8": ["задание 8", keyboard_math_8], "math_9": ["задание 9", keyboard_math_9], \
      "math_10": ["задание 10", keyboard_math_10], "math_11": ["задание 11", keyboard_math_11], "math_12_14": ["задания 12 14", keyboard_math_12_14], \
      "math_13": ["задание 13", keyboard_math_13], "math_15": ["задание 15", keyboard_math_15], "math_16": ["задание 16", keyboard_math_16], \
      "math_17": ["задание 17", keyboard_math_17], "math_18": ["задание 18", keyboard_math_18], "back_to_math_12_14": ["задания 12 14", keyboard_math_12_14],\
      "back_to_math_13": ["заданиt 13", keyboard_math_13], "back_to_math_15": ["заданиt 15", keyboard_math_15], \
      "back_to_math_16": ["заданиt 16", keyboard_math_16], "back_to_math_17": ["заданиt 17", keyboard_math_17], \
      "back_to_math_18": ["заданиt 18", keyboard_math_18], "math_12_14_ur1": ["задания 12 14 первый урок", keyboard_math_12_14_ur1], \
      "math_12_14_ur2": ["задания 12 14 второй урок", keyboard_math_12_14_ur2], "math_12_14_ur3": ["задания 12 14 третий урок", keyboard_math_12_14_ur3],
      "math_12_14_ur4": ["задания 12 14 четвертый урок", keyboard_math_12_14_ur4], "math_12_14_ur5": ["задания 12 14 пятый урок", keyboard_math_12_14_ur5],\
      "math_15_ur1" : ["задание 15 первый урок", keyboard_math_15_ur1], "math_15_ur2" : ["задание 15 второй урок", keyboard_math_15_ur2],
      "math_15_ur3" : ["задание 15 третий урок", keyboard_math_15_ur3], "math_17_ur1": ["задание 17 урок 1", keyboard_math_17_ur1], \
      "math_17_ur2": ["задание 17 урок 2", keyboard_math_17_ur2], "math_17_ur3": ["задание 17 урок 3", keyboard_math_17_ur3], \
      "math_17_ur4": ["задание 17 урок 4", keyboard_math_17_ur4], "math_17_ur5": ["задание 17 урок 5", keyboard_math_17_ur5], \
      "math_17_ur6": ["задание 17 урок 6", keyboard_math_17_ur6], "math_18_ur1": ["задание 18 урок 1", keyboard_math_18_ur1], \
      "math_18_ur2": ["задание 18 урок 2", keyboard_math_18_ur2], "math_18_ur3": ["задание 18 урок 3", keyboard_math_18_ur3], \
      "math_18_ur4": ["задание 18 урок 4", keyboard_math_18_ur4], "math_18_ur5": ["задание 18 урок 5", keyboard_math_18_ur5], \
      "math_18_ur6": ["задание 18 урок 6", keyboard_math_18_ur6], "math_16_ur1": ["задание 16 урок 1", keyboard_math_16_ur1], \
      "math_16_ur2": ["задание 16 урок 2", keyboard_math_16_ur2], "math_16_ur3": ["задание 16 урок 3", keyboard_math_16_ur3], \
      "math_16_ur4": ["задание 16 урок 4", keyboard_math_16_ur4], "math_16_ur5": ["задание 16 урок 5", keyboard_math_16_ur5], \
      "math_16_ur6": ["задание 16 урок 6", keyboard_math_16_ur6], "math_13_ur1": ["задание 13 урок 1", keyboard_math_13_ur1], \
      "math_13_ur2": ["задание 13 урок 2", keyboard_math_13_ur2], "math_13_ur3": ["задание 13 урок 3", keyboard_math_13_ur3], \
      "math_13_ur4": ["задание 13 урок 4", keyboard_math_13_ur4], "math_13_ur5": ["задание 13 урок 5", keyboard_math_13_ur5], \
      "math_13_ur6": ["задание 13 урок 6", keyboard_math_13_ur6]}

info_str = "Хей! Вот инфа по курсу:" +"\n"+"\n"+\
"- Наш курс - это комплект по подготовке к профильной математике и русскому. Платишь один раз - готовишься сразу ко всему и в одном месте. Это удобно ☝🏻"+"\n"+"\n"+\
"- Сдали сами - поможем сдать тебе. Наш курс основан на собственном опыте подготовки к экзаменам. Учим тому, что РЕАЛЬНО понадобится на ЕГЭ. Без воды, тысячи страниц бесполезной теории и насилия над учеником. Это эффективно 💯"+"\n"+"\n"+\
"- Гарантия результата. К своим 90+ мы шли самостоятельно, тебя же подкинем на попутке. Мы расскажем то, о чем школьные учителя и не догадываются, потому что сами-то не сдавали ЕГЭ 😦Обсудим не только экзамены, но и поможем с выбором траектории поступления, расскажем, как вести себя на экзамене, и поделимся секретом, как не выгореть при подготовке. Это с душой 😉"+"\n"+"\n"+\
"- Используем авторские материалы, презентации и приложения для отработки навыков. Твой основной инструмент на курсе - этот специально созданный бот. Он будет присылать тебе дз, теорию, напоминания об уроках и дедлайнах. Все необходимое сразу в твоем телефоне. Это практично 🤖"+"\n"+"\n"+\
"- Стоимость месяца занятий на курсе - 8 800р. В пересчете на одно занятие выходит, что трехчасовой урок математики обойдется тебе в 600р, а полуторачасовой урок русского в 500р. В месяц проводится 8 таких занятий по каждому предмету. Таких цен ты не найдешь больше нигде. Это выгодно 😱"+"\n"+"\n"+\
"- Из учеников создается мини-группа, что снижает единовременную нагрузку на учителя без потери качества обучения. По такой схеме работают самые топовые онлайн-школы. Занятия проходят 2 раза в неделю в формате вебинаров с обратной связью. Преподаватель открыт для вопросов и во внеучебное время. Это к-о-м-ф-о-р-т-н-о 😉"+"\n"+"\n"+\
"Если остались вопросы или готов уже сейчас записать на курс, то пиши в этот диалог. Удачи и ждем тебя на занятиях! 👊🏻"



#сопоставление сигнала и фотографии которую нужно отправить
slpht = {"math_mater_1" : ["photo_dz/ammm1.png", "photo_dz/menu.png", "photo_dz/mistake5.png", "photo_dz/nutipa.png",\
                           "photo_dz/paaaaaaaaa.png", "photo_dz/task1.png", "photo_dz/task2.png", "photo_dz/task3.png",\
                           "photo_dz/yaaaaaaa2.png", "photo_dz/ye.png", "photo_dz/yey.png", "photo_dz/yeyy.png"], \
         "russ_zd_1": ["photo_dz/testdz1.png", "photo_dz/testdz2.png"]}
#cоответсвие сигналов и таблиц с ответами по которым нужно будет проверять пользователя
slchk = {"russ_zd_1" : [["ряз_1_1", "именно", "какраз", "вот"], ["ряз_1_2", "если", "когда"]], "math_mater_1": [["м_1_1", "10"], ["м_1_2", "11"], ["м_1_3", "121"]]}
#айди допущенных людей и таблицы ответов по которым нужно будет проверять ответы пользователя
slusr = {"303245887" : [], "355952103" : [], "528233002" : []}
sl_all_user  = set()
list_of_users.seek(0, 0 )
while True:
    a = list_of_users.readline().strip()
    if len(a)<1:
       break
    sl_all_user.add(int(a))
curr_ans.seek(0,0)
while True:
    a = curr_ans.readline().strip()
    if len(a)<1:
       break
    id, ans = a.split()
    slusr[int(id)]=slchk[ans]
#основной цикл считывания событий
#try:
print("yep")

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        #новое сообщение
        request = event.object.message["text"]
        request = request.lower()
        if event.object.message["peer_id"] not in sl_all_user:
            sl_all_user.add(event.object.message["peer_id"])
            list_of_users.write(str(event.object.message["peer_id"])+"\n")
        if request=="старт" or request=="start":
            #отпрвка меню
            SendKeyboard(keyboard_menu)
        #проверка ответов
        elif request.count(" ")==1 and request[0] in "0123456789":
            if int(request.split()[0])<=len(slusr[event.object.message["peer_id"]]):
                numans, ans = request.split()
                if ans in slusr[event.object.message["peer_id"]][int(numans)-1]:
                    SendMessage("yep!")
                    log_ans.write(str(event.object.message["peer_id"])+" "+ str(slusr[event.object.message["peer_id"]][int(numans)-1][0])+" "+ ans+" " + "yep"+"\n")
                else:
                    vk.messages.send(peer_id=event.object.message["peer_id"],
                                     random_id=randint(1, 100), sticker_id=63059)
                    log_ans.write(str(event.object.message["peer_id"])+" "+ str(slusr[event.object.message["peer_id"]][int(numans)-1][0])+" "+ ans+" " + "nope"+"\n")
            else:
                SendMessage("Сорри чел,такого номера нет")
        #незнакомый текст
        elif event.object.message["peer_id"] in [303245887, 355952103] and request[:9:]=="рассылка " and len(request)>9:
            for user in sl_all_user:
                vk.messages.send(peer_id=user, message=request[9::], random_id=randint(1, 100))
        elif event.object.message["peer_id"] in [303245887, 355952103] and request=="стоп":
            SendMessage("Так точно")
            break
        else:
            SendMessage("не могу распознать команду")
            vk.messages.send(peer_id=event.object.message["peer_id"],
                             random_id=randint(1, 100), sticker_id=63063)
    #нажатие кнопки
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.peer_id not in sl_all_user:
            sl_all_user.add(event.object.peer_id)
            list_of_users.write(str(event.object.peer_id)+"\n")
        osn = event.object.payload['type']
        #osn - сигнал
        #открытие ссылки
        if osn == "open_link":
            if str(event.object.peer_id) in slusr:
                r = vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload))
            else:
                SendMessage("вас нет в б/д")
        #переключение в ноавое меню
        elif osn in sl:
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message=sl[osn][0],
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=sl[osn][1].get_keyboard())
        #оптравка фото и изменение окна ответов для пользователя
        elif osn in slpht:
            if str(event.object.peer_id) in slusr:
                SendPhoto(slpht[osn])
                if osn in slchk:
                    slusr[event.object.peer_id] = slchk[osn]
                    curr_ans.write(str(event.object.peer_id)+ " "+osn+"\n")
            else:
                SendMessage("вас нет в б/д")
        elif osn=="info":
            SendMessage(info_str)
        #пустая кнопка
        else:
            SendMessage("тут пока ничего нет")
            vk.messages.send(peer_id=event.object.peer_id,
                                 random_id=randint(1, 100), sticker_id=58645)
#фунционал кнопки прописывается в одном из sl
#кнопка добавляется как массив в массиве
'''
except:
    list_of_users.close()
    log_ans.close()
    curr_ans.close()
    pass'''
list_of_users.close()
log_ans.close()
curr_ans.close()
