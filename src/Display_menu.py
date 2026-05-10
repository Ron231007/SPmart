from hal import hal_lcd as LCD
import time
from get_keypad_value import shared_keypad_queue
from typing import Union
lcd = LCD.lcd()

def show_menu(first_message : str, second_message: str):
    lcd.lcd_clear()
    lcd.lcd_display_string(first_message,1)
    lcd.lcd_display_string(second_message,2)


def get_specific_inputs(first_line: str, second_line: str , options: list, reading_time: int) -> Union[int, str]:

    show_menu(first_line, second_line)
    key = shared_keypad_queue.get()
   
    while key not in options:
        show_menu("Invalid option","Options: " + str(options)[1:-1])
        time.sleep(reading_time)
        show_menu(first_line, second_line)
        key = shared_keypad_queue.get()

    return key

