# Отображаем на рабочем столе рандомную цитату из текстов Светланы Лавреньтевой, используя полученный мамкиным какирством URL из исходного кода веб-страницы сайта.
# Иногда обрезается текст, но я устал возиться.

URL = "https://lavrentyeva.space/wp-content/themes/bateaux/text-random-script.php"
INTERVAL = 15
CONKY_CONFIG_PATH = "/home/%YOUR_USERNAME%/.config/conky/conky.conf"

from os import popen
from urllib import request as r
import threading, time
from bs4 import BeautifulSoup

def skip_shit(text):
    text = text.decode("utf-8")
    text = BeautifulSoup(text, features="html.parser").get_text()
    return text.rstrip()

def worker():
    config = open(CONKY_CONFIG_PATH, "r").read()
    content = r.urlopen(URL).read()
    content = skip_shit(content)
    popen("killall conky")
    time.sleep(1)
    with open(CONKY_CONFIG_PATH, "w") as new_config:
        new_config.write("""conky.config = {
alignment = 'middle_left',
use_xft = true,
font = 'Ubuntu:size=10',
minimum_height = 5,
update_interval = 10,
color1 = '#990000',
color2 = '#009900',
color3 = '#000099',
double_buffer = true,
background = false,
border_width = 1,
own_window_transparent = false,
own_window_argb_visual = true,
}
conky.text = [[""" + content + "]]")
    popen("conky")

while True:
    thread = threading.Thread(target=worker, args=())
    thread.start()
    time.sleep(INTERVAL)
