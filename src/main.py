#For testing, user_id 1 has the password(both acc and card password)  "12345678"
#Admin id = 2 has the password "96694742" and card password = "12345678"

from threading import Thread
import time

from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_servo as servo
from hal import hal_usonic as usonic
import Display_menu as menu
import get_keypad_value
from get_keypad_value import shared_keypad_queue, key_pressed
import credentials
import access_database as db
import buy_products_process 
import checkout
import Ultrasound as usound

lcd = LCD.lcd()

def main():
    get_keypad_value.clear_queue()
    while True:
        started_scanning_products = False
        isLoggedIn = False
        items = []
        usonic.init()
        lcd.lcd_clear()
        led.init

        keypad.init(key_pressed)
        Thread(target=keypad.get_key).start()

        start= usound.got_movement()

        while not start:
            lcd.backlight(0)
            start = usound.got_movement()

        lcd.backlight(1)
        while True:
            key = menu.get_specific_inputs("1. Admin","2. Customer", [1,2],3)

            
            if key == 1:                      #admin
                key = menu.get_specific_inputs("1. Login", "*. Go back", [1, '*'], 3)
                if key != '*':
                    isAdmin = True
                    break           
                
                else:
                    continue     
                

            elif key == 2:                        #customer
                key = menu.get_specific_inputs("1.Login 2.SignUp","3.Guest Login",[1,2,3, '*'],3)
                isAdmin = False
                break

        
        while not started_scanning_products:
            if key == 1:
                info = credentials.get_valid_login_credentials()
                isVerified = db.login(info[0], info[1], isAdmin)

                if isVerified:
                    menu.show_menu(" Login Success!","Welcome 2 SPmart")
                    time.sleep(1.5)
                    isLoggedIn = True

                    started_scanning_products = True
                    items = buy_products_process.buy_product_process()
                    checkout.checkout(items , isLoggedIn, isAdmin, info[0])


                else:
                    menu.show_menu("Wrong ID or Pw","Please Try again")
                    time.sleep(3)
                
            elif key == 2:
                pw = credentials.get_valid_signUp_credentials(isAdmin)
                
                if pw[1] == []:                         #no card info
                    db.signup(pw[0],-1,"", isAdmin)
                    lcd.lcd_clear()
                    lcd.lcd_display_string("SignUp Success!",1)
                    time.sleep(1.5)
                    
                else:
                    db.signup(pw[0], pw[1][0], pw[1][1],isAdmin)
                    lcd.lcd_clear()
                    lcd.lcd_display_string("SignUp Success!",1)
                    time.sleep(1.5)


                key =1

            elif key == 3:  
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome 2 SPmart",1)
                time.sleep(1.5)
                started_scanning_products = True
                items = buy_products_process.buy_product_process()
                checkout.checkout(items, isLoggedIn, isAdmin, -1)






if __name__ == "__main__":
    main()


