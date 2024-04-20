import re
import json
import dnstwist
from rich.progress import Progress
from netlas import Netlas
from os import remove, path, makedirs
from time import sleep


def parse_jsons(json_string):
    json_string = '[' + json_string.replace('}{', '},{') + ']'
    return json.loads(json_string)


class DomainMutations:
    def __init__(self, netlas_connection: Netlas) -> None:
        self.netlas_connection = netlas_connection

    # TO DO: Make the file saved in a specific "tmp" directory
    # Returns a domain mutations list.
    @staticmethod
    def _mutate_domain(domain_name: str) -> list:
        tmp_dir_path = path.join(path.dirname(__file__), "tmp")
        makedirs(tmp_dir_path, exist_ok=True)
        tmp_path = path.join(tmp_dir_path, "domain_mutations.tmp")

        # Delete previous domain_mutations file
        if path.exists(tmp_path):
            remove(tmp_path)
        # Mutate and saves in domain_mutations file
        dnstwist.run(domain=domain_name, format="list",
                     output=tmp_path)
        # Extract mutations from file
        with open(tmp_path, 'r') as file:
            mutations = file.readlines()
        if mutations:
            mutations[0] = mutations[0].strip() + '*'
        for i in range(1, len(mutations)):
            mutations[i] = re.sub(r'\.[^.]*$', '.*', mutations[i])
        return mutations

    # Generates a query list with domain mutations like "domain:(example.* || another.*) level:2"
    # with maximum query operands '||' 100 by default
    @staticmethod
    def _make_query(mutations: list, max_query_operands=100) -> list:
        queries = []
        current_string = "a:* domain:("
        current_operands = 0
        for mutation in mutations:
            part = f"{mutation}"
            if current_operands >= max_query_operands:
                queries.append(current_string[:-4] + ") level:2")  # remove " || " and add ") level:2"
                current_string = "domain:(" + part + " || "
                current_operands = 1
            else:
                current_string += part + " || "
                current_operands += 1
        if current_string:
            queries.append(current_string[:-4] + ") level:2")  # remove " || " and add ") level:2"
        return queries

    # ATTENTION: Parsing response from Netlas can take a long time! Therefore, we need to be smart about implementing a 1 second delay for requests.
    # TO DO: Check to see if they belong to the perimeter and exclude such domains. For example domain!=*.example.com AND domain!=example.com.
    # Executes a query to Netlas, returns the domain list
    def search(self, domains: list) -> list:
        results = []
        with Progress() as progress:
            total_task = progress.add_task("[green]Search for domain mutations...", total=len(domains))
            for domain in domains:
                mutations = self._mutate_domain(domain)
                queries = self._make_query(mutations=mutations)
                domain_task = progress.add_task(f"[blue]Search mutations for {domain}...", total=len(queries))
                for query in queries:
                    count = self.netlas_connection.count(datatype="domain",
                                                         query=query)['count']
                    if count != 0:
                        iterator_of_bytes = self.netlas_connection.download(datatype="domain",
                                                                            query=query,
                                                                            fields="domain",
                                                                            size=count)
                        response = parse_jsons(b"".join(iterator_of_bytes).decode("utf-8"))
                        # saving domain field in the result list by default
                        for item in response:
                            results.append(item['data']['domain'])
                    progress.update(domain_task, advance=1)
                    sleep(1)
                progress.update(total_task, advance=1)
        return results


# Example for debugging
if __name__ == "__main__":
    netlas_connection = Netlas(api_key="1CNI8pZAx3vYWfJqaD74fEc1cSi5KsTW")
    mutations = DomainMutations(netlas_connection)
    domains = mutations.search(domains=["wildberries.ru"])
    print(domains)
