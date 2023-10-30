from pprint import pprint
import re
import csv

# lastname,firstname,surname,organization,position,phone,email

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


regexp_phone = r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*'
changed_phone = r'+7(\2)-\3-\4-\5 \6\7'
list_fio = []

# ФИО
for idx, contact in enumerate(contacts_list):
    fio = " ".join(contact[:3])
    list_fio.append(fio.split(" "))
    for index, fio in enumerate(list_fio):
        if len(fio) > 3:
            list_fio[index] = fio[:3]
        contact[0] = fio[0]
        contact[1] = fio[1]
        contact[2] = fio[2]


#Телефон
for index, contact in enumerate(contacts_list):
    if contact[5]:
        phone = re.sub(regexp_phone, changed_phone, contact[5])
        contacts_list[index][5] = phone

#Дубли
contacts_dict = {}
for row in contacts_list:
    row_key = (row[0] + row[1]).upper()
    dict_element = contacts_dict.get(row_key)
    if dict_element is None:
        dict_element = row
    else:
        for index, text in enumerate(dict_element):
            if len(text) == 0:
                dict_element[index] = row[index]
    contacts_dict[row_key] = dict_element

contacts_list.clear()
for key, item in contacts_dict.items():
    contacts_list.append(item)


# Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding='cp1251') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
