from bs4 import BeautifulSoup
import os
from os import path
import requests
from pathlib import Path

url = "https://developer.android.com/reference/android/app/package-summary"
r = requests.get(url)

#html_code = r.text
soup = BeautifulSoup(r.content, 'html.parser')
results = soup.findAll('li', {"class": "devsite-nav-item devsite-nav-expandable"})

for result in results:
    subResult = result.findAll('span', {"class": "devsite-nav-text"})
    if subResult[0].text == "android.app":
        #print(result)
        listResults = result.findAll('li', {"class": "devsite-nav-item devsite-nav-expandable"})
        for listResult in listResults:
            #print(listResult)
            if listResult.span.text == "Interfaces":
                interface = listResult.ul
                interface_list = interface.findAll('li', {"class": "devsite-nav-item"})
            elif listResult.span.text == "Classes":
                classi = listResult.ul
                class_list = classi.findAll('li', {"class": "devsite-nav-item"})
            elif listResult.span.text == "Exceptions":
                exception = listResult.ul
                exception_list = exception.findAll('li', {"class": "devsite-nav-item"})

app_URL = "https://developer.android.com/reference/android/app/"
try:
    os.mkdir("./outFiles")
except OSError as error:
    print(error)




def notes_crawler(obj_url, name):
    f = None
    re = requests.get(obj_url)
    soupa = BeautifulSoup(re.content, 'html.parser')
    body = soupa.find('div', {'class': "devsite-article-body"})
    #objects = soupa.findAll('div', {'id': "jd-content"})
    objs = body.div.findAll('div', {'id': None})
    #objsa = objs.findAll('div')
    #print(objsa) # ??????
    for obj in objs:
        caution = obj.findAll('p', {"class": "caution"})
        notes = obj.findAll('p', {"class": "note"})
        my_file = Path("./outFiles/" + str(name.text) + ".txt")
        #print(notes)
        if caution != []:
            if(not my_file.is_file()):
                filename = "./outFiles/" + str(name.text) + ".txt"
                f = open(filename, "w")
            #print(obj)
            #print(obj.h3.text)
            #print("-------------------")
            #print(notes)
            f.write(str(obj.h3.text) + ":" + str(caution[0].text) + "\n")
        if notes != []:
            if (not my_file.is_file()):
                filename = "./outFiles/" + str(name.text) + ".txt"
                f = open(filename, "w")
            for note in notes:
                f.write(str(obj.h3.text) + ":" + str(note.text) + "\n")
    if f != None:
        f.close()

# def except_notes_crawler(obj_url, name):
#     f = None
#     re = requests.get(obj_url)
#     soupe = BeautifulSoup(re.content, 'html.parser')
#     #print(soupe)
#     body = soupe.find('div', {'id': "jd-content"})
#     #print(body)
#     #objects = soupa.findAll('div', {'id': "jd-content"})
#     objs = body.findAll('div')
#     #objsa = objs.findAll('div')
#     #print(objsa) # ??????
#     for obj in objs:
#         caution = obj.findAll('p', {"class": "caution"})
#         notes = obj.findAll('p', {"class": "note"})
#         my_file = Path("./outFiles/" + str(name.text) + ".txt")
#         #print(notes)
#         if caution != []:
#             if(not my_file.is_file()):
#                 filename = "./outFiles/" + str(name.text) + ".txt"
#                 f = open(filename, "w")
#             #print(obj)
#             #print(obj.h3.text)
#             #print("-------------------")
#             #print(notes)
#             f.write(str(obj.h3.text) + ":" + str(caution[0].text) + "\n")
#         if notes != []:
#             if (not my_file.is_file()):
#                 filename = "./outFiles/" + str(name.text) + ".txt"
#                 f = open(filename, "w")
#             f.write(str(obj.h3.text) + ":" + str(notes[0].text) + "\n")
#     if f != None:
#         f.close()

for class_obj in class_list:
    obj_URL = app_URL + class_obj.span.text
    notes_crawler(obj_URL, class_obj)

for exception_obj in exception_list:
     obj_URL = app_URL + exception_obj.span.text
     notes_crawler(obj_URL, exception_obj)

for interface_obj in interface_list:
    obj_URL = app_URL + interface_obj.span.text
    notes_crawler(obj_URL, interface_obj)