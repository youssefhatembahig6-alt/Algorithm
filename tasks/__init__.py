"""EED461: Design and Analysis of Algorithms - Project Tasks."""

from .task1_coin_removal import removeCoins
from .task2_domino_tiling import tileDominoes
from .task3_switches import turnOffSwitches
from .task4_points import colorPoints
from .task5_round_table import seatKnights, verify_seating
from .task6_killing_squares import breakAllSquares, verify_broken_squares
from .task7_poison_test import designWineTests, verify_wine_tests
from .task8_tromino import Tromino, tileTromino

__all__ = [
    "removeCoins",
    "tileDominoes",
    "turnOffSwitches",
    "colorPoints",
    "seatKnights",
    "verify_seating",
    "breakAllSquares",
    "verify_broken_squares",
    "designWineTests",
    "verify_wine_tests",
    "Tromino",
    "tileTromino",
]
