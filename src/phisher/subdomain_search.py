import json
import netlas
from time import sleep

# from __main__ import netlas_connection

# For debugging
netlas_connection = netlas.Netlas(api_key='XscrhB8jzaXqGjgg3IgWXCdm19V5k4ai')


def extract_domain_from_bytes(iterator) -> str:
    # Считываем байты из итератора и объединяем их в одну строку
    bytes_data = b"".join(iterator)

    # Декодируем байты в строку
    json_string = bytes_data.decode("utf-8")

    # Преобразуем строку в JSON объект
    json_data = json.loads(json_string)

    # Извлекаем поле "domain" из JSON объекта
    domain = json_data.get("domain", "")

    return domain

class SubdomainSearch:
    def __init__(self) -> None:
        pass

    """Generate query like "domain:<name>.* level:[3 TO max_level]"""

    @staticmethod
    def _make_query(name: str, max_level: int) -> str:
        return f"domain:{name}.* level:[3 TO {max_level}]"

    @staticmethod
    def search_subdomains(names: [], max_level: int) -> []:
        global netlas_connection
        domains = []
        for name in names:
            query = SubdomainSearch._make_query(name, max_level)
            count = netlas_connection.count(datatype="domain",
                                            query=query)["count"]
            if count != 0:
                iterator_of_bytes = netlas_connection.download(datatype="domain",
                                                               query=query,
                                                               size=count)
                # save domain field in list
                domains.append(extract_domain_from_bytes(iterator_of_bytes))
            sleep(1)
        return domains


results = SubdomainSearch.search_subdomains(names=["vkontakte"], max_level=4)
print(results)
