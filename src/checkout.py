import math 
import Display_menu as menu
from hal import hal_lcd as LCD
import credentials
import access_database as db 
import time
import calculatePrice_or_points
import RFID as rfid
import DCmotor
lcd = LCD.lcd

def pay_by_points(ID: int, isAdmin: bool, totalCost: float, items: list)-> int:
    total_points = db.get_points(ID, isAdmin)
    
    if total_points < 100:
        menu.show_menu("Insuffienent", "points")
        time.sleep(3)
        return -1
    

    max_discount = math.floor(total_points/100) * 5 

    after_deduction = totalCost - max_discount

    if after_deduction <0:                              #more points than needed
        after_deduction = 0
        points_used = math.ceil(totalCost /5) * 100

    else:                                               #not enough points
        points_used = math.floor(total_points / 100) * 100
        

    
    key = menu.get_specific_inputs(f"Before: ${totalCost: .2f}", f"After: ${after_deduction: .2f}", \
                                    ['*', '#'],3)

    if key == '#':
        #deduct points

        db.add_or_deduct_points("-", ID , isAdmin, points_used)
        if after_deduction ==0:
            points_earned = calculatePrice_or_points.calculatePoints(totalCost, isAdmin)
            db.add_or_deduct_points("+", ID, isAdmin,points_earned )
            db.buy_product(items)
            return 0
            
        else:                                   #points cannot cover full cost
            have_atm_card = db.got_ATM_card(ID, isAdmin)
            
            if have_atm_card : 
                first_msg = "1. Atm Card"
                second_msg = "2. Paywave"
                options = [1,2]
            else:
                first_msg = "Please pay"
                second_msg= "via Paywave (1)"
                options = [1]


            key = menu.get_specific_inputs(first_msg, second_msg, options,3)

            if have_atm_card:
                while True:
                    if key ==1:                         #pay using atm      
                        card_id, card_pw = credentials.get_atm_credentials()
                        card_id = int(card_id)

                        if db.verify_card_info(ID,card_id,card_pw,isAdmin):
                            db.buy_product(items)
                            db.add_or_deduct_points("+", ID, isAdmin,\
                                                    calculatePrice_or_points.calculatePoints(totalCost, isAdmin))
                            return 0
                        
                        else:
                            menu.show_menu("Wrong Credential", "Try again")
                            time.sleep(3)
                            key =1

            else:

                if pay_by_paywave(ID, isAdmin,points_earned, items) == 0:
                    
                    db.add_or_deduct_points("+", ID, isAdmin,points_earned)
                    db.buy_product(items)
                    return 0
                
                else: 
                    return -1
        
    else: 
        return -1

def pay_by_paywave(ID: int, isAdmin : bool, points: int, items : list)-> int:
    
    menu.show_menu("Please tap your"," card on reader")
    
    ispayment_successful = rfid.read_rfid()

    if ispayment_successful: 
        db.add_or_deduct_points("+", ID, isAdmin, points)
        db.buy_product(items)

        return 0
    else:
        menu.show_menu("No card Detected", "")
        time.sleep(3)
        return -1
    

def buy_products_plus_points(items: list, ID: int, isAdmin: bool, totalCost : float)-> None:
    db.buy_product(items)
    db.add_or_deduct_points("+", ID, isAdmin,\
                                calculatePrice_or_points.calculatePoints(totalCost, isAdmin))
    return


def checkout(items : list, isLoggedIn : bool , isAdmin: bool, ID: int ):
    
    
    totalCost = calculatePrice_or_points.calculateTotalPrice(items)
    points = calculatePrice_or_points.calculatePoints(totalCost, isAdmin)

    while True:

        menu.show_menu(f"Total: ${totalCost: .2f}",f"Points : {points}")
        time.sleep(3)

        if isLoggedIn:

            got_ATM_card = db.got_ATM_card(ID, isAdmin)

            if got_ATM_card:

                first_msg = "1.ATM 2.Paywave"
                second_msg = "3.Points"
                options = [1,2,3]

            else:
                first_msg = "1. Paywave"
                second_msg = "2. Points"
                options = [1,2]

        else:                                     #not logged in
            first_msg = "1.Login 2.Signup"
            second_msg = "3.Pay by Paywave"
            options = [1,2,3]

        key = menu.get_specific_inputs(first_msg,second_msg, options, 3)

        if not isLoggedIn:                          #not logged in
            if key ==1:                             #login
                info = credentials.get_valid_login_credentials()
                isVerified = db.login(info[0], info[1], isAdmin)
                if isVerified:
                    isLoggedIn = True

                else:
                    continue

            elif key ==2:                           #signup
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

            else:                               #paywave
                if pay_by_paywave(ID, isAdmin, points, items) == 0: 
                    buy_products_plus_points(items, ID, isAdmin, totalCost)
                    
                    menu.show_menu("    Printing", "   receipt...")
                    DCmotor.spin_motor(items)
                    menu.show_menu("Thank you for ", "Shopping @ SPmart") 
                    time.sleep(5)
                    break

                else:
                    continue


        else:                                   #logged in
            if key ==1:                         #pay using atm      
                card_id, card_pw = credentials.get_atm_credentials()
                card_id = int(card_id)

                if db.verify_card_info(ID,card_id,card_pw,isAdmin):
                    buy_products_plus_points(items, ID, isAdmin, totalCost)
                    menu.show_menu("    Printing", "   receipt...")
                    DCmotor.spin_motor(items)
                    menu.show_menu("Thank you for ", "Shopping @ SPmart")
                    time.sleep(5)
                    break

                else:
                    menu.show_menu("Invalid ID or Pw", "Try again")
                    time.sleep(1.5)

            elif key ==2:                       #pay using paywave
                if pay_by_paywave(ID, isAdmin, points, items) == 0: 
                    buy_products_plus_points(items, ID, isAdmin, totalCost)
                    menu.show_menu("    Printing", "   receipt...")
                    DCmotor.spin_motor(items)
                    menu.show_menu("Thank you for ", "Shopping @ SPmart") 
                    time.sleep(5)
                    break

                else:
                    continue

            else:                               #Pay using points
                can_pay_by_points = pay_by_points(ID,isAdmin,totalCost, items)
                if can_pay_by_points ==0:
                    buy_products_plus_points(items, ID, isAdmin, totalCost)
                    menu.show_menu("    Printing", "   receipt...")
                    DCmotor.spin_motor(items)
                    menu.show_menu("Thank you for ", "Shopping @ SPmart") 
                    time.sleep(5)
                
                    break

                elif can_pay_by_points == -1:
                    continue

                

                


        

