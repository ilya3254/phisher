import requests
from bs4 import BeautifulSoup


class Keywords:
    @staticmethod
    def search(domain: str, keywords: list) -> dict:
        """
        Takes a domain and a list of keywords.
        Returns a dictionary where the keys are keywords and the values are the number of matches (0 or >=1).
        :param domain: str
        :param keywords: list
        :return: dict or None if connection failed
        """
        result = {keyword: 0 for keyword in keywords}
        try:
            response = requests.get("http://" + domain)
        except Exception as e:
            return result
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        for keyword in keywords:
            result[keyword] = text.lower().count(keyword.lower())
        return result


# Example for debugging
if __name__ == "__main__":
    res = Keywords.search(domain="bspb.ru", keywords=["Банк", "Банк Санкт-Петербург", "БСПБ"])
    print(res)
