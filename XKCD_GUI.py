"""
Written by: Shreyas Daniel - github.com/shreydan
Written on: 26 April 2017
Description: Download latest XKCD Comic with this program.
NOTE:
	if this script is launched from the cloned repo, a new folder is created.
	Please move the file to another directory to avoid messing with the folder structure.

PySimpleGUI interface added by:Tom Imlay - github.com/imlayt
Written on: 03/29/2020
Description: downloads the latest XKCD comic then reads in the file to display it in a window
"""

import sys
import os
import PySimpleGUI as sg
import urllib.request
import requests
from lxml import html


comic_name = ''
comic_location = ''

lightblue = '#b9def4'
mediumblue = '#d2d2df'
mediumblue2 = '#534aea'
darkaccent = '#322998'
lightaccent = '#b1b1b1'
lighteraccent = '#fbe9b3'


def getcomic():
    global comic_location
    global comic_name

    # opens xkcd.com
    try:
        page = requests.get("https://www.xkcd.com")
    except requests.exceptions.RequestException as e:
        print(e)
        exit()

    # parses xkcd.com page
    tree = html.fromstring(page.content)

    # finds image src url
    image_src = tree.xpath(".//*[@id='comic']/img/@src")[0]
    image_src = "https:" + str(image_src)

    # gets comic name from the image src url
    comic_name = image_src.split('/')[-1]

    # save location of comic
    comic_location = os.getcwd() + '\\comics\\'
    print('comic_location =>', comic_location)

    # checks if save location exists else creates
    if not os.path.exists(comic_location):
        os.makedirs(comic_location)

    # creates final comic location including name of the comic
    comic_location = comic_location + comic_name

    # downloads the comic
    urllib.request.urlretrieve(image_src, comic_location)



def write_to_message_area(window, message):
    window.FindElement('_MESSAGEAREA_').Update(message)
    window.Refresh()

getcomic()


# print('getcomic=>', comic_location)
# comic_location = 'C:/Users/imlay/PycharmProjects/Examples/comics/6_foot_zone.png'


# Define the mainscreen layout using the above layouts
mainscreenlayout = [[sg.Image(filename=comic_location, key='XKCD')],
                    [sg.Text('Message Area', size=(50, 1), key='_MESSAGEAREA_')],
                    [sg.Exit()]]


# ########################################
# initialize main screen window
sg.SetOptions(element_padding=(2, 2))
window = sg.Window('XKCD Cartoon', background_color=darkaccent,
        default_element_size=(20, 1)).Layout(mainscreenlayout)
window.Finalize()
window.Refresh()


write_to_message_area(window,comic_name)

# event loop
while True:  # Event Loop
    event, values = window.Read()
    if event is None or event == "Exit":
        sys.exit(1)