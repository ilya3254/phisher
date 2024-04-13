import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class FindLinks:
    def __init__(self) -> None:
        pass

    # Function converts the provided DOMAIN into a URL for use in check_resources()
    @staticmethod
    def _domain_to_url(domain: str, protocol='https') -> str:
        if not domain.startswith('http://') and not domain.startswith('https://'):
            url = f"{protocol}://{domain}"
        else:
            url = domain
        return url
    
    # Function finds all links to images and icons present on the page and its subdomains.
    # Returns a list of image links and a list of icon links.
    def check_resources(self, domain: str) -> tuple[list, list]:
        available_images = set()
        available_icons = set()

        url = self._domain_to_url(domain)
        # Queue for traversing links on pages
        queue = [url]

        for current_url in queue:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Search for images
            images = soup.find_all('img', src=True)
            for image in images:
                src = image['src']
                full_src = urljoin(current_url, src)
                available_images.add(full_src)

            # Search for icons
            icons = soup.find_all('link', rel='icon')
            for icon in icons:
                href = icon['href']
                full_href = urljoin(current_url, href)
                available_icons.add(full_href)

            # Add links with subdomains to the queue
            subdomains = set()
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                parsed_link = urlparse(href)
                if parsed_link.netloc.endswith(domain) and parsed_link.netloc != domain:
                    subdomains.add(parsed_link.netloc)
            for subdomain in subdomains:
                parsed_url = urlparse(current_url)
                subdomain_url = f"{parsed_url.scheme}://{subdomain}"
                if subdomain_url not in queue:  # Add the link to the queue if it's not there already
                    queue.append(subdomain_url)
                
        return list(available_images), list(available_icons)


# Example for debug
if __name__ == "__main__":
    domain = "bspb.ru"  # company domain
    img_links, icons_links = FindLinks().check_resources(domain,)
    print(img_links, icons_links)
