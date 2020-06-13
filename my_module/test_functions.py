import pytest
from functions import *

def test_boat_coords():
    """ Test the boat_coords function """
    actual = boat_coords("battleship", "down", 0, 0)
    expected = [(0, 0), (0, 1), (0, 2), (0, 3)]
    assert actual == expected

    actual = boat_coords("patrol boat", "left", 3, 5)
    expected = [(3, 5), (2,5)]
    assert actual == expected

def test_is_end():
    """ Test the is_end method in Battleship """
    x = Battleship()
    x.board = [["+", "+", "+", "+", "+", "+", "+"] for i in range(7)]
    x.ship_dir = {"battleship": "down", "submarine": "down", \
            "destroyer": "down", "patrol boat": "down"}
    x.ships_locs = {"battleship": [], "submarine": [], \
            "destroyer": [], "patrol boat": []}
    
    assert x.is_end()

    """ Test the is_end method in Battleship """
    x = Battleship()
    x.board = [["+", "+", "+", "+", "+", "+", "+"] for i in range(7)]
    x.ship_dir = {"battleship": "down", "submarine": "down", \
            "destroyer": "down", "patrol boat": "down"}
    x.ships_locs = {"battleship": [(1, 1)], "submarine": [], \
            "destroyer": [], "patrol boat": []}
    
    assert not x.is_end()

