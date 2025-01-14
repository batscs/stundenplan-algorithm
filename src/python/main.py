import sys
from argparse import ArgumentParser


from utils import time_utils
from src.python.ga import genetic_algorithm
from src.python.log.logger import logger_app
from src.python.io import parser_json as parser
from src.python.io import printer_json as printer

def parse_arguments() -> tuple[int, str, str, bool]:
    """Parses command-line arguments for the genetic algorithm scheduling program.

    This function sets up the argument parser with the following options:
    - Generations: Specifies how many generations the genetic algorithm will run (default is 20000).
    - Term: Determines whether the term is summer or winter (default is summer).
    - Output format: Chooses the format for printing the results (default is tabular text format).

    If any error occurs while parsing, the help message is printed to stderr and the program exits
    using an appropriate exit code.

    Returns:
        A tuple containing the following parsed arguments:
        generations: Bumber of generations for the genetic algorithm.
        term: Term to be used for the scheduling ("Sommer" or "Winter").
        output_format: Output format type ("Tabular").
    """
    parser: ArgumentParser = ArgumentParser(
        prog="fhw_timeschedule_generator",
        description="This program uses a genetic algorithm to optimize the scheduling of events "
        + "for a given term. It processes input parameters for the number of generations, "
        + "term (summer or winter), and the output format of the results.",
    )
    parser.add_argument(
        "-g",
        "--generations",
        metavar="N",
        type=int,
        default=genetic_algorithm.NUM_GENERATIONS,
        help=f"Set number of generations (defaults to {genetic_algorithm.NUM_GENERATIONS})",
    )
    parser.add_argument(
        "-s",
        "--summer",
        action="store_true",
        help="Set summer term (default)",
        default=True,
    )
    parser.add_argument(
        "-w",
        "--winter",
        action="store_true",
        help="Set winter term (overrides -s)",
        default=False,
    )
    parser.add_argument(
        "-t",
        "--print-tabular",
        action="store_true",
        help="Print result to a .txt file using a table format (default)",
        default=True,
    )
    parser.add_argument(
        "-d",
        "--debug_mode",
        action="store_true",
        help="Turn debug mode on",
        default=False,
    )
    # parser.add_argument(
    #     "-x",
    #     "--print-xml",
    #     action="store_true",
    #     help="Print result to an .xml file using the splan format.",
    #     default=False,
    # )
    try:
        args = parser.parse_args()
        return (
            args.generations,
            "Winter" if args.winter else "Sommer",
            # TODO: Use when print to xml is implemented: "XML" if args.print_xml else "Tabular"
            "Tabular",
            args.debug_mode,
        )
    except SystemExit as e:
        if e.code != 0:
            print(parser.format_help(), file=sys.stderr)
        exit(e.code)





def main() -> None:
    logger_app.debug("Starting Application")

    generations, _, output_format, debug_mode = parse_arguments()
    parser.parse()
    print(f"Genetic algorithm started (generations = {generations})")

    # ------ RUNTIME ESTIMATION - commented out to avoid logging
    #runtime, _, _, _ = genetic_algorithm(1, term)
    #estimated_runtime: float = generations * runtime
    #print(f"Estimated runtime up to: {time_utils.seconds_to_formatted_duration(estimated_runtime)}")

    runtime, parsed_solution, fitness, generations_completed = genetic_algorithm.genetic_algorithm(generations)
    print(f"\nSolution fitness: {fitness}")
    print(f"Generations completed: {generations_completed}")
    print(f"Actual runtime: {time_utils.seconds_to_formatted_duration(runtime)}")

    printer.printer_save(parsed_solution, fitness, debug_mode)

    exit(0)


if __name__ == "__main__":
    main()
