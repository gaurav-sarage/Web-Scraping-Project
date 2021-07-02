# Web Scraping Project using requests, BeautifulSoup and pandas.
import requests
from bs4 import BeautifulSoup
import pandas

headers = {'user-agent': 'Mozilla/70.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

oyo_url = 'https://www.oyorooms.com/hotels-in-pune/?page='
page_num_MAX = 6
scraped_info_list = []

for page_num in range(1, page_num_MAX):
    req = requests.get(oyo_url + str(page_num), verify=True, headers=headers) #requesting for url
    content = req.text #from request we'll extract the content
    print(content)

    soup = BeautifulSoup(content,"html.parser")
    all_hotels = soup.find_all("div", {"class" : "hotelCardListing"})

    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict["name"] = hotel.find("h3", {"class": "listingHotelDescription__hotelName"}).text
        hotel_dict["address"] = hotel.find("span", {"itemprop" : "streetAddress"}).text
        hotel_dict["price"] = hotel.find("span", {"class" : "listingPrice__finalPrice"}).text
        # using try and except
        try:
            hotel_dict["rating"] = hotel.find("span", {"class" : "hotelRating__ratingSummary"}).text
        except AttributeError:
            pass

        parent_amenities_element = hotel.find("div", {"class" : "amenityWrapper"})

        amenities_list = []
        for amenity in parent_amenities_element.find_all("div", {"class" : "amenityWrapper__amenity"}):
            amenities_list.append(amenity.find("span", {"class" : "d-body-sm"}).text.strip())

        hotel_dict["amenities"] = ', '.join(amenities_list[:-1])

        scraped_info_list.append(hotel_dict)


dataFrame = pandas.DataFrame(scraped_info_list)
dataFrame.to_csv("Oyo.csv")
