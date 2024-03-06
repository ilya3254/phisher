import dnstwist
import netlas

apikey = 'apikey'


def write_bytes_to_file(iterator, filepath):
    with open(filepath, 'wb+') as file:
        for chunk in iterator:
            file.write(chunk)


class DomainMutation:
    def __init__(self, input_list):
        self.domain_list = input_list
        self.mutation_data_filepath = 'domain_mutations.txt'

    def _mutate_domain(self, domain_name):
        dnstwist.run(domain=domain_name, format='list',
                     output=self.mutation_data_filepath)

    # Generates a query with domain mutations like 'domain:x.com || domain:y.com'
    def _make_query(self):
        with open(self.mutation_data_filepath, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        query = ' || '.join([f'domain:{line}' for line in lines])
        return query

    # Executes a query to Netlas, saves the response to dst_filepath
    def search_mutation_domains(self, dst_filepath='..\\output\\output_file.json', fields=None):
        # Clear file
        with open(dst_filepath, 'wb') as file:
            pass
        # Create connection to Netlas
        netlas_connection = netlas.Netlas(api_key=apikey)
        for domain in self.domain_list:
            self._mutate_domain(domain)
            query = self._make_query()
            count = netlas_connection.count(datatype='domain',
                                            query=query)['count']
            iterator_of_bytes = netlas_connection.download(datatype='domain',
                                                           query=query,
                                                           fields=fields,
                                                           size=count)
            write_bytes_to_file(iterator_of_bytes, dst_filepath)

# Example:
# mutation = DomainMutation([input_list])
# mutation.search_mutation_domains()
