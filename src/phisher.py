import argparse
import consoleout
import parse
import heuristics

# Global constants
is_verbose = False

# Print utility wrapper
consoleout.print_banner()

# Processing command line arguments
parser = argparse.ArgumentParser()

parser.add_argument("input_file", help="file with resources")
parser.add_argument("-v", "--verbose", help="run in verbose mode", 
                     action="store_true")
parser.add_argument("-n", "--normal", help="run in normal mode", 
                    action="store_true")

args = parser.parse_args()

# Select consoleout mode
if args.verbose:
    is_verbose = True
    print("Processing in verbose mode...\n")
else:
    is_verbose = False
    print("Processing in normal mode...")


# Processing
input_data = parse.Parse()
input_data.magic(parse.read(args.input_file))

domain_mutation = heuristics.DomainMutation(input_data.domains)
domain_mutation.search_mutation_domains()

