import json
from netlas import Netlas
from time import sleep


def parse_jsons(json_string):
    json_string = '[' + json_string.replace('}{', '},{') + ']'
    return json.loads(json_string)


# Heuristics are needed to identify legitimate resources obtained.
class WhoisRegistration():
    def __init__(self, netlas_connection: Netlas) -> None:
        self.netlas_connection = netlas_connection

    # Returns two lists: correct and incorrect resources - according to the received registration data.
    def search(self, domains: list, org_name: list) -> list:
        correct_domains = []    # domains that match the registration data
        wrong_domains = []      # domains that don't match the registration data
        for domain in domains:
            count = self.netlas_connection.count(datatype="whois-domain",
                                                 query=domain)['count']
            if count != 0:
                iterator = self.netlas_connection.download(datatype="whois-domain",
                                                           query=domain, size=count)
                # saving domain field in the list by default
                bytes_data = b"".join(iterator)
                results = parse_jsons(bytes_data.decode("utf-8"))
                # for every domain check registrant data
                # To do: put the verification of registration data in a separate procedure
                for response in results:
                    for name in org_name:
                        if 'registrant' in response['data'] and 'organization' in response['data']['registrant']:
                            if response['data']['registrant']['organization'] == name:
                                correct_domains.append(response['data']['domain'])
                        else:
                            wrong_domains.append(response['data']['domain'])
            sleep(1)
        return correct_domains, wrong_domains


    
# Example for debugging
if __name__ == "__main__":
    netlas_connection = Netlas(api_key='api_key')
    registrant = WhoisRegistration(netlas_connection)
    correct_domains, wrong_domains = registrant.search(domains=["vkontakte"], org_name=["LLC \"V Kontakte\"", "V Kontakte LLC"])
    print(correct_domains, wrong_domains)