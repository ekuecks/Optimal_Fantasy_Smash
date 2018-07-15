import argparse
import os.path
import sys

from tabulate import tabulate

from optimizer import Optimizer, Result


def main(args: argparse.Namespace) -> int:
    # players.txt holds the file with all players and their value and salary
    # as well as the salary cap
    if args.tournament:
        filename = None
    else:
        filename = os.path.expanduser(os.path.expandvars(args.filename))
    optimizer: Optimizer = Optimizer(filename=filename, tournament=args.tournament)
    opt: Result = optimizer.optimize()
    if not opt.players:
        raise ValueError("Failed to find any possible lineup for the tournament")
    headers = ["name", "salary", "value"]
    print(tabulate([(p.name, p.salary, p.value) for p in opt.players], headers))
    print("Optimal Score: {}".format(opt.value))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    input_data = parser.add_mutually_exclusive_group()
    input_data.add_argument(
        "--filename", help="Use the data in the unput file.", default="data/players.txt"
    )
    input_data.add_argument(
        "--tournament",
        # TODO: Unsuppress this argument when this feature is supported
        # help="Fetch data from smash.gg using the name of the tournament.",
        help=argparse.SUPPRESS,
    )

    sys.exit(main(parser.parse_args()))
