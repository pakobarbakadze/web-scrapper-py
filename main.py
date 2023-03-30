import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

from top_restaurants import top_restaurants
from node import Node


def main():
    fetch_data('https://www.goldenpages.ie/q/business/advanced/where/Dublin/what/Hotels/', 5, "hotels")


def fetch_data(url: int, pages_number: int, lead_name: str):
    leads = []
    start = time.time()
    for i in range(1, pages_number):
        home_response = requests.get(
            f"{url}{i if i > 1 else ''}")
        home_soup = BeautifulSoup(home_response.text, "html.parser")

        listing_containers = home_soup.findAll("div", class_="listing_container")

        for listingContainer in listing_containers:
            new_node = Node(listingContainer, "a", "listing_title_link")
            title = new_node.get_text().strip().split(" ", 1)[1]

            if any(x in title for x in top_restaurants):
                continue

            new_node = Node(listingContainer, "a", "link_listing_number")
            number = new_node.get_text()

            new_node = Node(listingContainer, "div", "listing_address")
            address = new_node.get_text()

            new_node = Node(listingContainer, "a", "listing_title_link")
            link = new_node.get_link()

            details_response = requests.get(f"https://www.goldenpages.ie{link}")
            details_soup = BeautifulSoup(details_response.text, "html.parser")

            new_node = Node(details_soup, "div", "details_contact_other col_item width_2_4")
            email = new_node.get_email()

            leads.append([title, number, address, email])

    df = pd.DataFrame(leads, columns=["Title", "Number", "Address", "Email"])
    df.to_csv(f"{lead_name}.csv")
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()
