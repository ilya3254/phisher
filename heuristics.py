import dnstwist

class DomainMutation:
    def __init__(self, input_list):
        self.domain_list = input_list
        self.mutation_data_filepath = "domain_mutations.txt"

    def get_domain_mutations(self, domain_name):
        dnstwist.run(domain=domain_name, format='list', 
                     output = self.mutation_data_filepath)
    
    #основа функции организации эвристики  
    def fetch_domain_mutations(self):
        for domain in self.domain_list:
            self.get_domain_mutations(domain)
            #функция, делающая запрос Netlas.io