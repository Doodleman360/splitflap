import serial
import serial.tools.list_ports
import json
from time import sleep, time

from random_word import RandomWords

r = RandomWords()

flaps = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', '\'']


def find_USB_device():
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    usb_port_list = [p[0] for p in myports]

    return usb_port_list


ser = serial.Serial(find_USB_device()[0], 230400, timeout=.1)


def readData():
    answer = ""
    while ser.inWaiting() > 0:  # self.serial.readable() and
        answer += "\n" + str(ser.readline()).replace("\\r", "").replace("\\n", "").replace("'", "").replace("b", "")
    try:
        answer = json.loads(answer)
    except json.decoder.JSONDecodeError:
        answer = {}
    return answer


def move(word):
    if len(word) > 6:
        print("word to big")
        return -1
    ser.write(str.encode(f'={word}\n'))

    while True:
        data = readData()
        if 'type' in data:
            print(data['type'])
            if data['type'] == 'status':
                sleep(1)
                return


def calibrate(current):
    offset = ''
    for letter in current:
        if letter == ' ':
            offset += ' '
        else:
            offset += flaps[len(flaps) - flaps.index(letter)]
    ser.write(b'@')
    move(offset)
    ser.write(b'@')


def dif(a, b):
    while len(a) < 6:
        a += ' '
    while len(b) < 6:
        b += ' '
    dif = [i for i in range(len(a)) if a[i] != b[i]]
    s = ''
    for i in range(len(a)):
        if i in dif:
            s += b[i]
        else:
            s += '$'
    return s


print(ser.name)

# calibrate('exoort')
# move("hi   ")
move("      ")
old = '      '
while True:
    new = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1000, minLength=2, maxLength=6).lower()
    print(f"**{new}**")
    move(dif(old, new))
    old = new
    sleep(600)
