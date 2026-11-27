"""Demo runner for EED461: Design and Analysis of Algorithms project tasks."""

import argparse

from tasks.task1_coin_removal import _run_demo as run_task1_demo
from tasks.task2_domino_tiling import _run_demo as run_task2_demo
from tasks.task3_switches import _run_demo as run_task3_demo
from tasks.task4_points import _run_demo as run_task4_demo
from tasks.task5_round_table import _run_demo as run_task5_demo
from tasks.task6_killing_squares import _run_demo as run_task6_demo
from tasks.task7_poison_test import _run_demo as run_task7_demo
from tasks.task8_tromino import _run_demo as run_task8_demo


def main() -> None:
    runners = {
        1: run_task1_demo,
        2: run_task2_demo,
        3: run_task3_demo,
        4: run_task4_demo,
        5: run_task5_demo,
        6: run_task6_demo,
        7: run_task7_demo,
        8: run_task8_demo,
    }

    parser = argparse.ArgumentParser(
        description="Run demo test cases for EED461 Algorithm project tasks."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=sorted(runners),
        help="Run a specific task (omit to run all implemented tasks).",
    )
    args = parser.parse_args()

    if args.task is not None:
        runners[args.task]()
    else:
        for task_id in sorted(runners):
            runners[task_id]()
            print()


if __name__ == "__main__":
    main()
