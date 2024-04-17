from rich.progress import Progress
from netlas import Netlas
from time import sleep


class Keywords():
    def __init__(self, netlas_connection: Netlas) -> None:
        self.netlas_connection = netlas_connection
        
    # Generates query like 'host:<domain> port:(443 || 80) path:"/" http.body:"<keyword>"'
    @staticmethod
    def _make_query(domain: str, keyword: str) -> str:
        return f'host:{domain} port:(443 || 80) path:"/" http.body:"{keyword}"'

    # Takes a domain and a list of keywords.
    # Returns a dictionary where the keys are keywords and the values are the number of matches (0 or >=1).
    def search(self, domain: str, keywords: list) -> dict:
        result = {keyword: 0 for keyword in keywords}
        with Progress() as progress:
            total_task = progress.add_task(f"[green]Search for keywords for {domain}...", total=len(keywords))
            for keyword in keywords:
                query = self._make_query(domain, keyword)
                count = self.netlas_connection.count(datatype="response",
                                                     query=query)['count']
                result[keyword] = count
                progress.update(total_task, advance=1)
                sleep(1)
        return result


# Example for debugging
if __name__ == "__main__":
    netlas_connection = Netlas(api_key="apikey")
    KeywordS = Keywords(netlas_connection)
    result = KeywordS.search(domain="www.bspb.ru", keywords=["Банк", "Банк Санкт-Петербург", "БСПБ"])
    print(result)
