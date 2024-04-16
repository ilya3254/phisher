import netlas
import argparse
import cout
import inparse
import domain_mutations
import subdomains
import keywords


def main():
    # Processing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "-perimeter", help="file with perimeter data")
    parser.add_argument("-a", "-apikey", help="personal API key")
    args = parser.parse_args()

    # Processing
    perimeter = inparse.Inparse()
    perimeter.parse(inparse.read(args.input_file))
    # модулям передается готовый инициализированный Netlas объект
    netlas_connection = netlas.Netlas(api_key=args.api_key)

    mutations = domain_mutations.DomainMutations(netlas_connection)
    existing_mutdomains = mutations.search(domains=perimeter.domains)
    print(existing_mutdomains)

    SubdomainS = subdomains.Subdomains(netlas_connection)
    existing_subdomains = SubdomainS.search(names=perimeter.brandnames,
                                            legit_topdomains=perimeter.topdomains)
    print(existing_subdomains)

    KeywordS = keywords.Keywords(netlas_connection)
    result = KeywordS.search(domain="www.bspb.ru", keywords=["Банк", "Банк Санкт-Петербург", "БСПБ"])
    print(result)


if __name__ == "__main__":
    main()
