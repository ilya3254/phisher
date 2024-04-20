import json
from rich.progress import Progress
from netlas import Netlas
from time import sleep


def parse_jsons(json_string):
    json_string = '[' + json_string.replace('}{', '},{') + ']'
    return json.loads(json_string)


class Subdomains():
    def __init__(self, netlas_connection: Netlas) -> None:
        self.netlas_connection = netlas_connection
        
    """Generates query like "domain:<name>.* level:[3 TO max_level] a:* !domain:(*.<legit_domain1> || *.<legit_domain2> || ...)"""
    @staticmethod
    def _make_query(name: str, legit_domains_exception: str, max_level: int) -> str:
        return f"domain:{name}.* level:[3 TO {max_level}] a:*" + legit_domains_exception

    # ATTENTION: Parsing response from Netlas can take a long time! Therefore, we need to be smart about implementing a 1 second delay for requests.
    # TO DO: Check to see if they belong to the perimeter and exclude such domains. For example domain!=*.example.com AND domain!=example.com.
    def search(self, names: list, legit_topdomains: list, max_level: int=4) -> list:
        domains = []
        legit_domains_exception = "!domain:(" + " || ".join([f"*.{domain}" for domain in legit_topdomains]) + ")"
        with Progress() as progress:
            total_task = progress.add_task("[yellow]Search for subdomains...", total=len(names))
            for name in names:
                query = self._make_query(name, legit_domains_exception, max_level)
                count = self.netlas_connection.count(datatype="domain",
                                                     query=query)['count']
                if count != 0:
                    iterator_of_bytes = self.netlas_connection.download(datatype="domain",
                                                                        query=query,
                                                                        fields="domain",
                                                                        size=count)
                    response = parse_jsons(b"".join(iterator_of_bytes).decode("utf-8"))
                    # saving domain field in the list by default
                    for item in response:
                        domains.append(item['data']['domain'])
                progress.update(total_task, advance=1)
                sleep(1)
        return domains


# Example for debugging
if __name__ == "__main__":
    netlas_connection = Netlas(api_key="1CNI8pZAx3vYWfJqaD74fEc1cSi5KsTW")
    SubdomainS = Subdomains(netlas_connection)
    domains = SubdomainS.search(names=["bspb", "bank-spb", "bank-saint-petersburg"],
                                legit_topdomains=["bspb.ru", "bspb-processing.ru", "ved-360.ru", "bspb.org", "bspb-redbreasts.org", "www.bspb.lt", "bspb-intl.com", "bspb.biz", "bspb.parts", "bspb.pl", "bspb-pkb.com", "bspb.net", "bspb-asso-bretagne.fr", "bspb.org", "adv.br"])
    print(domains)
