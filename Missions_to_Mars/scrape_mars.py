import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
from IPython.display import display_html

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    time.sleep(1)
    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')
    news_title = news_soup.find('div', class_='list_text').a.text
    news_paragraph = news_soup.find('div', class_='article_teaser_body').text

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')
    feat_img = img_soup.find('img', class_='main_image')['src']
    feat_img_url = f'https://www.jpl.nasa.gov{feat_img}'

    tweet_url = 'https://twitter.com/marswxreport'
    browser.visit(tweet_url)
    time.sleep(5)
    tweet_html = browser.html
    tweet_soup = bs(tweet_html, 'html.parser')
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
    
    table_url = 'https://space-facts.com/mars/'
    browser.visit(table_url)
    time.sleep(1)
    table_html = browser.html
    table_soup = bs(table_html, 'html.parser')
    table = table_soup.find('table', id='tablepress-p-mars')
    table_string = str(table)
    table_df = pd.read_html(table_string)
    table_df = table_df[0]
    facts_string = table_df.to_html(header=False, index=False)

    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(1)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')
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

    mars_info={
        'news_title':news_title,
        'news_paragraph':news_paragraph,
        'feat_img':feat_img_url,
        'weather':weather,
        'facts_data':facts_string,
        'hemispheres':images
    }

    browser.quit()

    return mars_info

