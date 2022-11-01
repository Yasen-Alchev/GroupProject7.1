from fhict_cb_01.CustomPymata4 import CustomPymata4
import time
import requests

board = CustomPymata4(com_port = "COM3")
board.set_pin_mode_digital_output(4)
board.set_pin_mode_digital_output(5)
board.set_pin_mode_digital_output(7)
board.set_pin_mode_digital_input_pullup(8)
board.set_pin_mode_digital_input_pullup(9)
board.digital_pin_write(7, 1)

url = input("Flask IP address: ")
cooking_time = int(input("What is the cooking time in minutes? "))
def start_smart_oven(cooking_time):
    time_left = cooking_time
    board.digital_pin_write(4, 1)
    board.digital_pin_write(7, 0)

    for _ in range(0, cooking_time):
        time_left -= 1
        time.sleep(1)
        data = { "status": "Pizza in oven", "time_left": time_left }
        post_data = requests.post(url, json = data)

    data = { "status": "Pizza is done", "time_left": time_left}
    post_data = requests.post(url, json = data)
    board.digital_pin_write(4, 0)

    for _ in range(0, 5):
        board.digital_pin_write(5, 1)
        time.sleep(0.5)
        board.digital_pin_write(5, 0)
        time.sleep(0.5)
        
    board.digital_pin_write(7, 1)

while True:
    level, time_stamp = board.digital_read(8)
    if level == 0:
        start_smart_oven(cooking_time)
    level, time_stamp = board.digital_read(9)
    if level == 0:
        data = { "status": "Oven turned off", "time_left": 0}
        post_data = requests.post(url, json = data)
        cooking_time = int(input("What is the cooking time in minutes? "))