import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tasks.task7_posionTest import designWineTests

# Example: 10 testers
possible, schedule, decoder = designWineTests(10)

print("Possible:", possible)

# Display which barrels each tester should taste
for tester, barrels in schedule.items():
    print(f"Tester {tester + 1}: {barrels}")

# Example: Tester 1 and Tester 3 die
# 1 means dead, 0 means alive
results = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0]

print("Poisoned barrel:", decoder(results))


# Example: 8 testers
possible, schedule, decoder = designWineTests(8)
print("\nWith 8 testers:", possible)
