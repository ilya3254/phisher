import dnstwist
import netlas
from os import remove, path
from time import sleep
from cout import print_percents

# Percent increment
percents_inc = 0


''' FILE FUNCTIONS '''


# Writes bytes to file
def write_bytes_to_file(iterator, filepath):
    with open(filepath, "ab") as file:
        for chunk in iterator:
            file.write(chunk)


# Prepares domain_mutations file
def prepare_mutation_file(filepath):
    # Deletes first string from domain_mutations file
    f = open(filepath).readlines()
    f.pop(0)
    # Replaces 'com' end of string on '*'
    for line in range(len(f)):
        f[line] = f[line].replace("com", "*")
    # Saves modify file
    with open(filepath, "w") as modf:
        modf.writelines(f)


class DomainMutations:
    def __init__(self, input_list, api_key):
        self.domain_list = input_list
        self.mutation_data_filepath = "domain_mutations.txt"
        self.api_key = api_key

    # Gets a domain mutations list and saves in file
    def _mutate_domain(self, domain_name):
        # Delete previous domain_mutations file
        if path.exists(self.mutation_data_filepath):
            remove(self.mutation_data_filepath)

        # Mutate and saves in domain_mutations file
        dnstwist.run(domain=domain_name, format="list",
                     output=self.mutation_data_filepath)

        prepare_mutation_file(self.mutation_data_filepath)

    # Generates a query list with domain mutations like "domain:x.com || domain:y.com"
    # with maximum query operands 25
    def _make_query(self, max_query_operands=25):
        with open(self.mutation_data_filepath, "r") as file:
            lines = [line.strip() for line in file.readlines()]

        result = []
        current_string = ""
        current_operands = 0

        for line in lines:
            part = f"domain:{line}"
            if current_operands >= max_query_operands:
                result.append(current_string[:-4])  # remove " || "
                current_string = part + " || "
                current_operands = 1
            else:
                current_string += part + " || "
                current_operands += 1

        if current_string:
            result.append(current_string[:-4])  # remove " || "

        return result

    # Executes a query to Netlas, saves the response to dst_filepath
    def search_mutation_domains(self, percents,
                                dst_filepath="output_file.json", fields=None):
        global percents_inc
        print_percents(percents)
        # Clear file
        with open(dst_filepath, "wb") as file:
            pass
        # Create connection to Netlas
        netlas_connection = netlas.Netlas(api_key=self.api_key)

        # Counts percent from processing of one domain
        domain_percents = 100 / len(self.domain_list)

        # Domains processing
        for domain in self.domain_list:
            self._mutate_domain(domain)
            queries = self._make_query()

            # Counts percent increment on every loop step
            percents_inc = domain_percents / len(queries)

            for query in queries:
                count = netlas_connection.count(datatype="domain",
                                                query=query)["count"]
                if count != 0:
                    iterator_of_bytes = netlas_connection.download(datatype="domain",
                                                                   query=query,
                                                                   fields=fields,
                                                                   size=count)
                    write_bytes_to_file(iterator_of_bytes, dst_filepath)

                # Print percents
                percents += percents_inc
                print_percents(percents)
                # Delay for netlas requests
                sleep(1)
