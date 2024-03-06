import dnstwist
import netlas
from os import remove, path
from time import sleep


def write_bytes_to_file(iterator, filepath):
    with open(filepath, 'ab') as file:
        for chunk in iterator:
            file.write(chunk)


class DomainMutation:
    def __init__(self, input_list, api_key):
        self.domain_list = input_list
        self.mutation_data_filepath = 'domain_mutations.txt'
        self.api_key = api_key

     # Gets a domain mutations list and saves in file
    def _mutate_domain(self, domain_name):
        # Delete previous domain_mutations file
        if(path.exists(self.mutation_data_filepath)):
            remove(self.mutation_data_filepath)

        # Mutate and saves in domain_mutations file
        dnstwist.run(domain=domain_name, format='list',
                     output=self.mutation_data_filepath)
        
        # Deletes first string from domain_mutations file
        f = open(self.mutation_data_filepath).readlines()
        f.pop(0)
        with open(self.mutation_data_filepath,'w') as modf:
            modf.writelines(f)

    # Generates a query with domain mutations like 'domain:x.com || domain:y.com'
    def _make_query(self, max_query_length=3000):
        with open(self.mutation_data_filepath, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        result = []
        current_string = ""

        for line in lines:
            part = f'domain:{line}'
            if len(current_string) + len(part) + len(" || ") > max_query_length:
                result.append(current_string[:-4])
                current_string = part + " || "
            else:
                current_string += part + " || "

        if current_string:
            result.append(current_string[:-4])

        return result

    # Executes a query to Netlas, saves the response to dst_filepath
    def search_mutation_domains(self, dst_filepath='output_file.json', fields=None):
        # Clear file
        with open(dst_filepath, 'wb') as file:
            pass
        # Create connection to Netlas
        netlas_connection = netlas.Netlas(api_key=self.api_key)
        for domain in self.domain_list:
            self._mutate_domain(domain)
            queries = self._make_query()
            for query in queries:
                count = netlas_connection.count(datatype='domain',
                                                query=query)['count']
                if count != 0:
                    iterator_of_bytes = netlas_connection.download(datatype='domain',
                                                                   query=query,
                                                                   fields=fields,
                                                                   size=count)
                    write_bytes_to_file(iterator_of_bytes, dst_filepath)
                sleep(0.5)

# Example:
# mutation = DomainMutation([input_list])
# mutation.search_mutation_domains()
