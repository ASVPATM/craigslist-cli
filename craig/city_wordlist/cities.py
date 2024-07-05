

cities_full_list = []
cities_list = []
with open('city_wordlist/world-cities copy.csv', 'r') as all_cities:
    for line in all_cities:
        i = 0
        j = 0
        city = ''
        other = ''
        commacount = 0
        while line[j] != ',':
            other+=line[j]
            j+=1
        while commacount != 3:
            if line[i+1] == ',':
                commacount+=1
            city +=line[i]
    
            i+=1
        cities_list.append(other)
        cities_full_list.append(city)

def shorten_city_name(city):
    index = 0
    short = ''
    while city[index] != ',':
        short+=city[index]
        index +=1
    return short

