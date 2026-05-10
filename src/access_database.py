import mysql.connector
import password as pw
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=3306,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

cursor = db.cursor()

def getValidID(isAdmin : bool) -> int:
    
    if isAdmin:
        cursor.execute("SELECT ID FROM Admin ORDER BY ID DESC LIMIT 1")

    else:
        cursor.execute("SELECT user_id FROM user_info ORDER BY user_id DESC LIMIT 1")

    result = cursor.fetchone()
    return result[0] + 1 if result else 1
    


def signup(acc_password : str, card_id: str, card_password: str, isAdmin: bool):
    
    account_password = pw.encrypt(acc_password)
    
    if not isAdmin:

        if card_id == -1 and card_password == "":

            query = "INSERT INTO user_info (passwd) VALUES (%s)"
            value = [account_password]

        else:
            card_pw = pw.encrypt(card_password)

            query = "INSERT INTO user_info(passwd, card_id, card_password) VALUES (%s, %s, %s)"
            value = [account_password, card_id, card_pw]

    else:
        if card_id == -1 and card_password == "":

            query = "INSERT INTO Admin (Pw) VALUES (%s)"
            value = [account_password]

        else:
            card_pw = pw.encrypt(card_password)

            query = "INSERT INTO Admin(Pw, card_id, card_password) VALUES (%s, %s, %s)"
            value = [account_password, card_id, card_pw]


    cursor.execute(query, value)
    db.commit()




def login(id: int, password: str, isAdmin: bool) -> bool:
    # Step 1: Get hashed password from database by user_id

    if isAdmin:
        query = "SELECT Pw FROM Admin WHERE ID=%s"

    else:
        query = "SELECT passwd FROM user_info WHERE user_id=%s"
    
    cursor.execute(query, [id])
    result = cursor.fetchone()

    if result is None:
        return False

    stored_hash = result[0]  # This is the bcrypt hash stored during signup
    
    isVerified = pw.verify(password, stored_hash)

    return isVerified


def get_product_info(id : int) -> Optional[tuple]:                                      #Returns name, cost and if the product is alcoholic in the order
    query = "SELECT name, price, isAlcoholic from product WHERE ID = %s " 

    value = [id]


    cursor.execute(query, value)

    info = cursor.fetchone()

    return info

#[('Milk', 6.7, 2), ('Salmon', 8.5, 1)]

def buy_product(items: list) -> None:
    
    for item in items:
    
        name, quantity = item[0], item[2]

        query = "UPDATE product SET Quantity = Quantity - %s WHERE name = %s"

        value = [quantity, name]

        cursor.execute(query,value)

        db.commit()

        

def get_points(ID: int, isAdmin : bool) -> int:
    if isAdmin:
        query = "SELECT Points FROM Admin WHERE ID =%s"

    else:
        query = "SELECT points FROM user_info WHERE user_id =%s"

    value = [ID]

    cursor.execute(query, value)

    points = cursor.fetchone()[0]

    return points
    

def got_ATM_card(ID: int, isAdmin: bool) -> bool:
    if isAdmin:
        query = "SELECT card_id FROM Admin WHERE ID=%s"
    else:
        query = "SELECT card_id FROM user_info WHERE user_id=%s"

    cursor.execute(query, [ID])
    
    result = cursor.fetchone()[0]

    return False if result == None else True


def verify_card_info(id : int ,card_id : int, card_pw : str, isAdmin : bool):
    
    
    if isAdmin:
        query = "SELECT card_id, card_password FROM Admin WHERE ID=%s"
    else:
        query = "SELECT card_id, card_password FROM user_info WHERE user_id=%s"
    
    cursor.execute(query, [id])
    result = cursor.fetchall()[0]

    if result is None:
        return False

    stored_hash = result[1]  # This is the bcrypt hash stored during signup
    
    pw_verification = pw.verify(card_pw, stored_hash)

    return True if int(result[0]) == card_id and pw_verification else False


def add_or_deduct_points(operator: str, ID: int, isAdmin : bool, points : int) -> None:
    if isAdmin:
        query = f"UPDATE Admin SET Points = Points {operator} %s WHERE ID = %s"
    else:
        query = f"UPDATE user_info SET Points = points {operator} %s WHERE user_id = %s" 

    cursor.execute(query, [points, ID])
    db.commit()


    
