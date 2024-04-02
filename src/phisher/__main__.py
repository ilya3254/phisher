import netlas
import argparse
import cout
import inparse
import domain_mutations

# Global constants
is_verbose = False

def main():
    global is_verbose
    # Print utility wrapper
    cout.print_banner()

    # Processing command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", help="file with resources")
    parser.add_argument("api_key", help="personal API key")
    parser.add_argument("-v", "--verbose", help="run in verbose mode",
                        action="store_true")
    parser.add_argument("-n", "--normal", help="run in normal mode",
                        action="store_true")

    args = parser.parse_args()

    # Select console output mode
    if args.verbose:
        is_verbose = True
        print("Processing in verbose mode...\n")
    else:
        is_verbose = False
        print("Processing in normal mode...")

    percents = 0
    # Processing
    input_data = inparse.Inparse()
    input_data.parse(inparse.read(args.input_file))
    # лучше инициировать подключение с апи ключом сразу, 
    # а модулям передавать готовый Netlas объект
    #netlas_connection = netlas.Netlas(api_key=args.api_key)

    domain_mutation = domain_mutations.DomainMutations(input_data.domains, args.api_key)
    domain_mutation.search_mutation_domains(percents)


if __name__ == "__main__":
    main()
