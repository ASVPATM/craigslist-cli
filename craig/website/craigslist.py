import urllib
import urllib.request
import webbrowser
import sys
from bs4 import BeautifulSoup
import requests
sys.path.append('cli/configs')
from configs import config
import website.ultimate as ultimate
from colorama import Fore, Back, Style

base_url = "https://craigslist.org"
location = ''

def fetchPage(query, search_index_bottom, search_index_top):
    
    temp_array = []

    
    if config.max_price != 0 and config.min_price != 0:
        #url = f"https://{location3}.craigslist.org/search/sss?max_price={config.max_price}&min_price={config.min_price}&query={config.query}#search=1~gallery~{config.page_number}~0"
        url = f"{config.city_url}/search/sss?max_price={config.max_price}&min_price={config.min_price}&query={config.query}#search=1~gallery~{config.page_number}~0"
        response = requests.get(url)
    else:
        #url = f"https://{location3}.craigslist.org/search/sss?query={config.query}#search=1~gallery~{config.page_number}~0"
        url = f"{config.city_url}/search/sss?query={config.query}#search=1~gallery~{config.page_number}~0"
        response = requests.get(url)

    
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    listings = soup.findAll('li', class_='cl-static-search-result')
    
    
    if len(listings) > 3:
        for x in range(search_index_bottom, search_index_top):
            print("\n")
            print(len(listings))
            print(x)
            listing = listings[x]
            title = listing.find('div', class_='title').text
            href = listing.find('a')['href']
            price = listing.find('div', class_='price').text
            print(listing.find('div', class_='location').text.strip())
            location = listing.find('div', class_='location').text.strip()

            # if location
            new_listing = [
                {
                    'index': x,
                    'title': title,
                    'href': href,
                    'price': price,
                    'location': location

                }
            ]
            config.json_listings.append(new_listing)
            ultimate.write_data(ultimate.file_json, config.json_listings)
            config.craigslist_array.append(new_listing)

            print(Fore.BLACK + "Index: "+ Fore.RED + "{}".format(x))
            print(Fore.CYAN +"Title: {}".format(title))
            print(Fore.LIGHTWHITE_EX + "URL: {}".format(href))
            print(Fore.GREEN + "Price: {}".format(price))
            print(Fore.YELLOW + "Location: {}".format(location))
    elif len(listings) == 2:
        print("\n")
        print(Fore.BLACK + "Index: "+ Fore.RED + "{}".format(0))
        listing = listings[0]
        title = listing.find('div', class_='title').text
        href = listing.find('a')['href']
        price = listing.find('div', class_='price').text
        location = listing.find('div', class_='location').text.strip()
        print(Fore.CYAN +"Title: {}".format(title))
        print(Fore.LIGHTWHITE_EX + "URL: {}".format(href))
        print(Fore.GREEN + "Price: {}".format(price))
        print(Fore.YELLOW + "Location: {}".format(location))
        config.looking_answer = 'n'

        print("\n")
        print(Fore.BLACK + "Index: "+ Fore.RED + "{}".format(1))
        listing = listings[1]
        title = listing.find('div', class_='title').text
        href = listing.find('a')['href']
        price = listing.find('div', class_='price').text
        location = listing.find('div', class_='location').text.strip()
        print(Fore.CYAN +"Title: {}".format(title))
        print(Fore.LIGHTWHITE_EX + "URL: {}".format(href))
        print(Fore.GREEN + "Price: {}".format(price))
        print(Fore.YELLOW + "Location: {}".format(location))
        config.looking_answer = 'n'
    elif len(listings) == 1:
        print("\n")
        print(Fore.BLACK + "Index: "+ Fore.RED + "{}".format(x))
        listing = listings[0]
        title = listing.find('div', class_='title').text
        href = listing.find('a')['href']
        price = listing.find('div', class_='price').text
        location = listing.find('div', class_='location').text.strip()
        print(Fore.CYAN +"Title: {}".format(title))
        print(Fore.LIGHTWHITE_EX + "URL: {}".format(href))
        print(Fore.GREEN + "Price: {}".format(price))
        print(Fore.YELLOW + "Location: {}".format(location))
        config.looking_answer = 'n'
    else:
        print("\nNo Results")
        

    
def keepSearching():
     pass



def main():
    pass
    
    

def commentedOutCode():
    pass


    


if __name__ == "__main__":
    main()

