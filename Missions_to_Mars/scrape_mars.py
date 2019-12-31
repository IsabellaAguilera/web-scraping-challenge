# Dependencies
import os
import pandas as pd
import requests as req
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape():
    time.sleep(5)
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', chrome_options=options,**executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, "html.parser")

    # Mars News

    
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Mars Images

    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url)
    image_html = browser.html
    soup = bs(image_html, 'html.parser')

    base_url = 'https://www.jpl.nasa.gov'
    image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    full_image_url = base_url + image_url

    # Mars Weather

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    weather_html = browser.html
    soup = bs(weather_html,'html.parser')

    recent_tweets = soup.find_all('div', class_='js-tweet-text-container')

    for tweet in recent_tweets: 
        weather_tweet = tweet.find('p').text
        if 'InSight' and 'sol' in weather_tweet:
            mars_weather_tweet = weather_tweet
            break
        else: 
            pass

    # Mars Facts

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    table = pd.read_html(facts_url)
    facts_table = table[0]

    facts_table.columns = ['Fact Description','Value']
    facts_table = facts_table.set_index('Fact Description')

    facts_html = facts_table.to_html('mars_table.html')

    # Mars Hemispheres

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    hemispheres_html = browser.html
    soup = bs(hemispheres_html, 'html.parser')

    items_url = soup.find_all('div', class_='item')
    hemi_image_urls = []

    base_url = 'https://astrogeology.usgs.gov'

    for item in items_url: 
        title = item.find('h3').text
        image_url = item.find('a', class_='itemLink product-item')['href'] 
        browser.visit(base_url + image_url)
        image_html = browser.html
        soup = bs(image_html, 'html.parser')
        full_url = base_url + soup.find('img', class_='wide-image')['src'] 
        hemi_image_urls.append({"title" : title, "img_url" : full_url})

        mars_data = {
            "news_title": news_title,
            "news_description": news_p,
            "featured_image_url": full_image_url,
            "weather": mars_weather_tweet,
            "facts": facts_html,
            "hemispheres_images": hemi_image_urls
        }

    

    return mars_data

if __name__ == '__main__':
    scrape()







