# 🛒 Spmart Project

> ⚠️**Keypad Input Timing:**  
Please avoid pressing multiple keys rapidly in succession. The keypad processes input in a queue, and excessive rapid key presses may overflow the input buffer, leading to incorrect or unexpected behavior.
---
# Table of Contents

1. [✅ Features Implemented](**#features-implemented**)  
2. [📦 Build locally](#build-locally)
3. [📦 Pull image from Docker hub](#pulling-image-from-dockerhub)
4. [🧑‍💻 User Guide](#-user-guide)  
   - [1.0 Role Selection](#10-role-selection)  
   - [1.1 Admin Menu](#11-admin-menu)  
     - [1.1.1 Admin Login](#111-admin-login)  
   - [1.2 Customer Menu](#12-customer-menu)  
     - [1.2.1 Guest Login (Account-linked)](#121-guest-login-account-linked)  
     - [1.2.2 Guest Signup](#122-guest-signup)  
     - [1.2.3 Anonymous Guest Login (no account)](#123-anonymous-guest-login)  
   - [2.0 Main Menu](#20-main-menu)  
   - [2.1 Scan Products](#21-scan-products)  
   - [2.2 Viewing Cart](#22-viewing-cart)  
   - [3 Checkout](#3-checkout)  
5. [Non-functioning Requirements](#non-functioning-requirements)
6. [Demo Video](#demo-video)
7. [ℹ️ Additional Notes](#ℹ️-additional-notes)  
8. [Future Developments](#future-developments)
9. [Contributions](#contributions)
10. [Credits](#proudly-presented-to-you-by)
  

---
## ✅ Features Implemented

- Admin Login
- Admin Signup
- Guest Login (linked to account)
- Anonymous Guest Login (no account)
- Product Scanning
- Cart Viewing
- Item Removal from Cart
- Clear Whole Cart
- Alcohol Detection and Staff Verification Prompt
- Checkout Proceedure
- Printing of receipt
- Idle Mode to save electricity
- Website

---

## 📦 Download Instructions

## Build locally:

### 1. Extract the Project

Unzip the release archive (`.zip` or `.tar.gz`) into your preferred working directory.

### 2. Navigate into the `src/` Directory

```bash
cd DCPE_2A_04_Group2-1.0.0/src
```

### 3. Build the Docker Image

```bash
docker build -t SpMart .
```

> ⚠️ This may take some time. Sit back, relax, and let the magic happen.

### 4. Run the Docker Image

```bash
docker run  -p 5000:5000 --privileged --device=/dev/video* -v $(pwd)/images:/app/images -v /run/udev:/run/udev:ro SpMart
```

> ⚠️ `--privileged` and `/dev/video*` access is required for hardware components (e.g., keypad and camera). Ensure you're running this on a Raspberry Pi with the camera connected.

---
### 5. Access the Website

In another terminal, run the following:  
```bash
ifconfig
```


<img width="696" height="180" alt="Screenshot 2025-08-12 220241" src="https://github.com/user-attachments/assets/3a56c428-210e-410e-af4e-c79d972e50b7" />

Simply copy and paste that ip address with port 5000 into your web browser to access the website. In this case, you would key into the web browser: 

```bash
http://172.23.56.190:5000/
```

## Pulling Image from dockerhub

Pull the image from dockerhub with: 
```bash
docker image pull beyondcooked/app:final
```
Similar to building the image locally, you may run the image in a container with:
```bash
docker run -p 5000:5000 --privileged --device=/dev/video* -v $(pwd)/images:/app/images -v /run/udev:/run/udev:ro beyondcooked/app:final
```

And you may access the website with 
```bash
ifconfig
```


<img width="696" height="180" alt="Screenshot 2025-08-12 220241" src="https://github.com/user-attachments/assets/3a56c428-210e-410e-af4e-c79d972e50b7" />

Simply copy and paste that ip address with port 5000 into your web browser to access the website. In this case, you would key into the web browser: 

```bash
http://172.23.56.190:5000/
```

---



## 🧑‍💻 User Guide

 🔑 **Keypad Controls:**  
- `*` → Delete / Go Back  
- `#` → Confirm / Enter  

---

### 1.0 Role Selection

After launching the program, select a role using the keypad:

- `1` → Admin  
- `2` → Customer

---

## 1.1 Admin Menu

- `1` → Login  
- `*` → [Go back to role selection](#10-role-selection)

### 1.1.1 Admin Login

To log in with your ID and password, follow these steps:

1. Enter your ID using the keypad.  
2. Press `*` to delete the last character entered.  
3. Press `#` to proceed to password input.  
4. Your password **must be exactly 8 digits long** and contain **at least 4 unique digits**.
  
---

### 1.2 Customer Menu

- `1` → Guest Login (Account-linked)  
- `2` → Guest Signup  
- `3` → Anonymous Guest Login

#### 1.2.1 Guest Login (Account-linked)

>  [1.1.1 Admin Login](#111-admin-login)


#### 1.2.2 Guest Signup

 1. Your new **User ID will be displayed** — take note of it, as it's required to log in.  
 2. Follow the same rules for password creation as in section 1.1.1 (steps 2–4).  
 3. You will be prompted to link your ATM card. You may skip this, but you will **not be able to use ATM checkout** in the future.

> 🔐 **Tip:** Keep your User ID and password secure and do not share them with others.

#### 1.2.3 Anonymous Guest Login

You may begin scanning products immediately. However, note:

- You will **not earn points** after checkout.  
- **Only Paywave** is accepted for payment.

---

### 2.0 Main Menu

You will be prompted to choose:

- `1` → Scan Products  
- `2` → View Cart

---


### 2.1 Scan Products
Point the camera towards the barcode to scan the product.
> 🍺🔑Do note that if the item is alcoholic, your would need to approach a staff and ask them to key in their staff credentials to ensure that you are of age to buy that alcoholic product.

> 🟢Scanning of product is usually quite fast and when activated, the green light near the lense of the camera will light up. 


---
### 2.2 Viewing Cart

- Press `#` to scroll through products in your cart (if more than 2 items).  
- Select the product (`1` or `2`) to view its price and quantity.
- Select the respective number to view details of the product
     - You may press `#` to initiate the deletion of the product
     - Press `#` again to delete the item or press `*` to cancel the deletion (keep the item)
     - There is also an option `3` (not stated on the lcd)
       - Option 3 is to clear your cart
         - Clearing the cart would delete all items in your cart
         - Similarly, press `#` to confirm and `*` to cancel the proceedure 
- Press `*` to go back to viewing your cart, and `*` again to return to product scanning.  
- Press `0` to proceed to checkout.

> ⚠️ **Note:** Proceeding to checkout is **irreversible**.

---

### 3 Checkout
The lcd will first show your total cost as well as the points you will earn after making that purchase and **not** the points that you have. 
The options that shows up on the screen for you to choose will depend on whether you are logged in or not and did you link your atm card when signing up

Logged In and linked atm card:
- `1`  --> Pay by ATM card
- `2` --> Pay by Paywave
- `3` --> Pay by Points accumulated

Logged in and didn't link atm card:
- `1` --> Pay by Paywave
- `2` --> Pay by Points accumulated

Not Logged In:
- `1` --> Login
- `2` --> Signup
- `3` --> Pay by Paywave
> You won’t earn points if you’re not logged in—sign up or log in to start racking up rewards! 💎

 #### Points to note
 - For this project, we do not interact with any real payment methods and all are a simulation.
 - 🛍️💎You earn 30 points for every $10 spent and can redeem a $5 discount for every 100 points. So go ahead—toss in a little extra and watch those points stack up!
 - For Paywave transactions, you have 10 seconds to scan your RFID. If you miss the time limit, the transaction will be cancelled and you’ll be prompted to select your checkout option again.
 - The login and signup features are the same as the ones that were promted at the start of the progam. All keys remain the same (`#` for enter key and `*` for deletion key) 

---

## Non-functioning Requirements
- 🔁➡️👤After every purchase or reboot, system will automatically navigate to the idle page until a user activates the ultrasound sensor.
- 🔒Passwords must be stored in a safe way and **absolutely not** in plain text
- 👾👾To prevent brute force attacks, lock account after 5 attempts. After another 5 attempts, lock for double the duration and continue afterwards for every 5 attempts. (2^n) is duration of account lock where n is the number of times the acccount is locked.
- Passwords must be only 8 digits (limited by hardware) with at least 4 different digits
- Card ID must be 10 digits long
- Card password cannot be longer than 10 digits long
- 💡⚡To save electricity, the device starts with a dimmed LCD backlight during idle periods. 


---

## Demo Video
You may view the video here: [Video](https://youtu.be/5SMN2erMR8I)
> Do note that the website may differ slightly from the video but core fucntions remain the same

---


## ℹ️ Additional Notes

- If you encounter permission issues, try running the Docker command with `sudo`.

---

## Future Developments

- Stock control management and warning system where headquarter staff will be notified when stocks are low so they would be replenished to ensure goods are readily available
- As we implement this system into different outlets, we must change our database to reflect this change
- More users and customer base also means that our id cannot be capped at 8 digits long and maybe can be 10 digits long in the future
- Website could use more styling to attract more customers
- The website can also be a form of advertisement to reflect discounts/flash sales in the physical stalls in the future

---


## 💻Contributions

|Name|Main Working Branch|Contributions|
|----|------|-------------|
|Rondell|Rondell|• Team Sprint Planning <br> • Build a Functioning MySQL database <br> • Linking Hardware to Database <br> Login (hardware) <br> • Signup <br> • Buying Products Main Process (hardware) <br> • Hashing Passwords <br> • Main Checkout Process <br> • Dockerfile and Containerization <br> • Website Styling <br> • Edit Card Information Page <br> • Readme File <br> • Merging of Branches<br> • Releases |
|Benedict|Benedict|• Buzzer <br> • LED <br> • Scanning of BarCode <br> • RFID <br> • DCmotor <br> • Pytest <br> • SRS documentation <br> • System Test Report Documentation|
|Yining|Yining|• Backbone of a functioning Website <br> • Barcode Generation|

> ✍️Commits: Rondell (111/146, ~76.03%), Benedict (21/146, ~14.38%), Yining (14/146, 9.59%)


## Proudly Presented to you by:
- Rondell Lit (p2425630)
- Benedict Chen Hung Han(p2404619)
- Zhou Yining (p2425317)

> **Disclaimer** This project is created as part of the Diploma in Computer Engineering at Singapore Polytechnic. All code, diagrams, and documentation are for
 educational purposes
