import re
import json
import dnstwist
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
    def _mutate_domain(domain_name: str, tmp_file="domain_mutations.tmp") -> list:
        # Создаем путь к временному каталогу в текущем рабочем каталоге
        tmp_dir_path = path.join(path.dirname(__file__), "tmp")
        
        # Создаем каталог, если он не существует
        makedirs(tmp_dir_path, exist_ok=True)
        
        # Полный путь к временному файлу
        full_tmp_file_path = path.join(tmp_dir_path, tmp_file)

        # Delete previous domain_mutations file
        if path.exists(full_tmp_file_path):
            remove(full_tmp_file_path)
        # Mutate and saves in domain_mutations file
        dnstwist.run(domain=domain_name, format="list",
                     output=full_tmp_file_path)
        # Extract mutations from file
        with open(full_tmp_file_path, 'r') as file:
            mutations = file.readlines()
        if mutations:
            mutations.pop(0)
        for i in range(len(mutations)):
            mutations[i] = re.sub(r'\.[^.]*$', '.*', mutations[i])
        return mutations

    # Generates a query list with domain mutations like "domain:(example.* || another.*) level:2"
    # with maximum query operands '||' 100 by default
    @staticmethod
    def _make_query(mutations: list, max_query_operands=100) -> list:
        queries = []
        current_string = "domain:("
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
        for domain in domains:
            mutations = self._mutate_domain(domain)
            queries = self._make_query(mutations=mutations)
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
                sleep(1)
        return results

# Example for debugging
if __name__ == "__main__":
    netlas_connection = Netlas(api_key="-")
    mutations = DomainMutations(netlas_connection)
    domains = mutations.search(domains=["netlas.io"])
    print(domains)