import netlas
import argparse
from rich.progress import Progress
import cout
import inparse
import domain_mutations
import subdomains
from keywords import Keywords


def main():
    # Processing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--perimeter", help="Path to file with perimeter data")
    parser.add_argument("-a", "--apikey", help="Personal Netlas API key")
    args = parser.parse_args()

    # Processing
    perimeter = inparse.Inparse()
    perimeter.parse(inparse.read(args.perimeter))
    # модулям передается готовый инициализированный Netlas объект
    netlas_connection = netlas.Netlas(api_key=args.apikey)

    potential_phishing = []

    mutations = domain_mutations.DomainMutations(netlas_connection)
    existing_mutdomains = mutations.search(domains=perimeter.domains)
    potential_phishing.extend(existing_mutdomains)

    SubdomainS = subdomains.Subdomains(netlas_connection)
    existing_subdomains = SubdomainS.search(names=perimeter.brandnames,
                                            legit_topdomains=perimeter.topdomains)
    potential_phishing.extend(existing_subdomains)

    # Для теста. Все равно тратит много времени, но намного меньше, чем до этого
    with Progress() as progress:
        total_task = progress.add_task("[red]Search for keywords...", total=len(potential_phishing))
        for domain in potential_phishing:
            result = Keywords.search(domain=domain, keywords=perimeter.keywords).values()
            #for keyword in result:
            #    if keyword > 1:
            #        pass
            print(result)
            progress.update(total_task, advance=1)

    # добавить whoisreg и urlsearch

    # тут красивый вывод potential_phishing
    print(potential_phishing)


if __name__ == "__main__":
    main()
