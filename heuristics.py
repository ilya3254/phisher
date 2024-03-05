import dnstwist

class DomainMutation:
    def __init__(self, domain_list):
        self.domain_list = domain_list
        self.mutation_file_path = "domain_mutations.txt"

    def get_domain_mutations(self, domain_name):
        dnstwist.run(domain=domain_name, format='list', 
                     output = self.mutation_file_path)
