import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tasks.task6_killingSquares import breakAllSquares

# Testing
for n in range(1, 5):
    answer = breakAllSquares(n)

    print(f"Board: {n} x {n}")
    print("Minimum toothpicks:", len(answer))
    print("Removed toothpicks:", answer)
    print()
