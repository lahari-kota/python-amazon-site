import csv
import requests
from bs4 import BeautifulSoup
import time

def getProductInformation(pageUrl, headers,productsData):
    response = requests.get(pageUrl, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        product_list = soup.find_all("div", {"data-component-type": "s-search-result"})

        for product in product_list:
            productUrl = "https://www.amazon.in" + product.find("a", {"class": "a-link-normal"})["href"]
            productName = product.find("span", {"class": "a-text-normal"}).text.strip()
            productPrice = product.find("span", {"class": "a-offscreen"}).text.strip()

            productRating = product.find("span", {"class": "a-icon-alt"})
            if productRating:
                productRating = productRating.text.split()[0]
            else:
                productRating = "Not available"

            productReviews = product.find("span", {"class": "a-size-base", "dir": "auto"})
            if productReviews:
                productReviews = productReviews.text
            else:
                productReviews = "0"
            print("=====================================================")
            print("Product Name:", productName)
            print("Product Price:", productPrice)
            print("productRating:", productRating)
            print("Number of Reviews:", productReviews)
            print("Product URL:", productUrl)
            print("=====================================================")
            print("\n")

            productsData.append({
              "Product Name": productName,
              "Product Price": productPrice,
              "productRating": productRating,
              "Number of Reviews": productReviews,
              "Product URL": productUrl
            })

            getNewDataOfProducts(productUrl, headers,productsData)
            time.sleep(3)

    else:
        print("Failed to fetch the page:", response.status_code)

def getNewDataOfProducts(productUrl, headers, productsData):
    response = requests.get(productUrl, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("span", {"id": "productTitle"})
        if title:
            description = title.text.strip()
        else:
            description = "Not available"

        htmlASIN = soup.find("th", string="ASIN")
        if htmlASIN:
            asin = htmlASIN.find_next_sibling("td").text.strip()
        else:
            asin = "Not available"

        productDescriptionDiv = soup.find("div", {"id": "productDescription"})
        if productDescriptionDiv:
            productDesc = productDescriptionDiv.text.strip()
        else:
            productDesc = "Not available"

        htmlManufacturer = soup.find("a", {"id": "bylineInfo"})
        if htmlManufacturer:
            manufacturer = htmlManufacturer.text.strip()
        else:
            manufacturer = "Not available"
        print("=====================================================")
        print("Description:", description)
        print("ASIN:", asin)
        print("Product Description:", productDesc)
        print("Manufacturer:", manufacturer)
        print("=====================================================")
        print("\n")
        productsData[-1]["Description"] = description
        productsData[-1]["ASIN"] = asin
        productsData[-1]["Product Description"] = productDesc
        productsData[-1]["Manufacturer"] = manufacturer

    else:
        print("Failed to fetch the product page:", response.status_code)
        print('\n')

def getProductFromAmazon(url, pageCount, headers, productsData):
    for page in range(1, pageCount + 1):
        print("Scraping page", page)
        pageUrl = url + "&page=" + str(page)
        getProductInformation(pageUrl, headers, productsData)
        time.sleep(3)

def export_to_csv(productsData, outputFile):
    with open(outputFile, mode='w', newline='', encoding='utf-8') as csvfile:
        attributes = ["Product Name", "Product Price", "productRating", "Number of Reviews", "Product URL", "Description", "ASIN", "Product Description", "Manufacturer"]
        writer = csv.DictWriter(csvfile, fieldnames=attributes)
        writer.writeheader()
        writer.writerows(productsData)


if __name__ == "__main__":
    url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
    pagesToScrape = 20

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    productsData = []

    getProductFromAmazon(url, pagesToScrape, headers, productsData)

    outputFile = "amazon_products_data.csv"
    export_to_csv(productsData, outputFile)