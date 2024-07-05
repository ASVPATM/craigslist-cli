from Cities import cities_retriever
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
sys.path.append('cli/city_wordlist')
sys.path.append('cli/websites')
from website import craigslist
from city_wordlist import cities

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
    while True:
        try:
            max_min_answer = str(input("\nDo You Want To Set a Maximum/Minimum Price?\n (PRESS Y OR N): ")).lower().strip()
            if max_min_answer == 'y' or max_min_answer == 'n':
                answer = max_min_answer
                break
            else:
                print("Invalid Number, Please Select between 1 or 2")
                print(str(attempts) + " Attempts Left")
                attempts-=1
                if attempts <= 0:
                    break
        except ValueError:
            print("Invalid Input, Please Enter a Number") 
    while True:
        if answer == 'y':
            try:
                min_price_answer = int(input("Min: "))
                max_price_answer = int(input("\nMax: "))
                if min_price_answer >= 0 and min_price_answer <= max_price_answer:
                    config.min_price = min_price_answer
                    config.max_price = max_price_answer
                    break
                else:
                    print("Make sure to enter valid values for the maximum/minimum. The minimum should be > 0 and <= maximum")
            except ValueError:
                print("Enter Integer Values Only")
        else:
            break

def city():
        while True:
            try:
                nearest_city_answer = str(input("\nName the closest/largest city to you: ")).lower().strip()
                city_close_matches = difflib.get_close_matches(nearest_city_answer, cities.cities_list)

                if len(city_close_matches) != 0:
                    number = 1
                    for x in range(0, len(cities.cities_list)):
                        if unidecode(cities.cities_list[x]).lower().strip() == nearest_city_answer:
                            print (str(number) + ") " + cities.cities_full_list[x])
                            config.indexes.append(x)
                            number+=1
                    if number != 1:
                        break
                    else:
                        print("Not a Valid City")  
                
            except ValueError:
                print("WRONG")
        while True:
            try: 
                
                actual_city_answer = int(input("\nSelect a number based on your actual city: "))
                config.city_number = actual_city_answer
                if actual_city_answer >= 1 and actual_city_answer <= len(city_close_matches):
                    config.actual_city = cities.cities_list[config.indexes[config.city_number-1]]
                    break
                else:
                    print("Please select a value within the range shown")
            except ValueError:
                print("Enter Integer Values Only")



def handle_query():
    while True:
        try:
            query_input = str(input("\nWhat would you like to look for today?: ")).strip()
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
                searching_input = int(input("\nPress: \n1) Keep Searching\n2) "
                                            +"Change Query\n3) Open in Browser\n4) Stop Searching"
                                            +"\nAnswer Here: "))    
            else:
                searching_input = int(input("\n1)Continue  2)Switch  3)Open Browser  4)Stop: "))

            if searching_input == 1:
                craigslist.fetchPage(config.query, config.keep_looking_bottom, config.keep_looking_top)
                config.keep_looking_bottom+=3
                config.keep_looking_top+=3
            elif searching_input == 2:
                keepLooking()
            elif searching_input == 3:
                    while True:
                                try:
                                    browser_index_input = int(input("Select the index of the listing you "
                                                                    + "you would like to open in your browser: "))
                                    webbrowser.open(get_href_by_index(browser_index_input))
                                    break
                                except ValueError:
                                    print("Still working")
            elif searching_input == 4:
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





def switch():
    pass
    
def specific_marketplaces():
    config.init()
    

def all_marketplaces():
    config.init()
    setting_price()
    city()
    handle_query()
    all_together()


#MAIN CODE HERE
def main():
    pass
    
    

   
def commentedOutCode():
    pass
    # while config.looking_answer == 'y':
    #     if config.transport_method == 1:
    #         craigslist.fetchPage(config.query, config.keep_looking_bottom, config.keep_looking_top)
    #         search_until_stop()
    #     elif config.transport_method == 2:
    #         offerup
            
    #     config.keep_looking_bottom+=3
    #     config.keep_looking_top+=3
    # if config.looking_answer == 'switch':
    #     craigslist.fetchPage(c)


    # if config.looking_answer == 'n':
    #     while True:
    #         try:
    #             change_query_or_stop_input = str(input("Would you like to: \n1)Change Query\n2)Stop Searching\n\nPlease" 
    #                                                    +"Select an Answer"))
    #         except ValueError:
    #             pass    
     # while config.continue_search:
    #     if config.looking_answer == 'y':
    #         craigslist.fetchPage(config.query, config.keep_looking_bottom, config.keep_looking_top)
    #         config.keep_looking_bottom+=3
    #         config.keep_looking_top+=3
    #     elif config.looking_answer == 'switch':
    #         config.query = config.switched_query
    #         config.keep_looking_bottom = 0
    #         config.keep_looking_top = 3
    #         config.looking_answer = 'y'
    #     elif config.looking_answer == 'n':
    #         config.continue_search = False
        
        # while True:
        #     try:
        #         searching_input = int(input("\nPress: \n1) Keep Searching\n2) "
        #                                     +"Change Query\n3) Stop Searching"
        #                                     +"\nAnswer Here: "))
        #         print(searching_input)
        #         if searching_input == 1:
        #             config.looking_answer = 'y'
        #             break
        #         elif searching_input == 2:
        #             config.looking_answer == 'switch'
        #             break
        #         elif searching_input == 3:
        #             config.looking_answer == 'n'
        #             break
        #     except ValueError:
        #         print("Enter a Correct Value Please")

        # while True:
                #     try:
                #         second_time = 0
                #         if second_time == 0:
                #             switched_query_input = str(input("What would you like to switch to?: ")).lower()
                #         else:
                #             switched_query_input == str(input("Try Again: "))
                #         confirm_input = str(input("\nAre you sure? (Press Y or N): ")).lower()
                #         not_confirmed = True
                #         if confirm_input == 'y':
                #             switched_query_input = config.query
                #             break
                #     except ValueError:
                #         print("Please enter valid values")
                                
                # config.query = config.switched_query
                # config.keep_looking_bottom = 0
                # config.keep_looking_top = 3
                # config.looking_answer = 'y'
        # def search_until_stop():
    #     if config.looking_answer == 'n':
    #         return
    #     if config.looking_answer == 'switch':

    #     keep_searching_input = str(input("To continue searching, press y, otherwise press n")).lower()
    #     while True:
    #         try:
    #             keep_searching_input = str(input("\nTo continue searching, press y, otherwise press n: ")).lower()
    #             if keep_searching_input == 'y' or keep_searching_input == 'n':
    #                 config.looking_answer = keep_searching_input
    #                 break
    #             else:
    #                 print("Please select an answer between Y or N")
    #         except ValueError:
    #             print("Enter Correct Values Only Please") 

    # from pkg_resources import resource_string
    #      import json

    # cities_data = resource_string('world_cities', 'data/world-cities_json.json').decode('utf-8')
    #    cities = json.loads(cities_data)

    # print(cities[0])

    #actual_city_answer = 0
    # city_number = 0
    # city_full_name = ''
    # indexes = []
    # actual_city = ''

    #ASK IF THEY WANT LOCAL, SHIPPING OR BOTH


   
if __name__ == "__main__":
    main()
    
    
   





#def  

    






