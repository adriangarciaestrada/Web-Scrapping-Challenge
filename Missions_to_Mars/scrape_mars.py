#Import Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
from IPython.display import display_html

#Funtion to initialize the browser
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#Function to make all of the scrapping
def scrape_info():
    browser = init_browser()

    ##News Scrapping
    #Defines the url from which the information is obtained
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    #The browser accesses the desired site and wait for it to load the complete information
    browser.visit(news_url)
    time.sleep(1)
    #The site's html is loaded into a variable
    news_html = browser.html
    #Beautiful soup and html parser are used to sort the information
    news_soup = bs(news_html, 'html.parser')
    #Finds the first news and stores the title and the paragraph
    news_title = news_soup.find('div', class_='list_text').a.text
    news_paragraph = news_soup.find('div', class_='article_teaser_body').text
    
    ##Featured Image Scrapping
    #Defines the url from which the image is obtained
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #The browser accesses the desired site and wait for it to load the complete information
    browser.visit(img_url)
    time.sleep(1)
    #The instruction is given to click on a text to see the full image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    #The instruction is given to click on a text to see the full image
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    #The site's html is loaded into a variable
    img_html = browser.html
    #Beautiful soup and html parser are used to sort the information
    img_soup = bs(img_html, 'html.parser')
    #Finds the featured image and gets the url
    feat_img = img_soup.find('img', class_='main_image')['src']
    feat_img_url = f'https://www.jpl.nasa.gov{feat_img}'

    ##Tweet Scrapping
    #Defines the url from the Mars weather report twitter page
    tweet_url = 'https://twitter.com/marswxreport'
    #The browser accesses the desired site and wait for it to load the complete information
    browser.visit(tweet_url)
    time.sleep(5)
    #The site's html is loaded into a variable
    tweet_html = browser.html
    #Beautiful soup and html parser are used to sort the information
    tweet_soup = bs(tweet_html, 'html.parser')
    #Finds the latest tweet with the Mars weather report
    tweets = tweet_soup.find_all('div', {'data-testid':'tweet'})
    weather = ""
    for t in tweets:
        spans = t.find_all('span')
        for s in spans:
            text = s.get_text()
            if 'InSight' in text:
                weather = text
                break
            if weather != "":
                break
    
    ##Table Scrapping
    #Defines the url from which the information is obtained
    table_url = 'https://space-facts.com/mars/'
    #The browser accesses the desired site and wait for it to load the complete information
    browser.visit(table_url)
    time.sleep(1)
    #The site's html is loaded into a variable
    table_html = browser.html
    #Beautiful soup and html parser are used to sort the information
    table_soup = bs(table_html, 'html.parser')
    #Finds the table with information about Mars and stores the html of that table
    table = table_soup.find('table', id='tablepress-p-mars')
    table_string = str(table)
    table_df = pd.read_html(table_string)
    table_df = table_df[0]
    facts_string = table_df.to_html(header=False, index=False)

    ##Hemispheres Images Scrapping
    #Defines the url from which the information is obtained
    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #The browser accesses the desired site and wait for it to load the complete information
    browser.visit(hemisphere_url)
    time.sleep(1)
    #The site's html is loaded into a variable
    hemisphere_html = browser.html
    #Beautiful soup and html parser are used to sort the information
    hemisphere_soup = bs(hemisphere_html, 'html.parser')
    #Finds all of the images of the Mars hemispheres and displays the url of each image
    links = hemisphere_soup.find('div', class_='collapsible results')
    links = links.find_all('div', class_='item')
    images =[]
    for link in links:
        text = link.find('h3').text
        browser.click_link_by_partial_text(text)
        time.sleep(1)
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        image_url = image_soup.find('a', string='Sample')['href']
        image_dict = {'title':text,'img_url':image_url}
        images.append(image_dict)
        browser.back()

    #Creates a dictionary to store the scrapped information
    mars_info={
        'news_title':news_title,
        'news_paragraph':news_paragraph,
        'feat_img':feat_img_url,
        'weather':weather,
        'facts_data':facts_string,
        'hemispheres':images
    }

    #Closes the browser
    browser.quit()

    #Returns the dictionary with the scrapped information
    return mars_info

