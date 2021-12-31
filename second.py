#!/home/rayon/.local/share/virtualenvs/web_scraping-VMHpI4Di/bin/python
import pandas as pd
from bs4 import BeautifulSoup
import requests

# header for https requests,as otherwise server doesn't respond with the html page
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def all_data():
    data = []
    for i in range(1, 12):  # total pages on site are 11
        response = requests.get(
            "https://www.yoshops.com/products?page="+str(i), headers=head)

        soup = BeautifulSoup(response.text, "html.parser")

        # adding all html elements with clas product to data list.
        data += soup.select(".product")

    # little bit of cleaning of data
    refined_data = []  # data after processing will be saved here
    for i in data:
        link = "https://www.yoshops.com/"+i.select_one(".product-link")["href"]
        title = i.select_one(".product-title").get_text()
        temp = i.select_one(".product-price").get_text().split("₹")
        old_price = temp[1]
        new_price = temp[2]
        refined_data.append([link, title, old_price, new_price])

    # saving data
    df = pd.DataFrame(refined_data)
    df.columns = ["link", "title", "old_price", "new_price"]
    df.to_excel("data.xlsx")


def given_product(link):
    response = requests.get(link, headers=head)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.select_one("#product-name").get_text()
    regular_price = soup.select_one("#regular-price").get_text()[1:]
    sale_price = soup.select_one("#sale-price").get_text()[1:]
    description = soup.select_one(".single-product-description").get_text()
    print("\n")
    print("title:                ", title)
    print("regular price:        ", regular_price)
    print("sale price            ", sale_price)
    print("\n\n")
    print("product description: \n\n", description.strip())
    print("\n")
    df = pd.DataFrame([[title, regular_price, sale_price, description]])
    df.columns = ["title", "regular_price", "sale_price", "description"]
    df.to_excel(title+".xlsx")


link = input("enter the url: ").strip()
home_links = ["https://www.yoshops.com",
              "https://www.yoshops.com/",
              "https://www.yoshops.com/products",
              "https://www.yoshops.com/products/"]
if link in home_links:
    all_data()
    print("data.xlsx file created in current folder")
else:
    given_product(link)
