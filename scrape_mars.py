# Import module

import os
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import Browser
import cssutils


# Initialize browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

# Create a dictionary
mars_info_dict = {}

# NASA Mars News

def scrape_mars_news():
    try:
        # Initialize browser
        browser = init_browser()

        # # use splinter to access web page
        news_url = "https://mars.nasa.gov/news/"
        browser.visit(news_url)
        html = browser.html
        news_soup = bs(html, "html.parser")
        news_title = news_soup.find("div", class_="content_title").find("a").text
        news_paragraph = news_soup.find("div", class_="article_teaser_body").text
        print(news_title)
        print(news_paragraph)
        mars_info_dict["news_title"] = news_title
        mars_info_dict["news_paragraph"] = news_paragraph
        return mars_info_dict
    
    finally:
        browser.quit()

# JPL Mars Space Images - Featured Image

def scrape_mars_featured_image ():
    try:
        browser = init_browser()

        image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)
        image_html = browser.html
        image_soup = bs(image_html, "html.parser")
        image_soup_style = image_soup.find("article")["style"].replace("background-image: url('", "").replace("');", "")
        print(image_soup_style)
        source_url = 'https://www.jpl.nasa.gov'
        featured_image_url = source_url + image_soup_style
        print(featured_image_url)
        mars_info_dict ["mars_featured_image"] = featured_image_url

        return mars_info_dict
    finally:
        browser.quit()


# ### Mars Weather

def scrape_mars_weather():
    try:
        browser = init_browser()
        weather_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(weather_url)
        html_weather = browser.html
        soup = bs(html_weather,'html.parser')

        # Find the elements that contain tweets
        tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Search entries that shows weather related posts to exclude non-weather tweets
        for tweet in tweets:
            mars_weather = tweet.find('p').text
            if 'Sol' and 'pressure' in mars_weather:
                print(mars_weather)
                break
            else:
                pass
        mars_info_dict["mars_weather"] = mars_weather
        return mars_info_dict
    finally:
        browser.quit() 

# Mars Facts

def scrape_mars_facts():
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    tables
    df = tables[0]
    df.columns = ["Description", "Values"]
    df.set_index("Description", inplace=True)
    html_table = df.to_html()
    mars_info_dict ["mars_data"] = html_table
    return mars_info_dict
    
# ### Mars Hemispheres

# Retrieve url for the high resolution url
def scrape_mars_hemisphere():
    try: 
        browser = init_browser()
        hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hem_url)
        hem_html = browser.html
        hem_soup = bs(hem_html, "html.parser")
        hemisphere_image_url = []
        all_hem = hem_soup.find_all("div", class_="item")
        main_url = "https://astrogeology.usgs.gov/"

        for hem in all_hem:
            title = hem.find("img", class_="thumb")["alt"]
            partial_img_url = hem.find("a", class_="itemLink product-item")["href"]
        #     print(f"{main_url}{partial_img_url}")

        # Retrieve image 
            browser.visit(f"{main_url}{partial_img_url}")
            indiv_img_html = browser.html
            indiv_img_soup = bs(indiv_img_html, "html.parser")
            indiv_partial_img_url = indiv_img_soup.find("img", class_="wide-image")["src"]
            img_url = main_url + indiv_partial_img_url
        #     print(indiv_partial_img_url)
            print (img_url)
            hemisphere_image_url.append({"title": title, "img_url": img_url})
        
        mars_info_dict["hemisphere_image_url"] = hemisphere_image_url

        return mars_info_dict
    finally:
        browser.quit()







