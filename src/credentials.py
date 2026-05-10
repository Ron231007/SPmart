import time

from hal import hal_lcd as LCD

from get_keypad_value import shared_keypad_queue

import access_database as db

import Display_menu as menu

lcd = LCD.lcd()





def get_valid_login_credentials()-> list:

    lcd.lcd_clear()

    menu.show_menu("     Please", "     Login")

    time.sleep(2)

    

    lcd.lcd_clear()

    lcd.lcd_display_string("ID: ", 1)

    user_id = ""

    password = ""



    while True:

        key = shared_keypad_queue.get()



        if key == "#" and len(user_id) <= 8 and len(user_id) != 0:

            break



        elif key == "*" and len(user_id) > 0:

            user_id = user_id[:-1]

        elif key not in ("*", "#") and len(user_id) < 8:

            user_id += str(key)



        lcd.lcd_display_string("ID: " + user_id + " ", 1)



    lcd.lcd_display_string("Pw: ", 2)



    while True:

        key = shared_keypad_queue.get()



        if key == "#":

            if len(password) == 8:

                break

            else:

                lcd.lcd_display_string("Pw: Invalid", 2)

                time.sleep(3)

                lcd.lcd_display_string("Pw: " + " " * 7, 2)

                password = ""



        elif key == "*" and len(password) > 0:

            password = password[:-1]

        elif key not in ("*", "#") and len(password) < 8:

            password += str(key)



        lcd.lcd_display_string("Pw: " + "*" * len(password) + " ", 2)



    return [int(user_id), password]



 

def get_valid_signUp_credentials(isAdmin: bool) -> list :

    password = ""

    id = db.getValidID(isAdmin)

    lcd.lcd_clear()



    lcd.lcd_display_string("ID: "+ str(id), 1)

    lcd.lcd_display_string("Pw: ",2)



    while True:

        key = shared_keypad_queue.get()



        if key == "#":

            if len(password) == 8 and len(set(password)) >3:

                break



            else:

                lcd.lcd_display_string("Pw: Invalid Pw!",2)

                time.sleep(2)

                lcd.lcd_display_string("Pw:" + " " *13,2)

                password = ""



        elif key == "*" and len(password) >0:

            password = password[:-1]

            lcd.lcd_display_string("Pw: " + "*" * len(password) + " ",2)



        elif key not in ["*", "#"] and len(password) < 8:

            password += str(key)

            lcd.lcd_display_string("Pw: " + "*" * len(password) , 2)

    

    card_info = link_ATM_card()

    return [password, card_info]





def get_atm_credentials() -> list:

    lcd.lcd_clear()

    card_password = ""

    card_id = ""

    menu.show_menu("ID: ", "")



    while True:

        key = shared_keypad_queue.get()



        if key == "#":

            if len(card_id) == 10:

                break

            else:

                menu.show_menu("Invalid Card ID", "Try Again")

                card_id = ""

                time.sleep(3)

                lcd.lcd_clear()

                lcd.lcd_display_string("ID: ",1)



        elif key == "*" and len(card_id) > 0:

            card_id = card_id[:-1]

            lcd.lcd_display_string("ID: " + card_id + " ",1)

        elif key not in ("#", "*") and len(card_id) <10:

            card_id +=str(key)

            lcd.lcd_display_string("ID: " + card_id,1)



    lcd.lcd_display_string("Pw: ",2)

    while True:

        key = shared_keypad_queue.get()



        if key == "#":

            if len(card_password) <= 10:

                break

            else:

                menu.show_menu("Invalid Card Pw", "Try Again")

                card_password = ""

                time.sleep(3)

                lcd.lcd_clear()

                lcd.lcd_display_string("Pw: ",2)



        elif key == "*" and len(card_password) > 0:

            card_password = card_password[:-1]

            lcd.lcd_display_string("Pw: " + "*" * len(card_password) + " ",2)

        elif key not in ("#", "*") and len(card_password) <10:

            card_password +=str(key)

            lcd.lcd_display_string("Pw: " + "*" * len(card_password),2)



    return [card_id, card_password]



            



def link_ATM_card() -> list:

    lcd.lcd_clear()

    card_id = ""

    card_password = ""



    return_values = False

    while not return_values:



        menu.show_menu(" Link ATM Card?", "  1.Yes   2.No")

        key = shared_keypad_queue.get()



        while key not in [1, 2]:

            menu.show_menu("Invalid option", "Select 1 or 2")

            time.sleep(2)

            menu.show_menu(" Link ATM Card?", "  1.Yes   2.No")

            key = shared_keypad_queue.get()



        if key == 1:

            card_id, card_password = get_atm_credentials()

            return_values = True   # ? exit after linking



        elif key == 2:

            menu.show_menu("Are You Sure?", "  1.Yes   2.No")

            key = shared_keypad_queue.get()

            while key not in [1, 2]:

                menu.show_menu("Invalid option", "Select 1 or 2")

                time.sleep(2)

                menu.show_menu("Are You Sure?", "  1.Yes   2.No")

                key = shared_keypad_queue.get()



            if key == 1:

                return []  # exit immediately if confirmed "No"

            else:

                continue



    return [card_id, card_password]

