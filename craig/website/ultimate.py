
from itertools import count
from unidecode import unidecode
import sys
import webbrowser
import difflib
import json
import os
from configs import config
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import requests
from website import craigslist
import matplotlib as plt
import fontstyle

file_json = 'listings_data.json'



                       
def load_json(file_json):
    if os.path.exists(file_json):
        with open(file_json, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def write_data(file_json, data):
     with open(file_json, 'w') as file:
        json.dump(data, file, indent=4)

config.json_listings = load_json(file_json)


def setting_price():
    answer = ''
    attempts = 3
    if config.change_max_min_price == 'n':

        while True:
            try:
                max_min_answer = str(input(Fore.LIGHTYELLOW_EX +"\nDo You Want To Set a Maximum/Minimum Price?\n (PRESS Y OR N): ")).lower().strip()
                if max_min_answer == 'y' or max_min_answer == 'n':
                    answer = max_min_answer
                    break
                else:
                    print(Fore.RED + "Invalid Number, Please Select between 1 or 2" )
                    print(str(attempts) + " Attempts Left")
                    attempts-=1
                    if attempts <= 0:
                        break
            except ValueError:
                print(Fore.RED + "Invalid Input, Please Enter a Number") 
        while True:
            if answer == 'y':
                try:
                    print(Fore.LIGHTYELLOW_EX)
                    min_price_answer = int(input("Min: "))
                    max_price_answer = int(input("\nMax: "))
                    if min_price_answer >= 0 and min_price_answer <= max_price_answer:
                        config.min_price = min_price_answer
                        config.max_price = max_price_answer
                        break
                    else:
                        print(Fore.RED + "Make sure to enter valid values for the maximum/minimum. The minimum should be > 0 and <= maximum")
                except ValueError:
                    print(Fore.RED + "Enter Integer Values Only")
            else:
                break
    elif config.change_max_min_price == 'y':
    
            while True:
                try:
                    
                    change_max_min_input = int(input(Fore.YELLOW + "\n1) Change\n2) Get Rid Of\nAnswer Here: "))
                
                    if change_max_min_input == 1:
                        
                        min_price_answer = int(input(+ "Min: "))
                        max_price_answer = int(input("\nMax: "))
                        
                        if min_price_answer >= 0 and min_price_answer <= max_price_answer:
                            config.min_price = min_price_answer
                            config.max_price = max_price_answer
                            break
                        else:
                            print(Fore.RED + "Make sure to enter valid values for the maximum/minimum. The minimum should be > 0 and <= maximum")
                    elif change_max_min_input == 2:
                        config.max_price = 0
                        config.min_price = 0
                        break
                except ValueError:
                    print(Fore.RED + "Please enter a Valid Value")

def city():
        config.avail_locations = []
        config.avail_locations_regions = []
        # Change City Stuff Here
        while True:
            try:
                intro = fontstyle.apply("\n(Cities list based on Craigslist availability)",
                    "bold/Italic/purple")
                print(intro)

                region_answer_input = int(input(Fore.YELLOW + "\nSelect the region you would like to search:\n" + Fore.GREEN + "\n1) United States    2) "
                                          +"Canada    3) Europe    4) Asia/Pacific/Middle/East\n     5) Oceania     6) Latin America     7) Africa\n"+ Fore.YELLOW +"Answer Here: "))
                if region_answer_input >= 1 and region_answer_input <= 7:
                    if region_answer_input == 1:
                        config.region = "US"
                    elif region_answer_input == 2:
                        config.region = "CA"
                    elif region_answer_input == 3:
                        config.region = "EU"
                    elif region_answer_input == 4:
                        config.region = "ASIA"
                    elif region_answer_input == 5:
                        config.region = "OCEANIA"
                    elif region_answer_input == 6:
                        config.region = "LATAM"
                    elif region_answer_input == 7:
                        config.region = "AF"   
                    break
                else:
                    print(Fore.RED + "Please select a value within the range")
            except ValueError:
                print(Fore.RED + "Enter a Valud Value")

          

def handle_Region_Area(region):
    if region == 'US':
        while True:
            try:
                state_answer_input = str(input("In what state would you like to search?: ")).strip().lower()
                config.state_region = state_answer_input
                fetchLocations(config.region, config.state_region)
                if len(config.avail_locations) == 0:
                    print(Fore.RED + "Not availiable in your region ")
                    city()
                else:
                    print(Fore.YELLOW + "In " + Fore.GREEN + state_answer_input.capitalize() + Fore.YELLOW + ", you can search in: \n")
                    break
            except ValueError:
                print("Please Enter a Valid State")
        
        
        for x in range(0, len(config.avail_locations)):
            print(Fore.GREEN)
            if x == (len(config.avail_locations)/2):
                print(str(x+1) + ") " + f"{config.avail_locations[x]['name']}".capitalize()+ "\n")
            else:
                print(str(x+1) + ") "+ f"{config.avail_locations[x]['name']}".capitalize()+ " ")
        selectCity()
  
    else:
        while True:
            try:
                fetchLocations(region,'')

                for x in range(0, len(config.avail_locations_regions)):
                    if x % 2 == 1:
                        print(str(x+1) + ")" + f"{config.avail_locations_regions[x]}".capitalize() + "\n")
                    else:
                        print(str(x+1) + ")" + f"{config.avail_locations_regions[x]}".capitalize())
                country_answer_input = int(input("What region would you like to search?: "))
                if country_answer_input >= 1 and country_answer_input <= len(config.avail_locations_regions):
                    fetchLocations(config.region, config.avail_locations_regions[country_answer_input-1])
                    # print(config.avail_locations_regions[country_answer_input-1])
                    # print(config.avail_locations[0])
                    break
            except ValueError:
                print("Please Enter a Valid Country")
                
        if len(config.avail_locations) == 0:
            print("Not availiable in your region ")
            config.region = ''
            city()
        else:
            print("In " + config.avail_locations_regions[country_answer_input-1] + ", you can search in: \n")
        for x in range(0, len(config.avail_locations)):
            if x % 2 == 1:
                print(str(x+1) + ")" + f"{config.avail_locations[x]['name']}".capitalize() + "\n")
            else:
                print(str(x+1) + ")" + f"{config.avail_locations[x]['name']}".capitalize())
        selectCity()
        

def selectCity():
    while True:
        try:
            city_answer_input = int(input(Fore.YELLOW + "Select a city you would like to search: ")) - 1
            if city_answer_input >= 0 and city_answer_input <= len(config.avail_locations)-1:
                config.city_url = config.avail_locations[city_answer_input]['href']
                break
            else:
                print(Fore.RED + "Please enter a value within the range")
        except ValueError:
            print(Fore.RED + "Wrong")



def fetchLocations(region, region_area):
    response = requests.get("https://www.craigslist.org/about/sites")
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    a = soup.find('a' ,{'name': region})
    h2 = a.find_parent('h2')
    h2_strip = h2.get_text().strip()
    
    region_container = h2.find_next('div', class_='colmask')

    for h4 in region_container.find_all('h4'):
        if region_area != '':
            h4_v2 = h4.get_text().strip()
            config.avail_locations_regions.append(h4_v2)
            
            if h4.get_text().strip().lower() == region_area.lower():
                #print(h4)
                ul = h4.find_next('ul')
                for li in ul.find_all('li'):
                    a = li.find('a')
                    #print(a)
                    config.avail_locations.append({'name': a.text, 'href': a['href']})
        elif region_area == '':
            region_area = region
            h4_v2 = h4.get_text().strip()
            config.avail_locations_regions.append(h4_v2)



def handle_query():
    while True:
        try:
            query_input = str(input(Fore.YELLOW + "\nWhat would you like to look for today?: ")).strip()
            config.query = query_input
            break

        except ValueError:
            print("Invalid Query")


    

    
def all_together():
    first_time = 0

    while config.continue_search:
        try:
            if first_time == 0:
                craigslist.fetchPage(config.query, config.keep_looking_bottom, config.keep_looking_top)
                config.keep_looking_bottom+=3
                config.keep_looking_top+=3
                searching_input = int(input(Fore.YELLOW + "\nPress: \n1) Keep Searching  2) "
                                            +"Change Query  3)Change Price\n4) Change Location 5) Open in Browser  6) Stop Searching"
                                            +"\nAnswer Here: "))    
            else:
                searching_input = int(input("\n1)Continue  2)Switch Q 3)Switch P 4)Change Location 5)Open Browser  6)Stop: "))

            if searching_input == 1:
                craigslist.fetchPage(config.query, config.keep_looking_bottom, config.keep_looking_top)
                config.keep_looking_bottom+=3
                config.keep_looking_top+=3
            elif searching_input == 2:
                keepLooking()
            elif searching_input == 3:
                config.change_max_min_price = 'y'
                setting_price()
            elif searching_input == 4:
                city()
            elif searching_input == 5:
                    while True:
                                try:
                                    browser_index_input = int(input("Select the index of the listing "
                                                                    + "you would like to open in your browser: "))
                                    webbrowser.open(get_href_by_index(browser_index_input))
                                    break
                                except ValueError:
                                    print("Still working")
            elif searching_input == 6:
                config.continue_search = False
            first_time +=1
        except ValueError:
            print("Please enter a correct corresponding value!")
   

def keepLooking():
        while True:
            try:
                second_time = 0
                if second_time == 0:
                    switched_query_input = str(input("What would you like to switch to?: ")).lower()
                else:
                    switched_query_input == str(input("Try Again: "))
                confirm_input = str(input("\nAre you sure? (Press Y or N): ")).lower()
                not_confirmed = True
                if confirm_input == 'y':
                    config.query = switched_query_input
                    break
            except ValueError:
                print("Please enter valid values")
                                    
            config.query = config.switched_query
            config.keep_looking_bottom = 0
            config.keep_looking_top = 3
            config.looking_answer = 'y'

def get_href_by_index(index):
    for listing_group in config.json_listings:
        for listing in listing_group:
            if listing['index'] == index:
                return listing['href']
    return None






    

def all_marketplaces():
    #print(Back.BLACK)
    config.init()
    setting_price()
    #transport()
    city()
    handle_Region_Area(config.region)
    handle_query()
    all_together()


#MAIN CODE HERE
def main():
    pass
    

   
if __name__ == "__main__":
    main()
    





