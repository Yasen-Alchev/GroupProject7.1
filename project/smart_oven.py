from fhict_cb_01.CustomPymata4 import CustomPymata4
import time
import requests

ORDER_PLACED = 1 # this is set on the server dynamically (do not provide status)
PIZZA_IN_OVEN = 2 # baking - preparing step
PIZZA_IS_DONE = 3 # pizza baked - quality check step
OVEN_IS_OFF = 4 # the pizza has finished the quality check step and is ready

board = CustomPymata4(com_port = "COM3")
board.set_pin_mode_digital_output(4)
board.set_pin_mode_digital_output(5)
board.set_pin_mode_digital_output(7)
board.set_pin_mode_digital_input_pullup(8)
board.set_pin_mode_digital_input_pullup(9)
board.digital_pin_write(7, 1)

url = input("Flask IP address: ")
order_number = input("Enter order number: ")
cooking_time = int(input("What is the cooking time in minutes? "))

def start_smart_oven(cooking_time):
    time_left = cooking_time
    board.digital_pin_write(4, 1)
    board.digital_pin_write(7, 0)

    data = { "status": PIZZA_IN_OVEN, "order_number": order_number }
    requests.post(url, json = data)

    for _ in range(cooking_time):
        time.sleep(1)
        time_left -= 1
        print(f"Time left to cook: {time_left}")

    data["status"] = PIZZA_IS_DONE
    requests.post(url, json = data)

    board.digital_pin_write(4, 0)

    for _ in range(5):
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
        data = { "status": OVEN_IS_OFF, "order_number" : order_number}
        requests.post(url, json = data)
        order_number = input("Enter order number: ")
        cooking_time = int(input("What is the cooking time in minutes? "))