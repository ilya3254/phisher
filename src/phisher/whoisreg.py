import json
from netlas import Netlas
from time import sleep
from typing import Tuple


def parse_jsons(json_string):
    json_string = '[' + json_string.replace('}{', '},{') + ']'
    return json.loads(json_string)


# Heuristics are needed to identify legitimate resources obtained.
class WhoisIdentification():
    def __init__(self, netlas_connection: Netlas) -> None:
        self.netlas_connection = netlas_connection
        
    def check_registration_data(self, data: dict, org_name: dict) -> bool:
    # Check if registrant organization matches any of the specified organization names
    if 'registrant' in data and 'organization' in data['registrant']:
        for name in org_name.get("organisation", []):
            if data['registrant']['organization'] == name:
                return True
    # Check if registrant phone matches any of the specified phone numbers
    if 'registrant' in data and 'phone' in data['registrant']:
        for phone in org_name.get("phone", []):
            if data['registrant']['phone'] == phone:
                return True
    # Check if registrant email matches any of the specified email addresses
    if 'registrant' in data and 'email' in data['registrant']:
        for email in org_name.get("email", []):
            if data['registrant']['email'] == email:
                return True
    return False


    # Returns two lists: correct and incorrect resources - according to the received registration data.
    def search(self, domains: list, org_name: dict) -> Tuple[list, list]:
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
                
                # 1. Переделать функцию проверки: нужно чтобы проверял на совпадение с полями словаря,
                #                                 которые заданы пользователем.
                # 2. Убрать дублирование записей в списке wrong_domains
                # 3. Добавлять в список входных словарей список доменов из периметра, т.к. они тоже могут давать результат
                for result in results:
                    if 'registrant' in result['data'] and 'organization' in result['data']['registrant']:
                        for name in org_name:
                            if result['data']['registrant']['organization'] == name:
                                correct_domains.append(result['data']['domain'])
                    else:
                        wrong_domains.append(result['data']['domain'])
            sleep(1)
        return correct_domains, wrong_domains

    
# Example for debugging
donain_mutations = ["vkontakte.*"]
whoisreg = {"organisation": ["LLC \"V Kontakte\"", "V Kontakte LLC"],
            "email": [],
            "phone": []}

if __name__ == "__main__":
    netlas_connection = Netlas(api_key='1CNI8pZAx3vYWfJqaD74fEc1cSi5KsTW')
    registrant = WhoisIdentification(netlas_connection)
    correct_domains, wrong_domains = registrant.search(domains=donain_mutations , org_name=whoisreg)
    print(correct_domains, wrong_domains)