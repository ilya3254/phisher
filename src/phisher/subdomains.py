import json
from netlas import Netlas
from time import sleep


def parse_jsons(json_string):
    json_string = '[' + json_string.replace('}{', '},{') + ']'
    return json.loads(json_string)


class Subdomains():
    def __init__(self, netlas_connection: Netlas) -> None:
        self.netlas_connection = netlas_connection
        
    """Generates query like "domain:<name>.* level:[3 TO max_level] !domain:(*.<legit_domain1> || *.<legit_domain2> || ...)"""
    @staticmethod
    def _make_query(name: str, legit_domains_exception: str, max_level: int) -> str:
        return f"domain:{name}.* level:[3 TO {max_level}] " + legit_domains_exception

    def search(self, names: list, legit_topdomains: list, max_level: int=4) -> list:
        domains = []
        legit_domains_exception = "!domain:(" + " || ".join([f"*.{domain}" for domain in legit_topdomains]) + ")"
        for name in names:
            query = self._make_query(name, legit_domains_exception, max_level)
            count = self.netlas_connection.count(datatype="domain",
                                            query=query)['count']
            if count != 0:
                iterator_of_bytes = self.netlas_connection.download(datatype="domain",
                                                                    query=query,
                                                                    size=count)
                # saving domain field in the list by default
                bytes_data = b"".join(iterator_of_bytes)
                results = parse_jsons(bytes_data.decode("utf-8"))
                for item in results:
                    domains.append(item['data']['domain'])
            sleep(1)
        return domains


# Example for debugging
if __name__ == "__main__":
    netlas_connection = Netlas(api_key='apikey')
    SubdomainS = Subdomains(netlas_connection)
    domains = SubdomainS.search(names=["bspb", "bank-spb", "bank-saint-petersburg"],
                                legit_topdomains=["bspb.ru", "bspb-processing.ru", "ved-360.ru", "bspb.org", "bspb-redbreasts.org", "www.bspb.lt", "bspb-intl.com", "bspb.biz", "bspb.parts", "bspb.pl", "bspb-pkb.com", "bspb.net", "bspb-asso-bretagne.fr", "bspb.org", "adv.br"])
    print(domains)
