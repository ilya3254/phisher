import netlas
import argparse
from rich.progress import track
import cout
import inparse
import domain_mutations
import subdomains
import keywords


def main():
    # Processing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "-perimeter", help="Path to file with perimeter data")
    parser.add_argument("-a", "-apikey", help="Personal Netlas API key")
    args = parser.parse_args()

    # Processing
    perimeter = inparse.Inparse()
    perimeter.parse(inparse.read(args.input_file))
    # модулям передается готовый инициализированный Netlas объект
    netlas_connection = netlas.Netlas(api_key=args.api_key)

    potential_phishing = []

    mutations = domain_mutations.DomainMutations(netlas_connection)
    existing_mutdomains = mutations.search(domains=perimeter.domains)
    potential_phishing.extend(existing_mutdomains)

    SubdomainS = subdomains.Subdomains(netlas_connection)
    existing_subdomains = SubdomainS.search(names=perimeter.brandnames,
                                            legit_topdomains=perimeter.topdomains)
    potential_phishing.extend(existing_subdomains)

    KeywordS = keywords.Keywords(netlas_connection)
    # возможно, код ниже стоит перенести в keywords.py
    for domain in track(potential_phishing, description="[red]Search for keywords..."):
        result = KeywordS.search(domain=domain, keywords=perimeter.keywords)
        for keyword in result:
            if keyword > 1:
                pass  # нужно продумать логику, что делать при совпадениях

    # добавить whoisreg и urlsearch

    # тут красивый вывод potential_phishing


if __name__ == "__main__":
    main()
