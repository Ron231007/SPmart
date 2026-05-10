import pytest
from calculatePrice_or_points import calculateTotalPrice, calculatePoints
from access_database import verify_card_info, got_ATM_card, get_points
import mysql.connector

def test_calculateTotalPrice():
    items = [
        ("Butter", 8, 5.15),
        ("Milk", 10, 6.7),
        ("Eggs", 5, 4.15),
        ("Beer", 3, 5.5),
        ("Apple", 20, 1.2),
    ]
    expected_total = (
        (8 * 5.15) + (10 * 6.7) + (5 * 4.15) + (3 * 5.5) + (20 * 1.2)
    )
    assert calculateTotalPrice(items) == expected_total

def test_calculatePoints_non_admin():
    cost = 23.45
    isAdmin = False
    expected_points = 60
    assert calculatePoints(cost, isAdmin) == expected_points

def test_calculatePoints_admin():
    cost = 23.45
    isAdmin = True
    expected_points = 120
    assert calculatePoints(cost, isAdmin) == expected_points

def test_verify_card_info():
    # Test with correct password and card ID
    assert verify_card_info(13, 1234567890, "12345678", False) == True

def test_got_atm_card():
    assert got_ATM_card(2, True) == True
    assert got_ATM_card(1, True) == False
    assert got_ATM_card(13, False) == True
    assert got_ATM_card(12, False) == False

def test_get_points():
    assert get_points(10, False) == 120
    assert get_points(1, True) == 0
