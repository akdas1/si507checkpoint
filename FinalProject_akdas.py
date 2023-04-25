import pandas as pd
import numpy as np
import requests
import webbrowser
import time
import json
import os

api_key = 'Enter API Key Here' # you do not need an API key since we are caching
# please input either Detroit or Ann Arbor in the command to get the cached data

class Food:
    '''Gets food data from the API and assigns attributes
    like name, latitude, longitude, address, price, yelp rating,
    and url.

    Instance Attributes
    -------------------
    name: string
        the name of the restaurant
    latitude: float
        the latitude location of the restaurant
    longitude: float
        the longitude location of the restaurant
    address: string
        the address of the restaurant
    price: string
        the price of the restaurant (1-4 dollar signs)
    rating: float
        the average rating of the restaurant
    type: string
        the type of restaurant
    url: string
        the yelp url of the restaurant
    json: string
        filepath to a json file'''
    def __init__(self, name="No Name", latitude="No Latitude",
                 longitude="No Longitude", address="No Address",
                 price="No Price", rating="No Rating", type="No Type",
                 url="No URL", json=None):
        if json == None:
            self.name = name
            self.latitude = latitude
            self.longitude = longitude
            self.address = address
            self.price = price
            self.rating = float(rating)
            self.type = type
            self.url = url
        else:
            self.name = json.get("name", "No Name")
            if isinstance(json["coordinates"], dict):
                self.latitude = json["coordinates"].get("latitude", "No Latitude")
                self.longitude = json["coordinates"].get("longitude", "No Longitude")
            else:
                self.latitude = "No Latitude"
                self.longitude = "No Longitude"
            self.address = json["location"].get("display_address", "No Address")
            self.price = json.get("price", "No Price")
            self.rating = float(json.get("rating", "No Rating"))
            if json["categories"]:
                self.type = json["categories"][0].get("title", "No Type")
            else:
                self.type = "No Type"
            self.url = json.get("url", "No URL")
    def info(self):
        '''
        Returns a string with the name, type, rating,
        and price of the restaurant'''
        return f"{self.name}, {self.type}, {self.rating}, {self.price}"


def get_map(latitude, longitude):
    '''
    Opens a web browser link to the input Google Maps location.

    Parameters
    ----------
    latitude: float
        The latitude location of the restaurant
    longitude: float
        The longitude location of the restaurant
    '''
    ## google maps uses latitude and longitude to search
    url = "https://www.google.com/maps/search/?api=1&query={},{}".format(latitude, longitude)
    webbrowser.open(url) # opens your web browser to the url

def get_api(term):
    '''
    Gets data from the Yelp API and returns a list of Restaurant
    data. Initially, it looks for a cache file. If it finds one,
    it'll load from that file. If not, it'll make a request to
    the API and save the data to a cache file. It'll also return
    50 restaurants at a time. Note, the API only allows 1000 search
    results, so this function will take a while to run. Caching
    should be faster.

    Parameters
    ----------
    term: string
        The city term for the API

    Returns
    -------
    restaurants: list
        A list of 50 Restaurants
    '''
    ## the cache file is named 'Ann_Arbor.json'
    # removes chance for error if user inputs Ann Arbor
    if term.lower() == 'Ann Arbor'.lower():
        term = 'Ann_Arbor'
    restaurants = []
    cache = f'{term}.json'
    filepath = os.getcwd() + '/' + cache
    print(filepath)
    ## check if cache file exists to load
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)['businesses']
        return [Food(json=r) for r in data] # returns a list of Food objects
    ## if cache file doesn't exist, make a request to the API
    else:
        headers = {
            "accept": "application/json",
            'Authorization': 'Bearer %s' % api_key}
        url = 'https://api.yelp.com/v3/businesses/search'
        for offset in range(0, 1000, 50):
            params = {'term': 'food', 'location': term, 'limit': 50, 'offset': offset}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            businesses = data['businesses']
            restaurants += businesses  # Appending new restaurants to the list
            with open(cache, 'w') as f:
                json.dump({'businesses': restaurants}, f)
        return [Food(json=r) for r in restaurants] # returns a list of Food objects

def get_types(restaurants):
    '''
    Gets a list of restaurants matching the input type.
    Appends the restaurants to a new list and returns it.
    If the list is too large, it'll only print the first 50.

    Parameters
    ----------
    restaurants: list
        a list of dictionaries of restaurants

    Returns
    -------
    new_restaurants: list
        a list of dictionaries of restaurants matching
        the input type
    '''
    new_restaurants = []
    next = input("Do you want to filter the type of food? (yes/no): ")
    ## keeps running until user inputs yes or no
    if next.lower() == 'yes':
        food_type = input("Enter a food type: ")
        for r in restaurants:
            if r.type.lower() == food_type.lower():
                new_restaurants.append(r)
        return new_restaurants
    elif next.lower() == 'no':
        return restaurants
    else:
        print("Invalid input. Please enter yes or no.")
        get_types(restaurants)

def get_rating(restaurants):
    '''
    Gets a list of restaurants matching the input rating.
    Appends the restaurants to a new list and returns it.
    If the list is too large, it'll only print the first 50.

    Parameters
    ----------
    restaurants: list
        a list of dictionaries of restaurants

    Returns
    -------
    new_restaurants: list
        a list of dictionaries of restaurants matching
        the input ratng
    '''
    new_restaurants = []
    next = input("Do you want to filter the rating? (yes/no): ")
    if next.lower() == 'yes':
        ## only takes specific floats, will keep asking until valid input
        while True:
            try:
                rating = float(input("Enter a rating: "))
                if rating >= 1 and rating <= 5:
                    for r in restaurants:
                        if r.rating >= float(rating):
                            new_restaurants.append(r)
                    return new_restaurants
                else:
                    print("Invalid input. Please enter a rating between 1 and 5. Decimals must be .0 or .5.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a float.")
                continue
    elif next.lower() == 'no':
        return restaurants
    ## keeps running until user inputs yes or no
    else:
        print("Invalid input. Please enter yes or no.")
        get_rating(restaurants)

def get_price(restaurants):
    '''
    Gets a list of restaurants matching the input price.
    Also checks if the input is valid and made of dollar signs.
    Appends the restaurants to a new list and returns it.
    If the list is too large, it'll only print the first 50.

    Parameters
    ----------
    restaurants: list
        a list of dictionaries of restaurants

    Returns
    -------
    new_restaurants: list
        a list of dictionaries of restaurants matching the input price'''
    new_restaurants = []
    next = input("Do you want to filter the price? (yes/no): ")
    if next.lower() == 'yes':
        while True:
            price = input("Enter a price: ")
            ## takes specific dollar sign amounts, will keep asking until valid input
            if price == '$' or price == '$$' or price == '$$$' or price == '$$$$':
                for i in restaurants:
                    if i.price == price:
                        new_restaurants.append(i)
                        return new_restaurants
            else:
                print("Invalid price. Please enter 1-4 dollar signs.")
                continue
    elif next.lower() == 'no':
        return restaurants
    ## keeps running until user inputs yes or no
    else:
        print("Invalid input. Please enter yes or no.")
        get_price(restaurants)

def final_step(final):
    '''
    Takes in a list and checks if it contains one or more restaurants.
    If the list contains one restaurant, it will print the final
    results and asks the user if they want to get directions to the
    restaurant. If it contains more than one restaurant, the user can
    choose which restaurant to get directions to. If the user enters yes,
    it'll call the get_map function to open a Google Maps link to the
    restaurant's location. If the user enters no, it'll end the session.
    If the user inputs a wrong value, it'll ask them to enter yes or no
    again.

    Parameters
    ----------
    final: list
        a list of dictionaries of restaurants

    Returns
    -------
    None
    '''
    print(' ')
    print('Final Results')
    print('---------------------------')
    ## prints the first 50 results
    for i, r in enumerate(final[:50]):
        print(f"{i}. {r.info()}")
    ## if 1, asks if user wants directions to the restaurant
    if len(final) == 1:
        while True:
            print(' ')
            answer = input("Would you like to get directions to this restaurant? (yes/no): ")
            if answer.lower() == 'yes':
                get_map(r.latitude, r.longitude)
                break
            elif answer.lower() == 'no':
                print(' ')
                print('Session Ended')
                time.sleep(1)
                quit()
            else:
                # only accepts yes or no
                print('Invalid input. Please enter yes or no.')
                continue
    ## if multiple, asks which restaurant they want directions to
    elif len(final) > 1:
        while True:
            print(' ')
            answer = input("Would you like to get directions to a restaurant? (yes/no): ")
            if answer.lower() == 'yes':
                directions = input('Enter the number of the restaurant you would like to get directions to: ')
                if directions.isdigit():
                    if int(directions) < len(final):
                        get_map(final[int(directions)].latitude, final[int(directions)].longitude)
                        break
                    else:
                        print('Invalid input. Please enter a valid number.')
                        continue
            elif answer.lower() == 'no':
                print(' ')
                print('Session Ended')
                time.sleep(1)
                quit()
            else:
                # only accepts yes or no
                print('Invalid input. Please enter yes or no.')
                continue

def webscrape(city):
    '''
    Takes in a city and scrapes a website for a list of top restaurants
    and their descriptions. It then returns a list of dictionaries
    containing the restaurant names and descriptions.

    Parameters
    ----------
    city: string
        a string of the city name

    Returns
    -------
    restaurants: list
        a list of dictionaries of top restaurants
    '''
    if city.lower() == 'Detroit'.lower():
        url = 'https://detroit.eater.com/maps/best-restaurants-detroit-38'
    elif city.lower() == 'Ann_Arbor'.lower():
        url = 'https://detroit.eater.com/maps/best-ann-arbor-restaurants'
    # get list of restaurants names and descriptions

def main():
    '''
    Main function that runs the program.

    Parameters
    ----------
    None
    '''
    print('To use cached data, enter Detroit or Ann Arbor. To use the API, add your own key at the top.')
    term = input("Enter a city: ")
    res = get_api(term)
    restaurants = []
    while True:
        ## if there are no city results or a typo, ask for input again
        if len(res) == 0:
            term = input("No results. Enter a city: ")
            res = get_api(term)
            continue
        ## user can choose to exit
        elif term.lower() == 'exit':
            print('Session Ended')
            time.sleep(1)
            quit()
        else:
            for r in res:
                restaurants.append(r)
            print(' ')
            print('Printing the first 50 of 1000 results')
            print('---------------------------')
            for r in restaurants[:50]:
                print(r.info())
        break
    while True:
        new_restaurants = get_types(restaurants)
        ## if there are no results or a typo, ask for input again
        if len(new_restaurants) == 0:
            print(' ')
            print('No results found. Please try again.')
            continue
        elif len(new_restaurants) == 1:
            ## if only one restaurant, jumps to final step
            final_step(new_restaurants)
            print('Session Ended')
            time.sleep(1)
            quit()
        else:
            ## ignores if the user doesn't want to filter by type
            if new_restaurants != restaurants:
                print(' ')
                print('Previewing up to 50 results')
                print('---------------------------')
                for r in new_restaurants[:50]:
                    print(r.info())
            break
    while True:
        new_restaurants1 = get_rating(new_restaurants)
        ## if there are no results or a typo, ask for input again
        if len(new_restaurants1) == 0:
            print(' ')
            print('No results found. Please try again.')
            continue
        elif len(new_restaurants1) == 1:
            ## if only one restaurant, jumps to final step
            final_step(new_restaurants1)
            print('Session Ended')
            time.sleep(1)
            quit()
        else:
            ## ignores if the user doesn't want to filter by rating
            if new_restaurants1 != new_restaurants:
                print(' ')
                print('Previewing up to 50 results')
                print('---------------------------')
                for r in new_restaurants1[:50]:
                    print(r.info())
            break
    while True:
        ## if there are no results or a typo, ask for input again
        final = get_price(new_restaurants1)
        if len(final) == 0:
            print(' ')
            print('No results found. Please try again.')
            continue
        else:
            break
    ## runs the final step
    final_step(final)
if __name__ == "__main__":
    main()