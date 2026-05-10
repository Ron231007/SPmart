import time
from hal import hal_lcd as LCD
import Display_menu as menu
import access_database as db
import credentials
import scanbarcode
import Buzzer_Switch as warning
import LEDLight as led




lcd = LCD.lcd()

def add_product(items: list, product: tuple) -> list:
    name, price = product
    for i in range(len(items)):
        if items[i][0] == name:
            items[i] = (name, price, items[i][2] + 1)
            return [items, i]
    items.append((name, price, 1))
    return [items, len(items) - 1]

def buy_product_process() -> list:
    items = []
    just_cleared_cart = False

    while True:

        key = menu.get_specific_inputs("1.Scan Products", "2.View Cart", [1, 2], 3)
        tries = 0
        isLoggedIn = False

        if key == 1:
            just_cleared_cart = False

            menu.show_menu("Point Camera", "At Barcode")
            time.sleep(3)
            id = scanbarcode.scanBarcode()
            product = db.get_product_info(id)

            if product[2]:  # alcoholic product
                menu.show_menu("Alcoholic item", "Detected")
                time.sleep(2)

                menu.show_menu("Please approach", "     staff")
                time.sleep(5)
                
                while not isLoggedIn:
                    if tries > 3:
                        led.control_led(1)
                        warning.reset_buzzer()
                        led.control_led(0)
                        tries =0

                    admin_id, admin_password = credentials.get_valid_login_credentials()
                    isLoggedIn = db.login(admin_id, admin_password, True)

                    if isLoggedIn:
                        product = product[:-1]
                        temp_items = add_product(items, product)
                        items = temp_items[0]
                        menu.show_menu("Name: " + product[0], "Price:" + f"{product[1]: .2f}" + " X " + str(items[temp_items[1]][2]))
                        time.sleep(3)
                    else:
                        menu.show_menu("   Wrong Info", "   Try Again")
                        time.sleep(3)
                        tries += 1
            else:
                product = product[:-1]
                temp_items = add_product(items, product)
                items = temp_items[0]
                menu.show_menu("Name: " + product[0], "Price:" + f"{product[1]: .2f}" + " X " + str(items[temp_items[1]][2]))
                time.sleep(3)

        elif key == 2:
            just_cleared_cart = False
            current_item_index = 0
            while True:
                first_item = -1
                item_index = -1

                if len(items) == 0 and not just_cleared_cart:
                    menu.show_menu("No Items scanned", "Scan items first")
                    time.sleep(3)
                    break

                lcd.lcd_clear()
                line1 = "1. " + items[current_item_index][0]

                if current_item_index + 1 < len(items):
                    line2 = "2. " + items[current_item_index + 1][0]
                    options = [1, 2, 3,'*', '#', 0]
                else:
                    line2 = "<-End of Cart-->"
                    options = [1, 3,'*', '#', 0]

                key = menu.get_specific_inputs(line1, line2, options, 3)

                if key == '*':
                    break
                elif key == 0:
                    return items
                elif key == '#':
                    if current_item_index + 2 < len(items):
                        current_item_index += 2
                    else:
                        current_item_index = 0
                elif key == 1 or key == 2:
                    if key == 1:
                        first_item = 1
                        line1 = "Name: " + items[current_item_index][0]
                        line2 = "Price:" + f"{items[current_item_index][1]: .2f}" + " X " + str(items[current_item_index][2])
                    else:
                        first_item = 2
                        line1 = "Name: " + items[current_item_index + 1][0]
                        line2 = "Price:" + f"{items[current_item_index + 1][1] : .2f}" + " X " + str(items[current_item_index + 1][2])

                    key = menu.get_specific_inputs(line1, line2, ['#', '*'], 3)

                    if key == '#':
                        if first_item == 1:
                            item_index = current_item_index
                        elif first_item == 2:
                            item_index = current_item_index + 1

                        key = menu.get_specific_inputs("Delete " + items[item_index][0] + '?', "", ['*', '#'], 3)

                        if key == "#":
                            item_name = items[item_index][0]
                            items.pop(item_index)
                            menu.show_menu("Deleted " + item_name, "")
                            if current_item_index >= len(items):
                                current_item_index = 0
                            time.sleep(2)
                        else:
                            continue


                else:
                    key = menu.get_specific_inputs("Are you sure u wan", "to clear ur cart?", ['#', '*'], 3)

                    if key == '*':
                        continue

                    else:
                        items = []
                        lcd.lcd_clear()
                        lcd.lcd_display_string("Cart Cleared", 1)
                        time.sleep(2)
                        just_cleared_cart = True
                        key = 2
                        break

