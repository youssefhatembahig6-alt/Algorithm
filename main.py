"""Demo runner for EED461: Design and Analysis of Algorithms project tasks."""

import argparse

from tasks.task1_coin_removal import _run_demo as run_task1_demo
from tasks.task2_domino_tiling import _run_demo as run_task2_demo
from tasks.task5_round_table import _run_demo as run_task5_demo


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run demo test cases for EED461 Algorithm project tasks."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=[1, 2, 5],
        help="Run a specific task (omit to run all implemented tasks).",
    )
    args = parser.parse_args()

    runners = {
        1: run_task1_demo,
        2: run_task2_demo,
        5: run_task5_demo,
    }

    if args.task is not None:
        runners[args.task]()
    else:
        for task_id in sorted(runners):
            runners[task_id]()
            print()


if __name__ == "__main__":
    main()
