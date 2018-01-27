
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
import pymongo
import requests
import pandas as pd
import time
from datetime import datetime

# In[2]:


def init_browser():
    chrome_location = "C:\\Users\\ssank\\chromedriver_win32\\chromedriver.exe"
    chrome_location = chrome_location.replace("\\","/")
    executable_path = {"executable_path":chrome_location}
    
    return Browser("chrome", **executable_path, headless=False)


# In[3]:


def get_soup_object(url):
    browser = init_browser()
    browser.visit(url)
    soup = BeautifulSoup(browser.html,"html.parser")
    return soup


# In[4]:


def get_latest_NASA_news():
    NASA_MARS_url = "https://mars.nasa.gov/news/"
    news_soup = get_soup_object(NASA_MARS_url)
    latest_news = news_soup.find_all("div",{"class":"list_text"})[0]
    return {
        "title":latest_news.find("div",{"class":"content_title"}).text,
        "content":latest_news.find("div",{"class":"article_teaser_body"}).text
    }    


# In[5]:


def get_MARS_img():
    JPL_home_url = "https://www.jpl.nasa.gov"
    JPL_img_url = JPL_home_url+"/spaceimages/?search=&category=Mars"
    jpl_soup = get_soup_object(JPL_img_url)
    items = jpl_soup.find("div",{"class":"carousel_items"})
    img_title = items.find("h1",{"class":"media_feature_title"}).text
    featured_img = items.find("article")
    img_url = JPL_home_url+featured_img['style'].split(':')[1].split('\'')[1]
    return {
            "title":img_title,
            "img_url":img_url
           }


# In[6]:


def get_MARS_temperature():
    twitter_report_url = "https://twitter.com/marswxreport?lang=en"
    temp_soup = get_soup_object(twitter_report_url)
    return temp_soup.find("ol",{"id":"stream-items-id"}).find("li").find("p").text


# In[7]:


def get_MARS_facts():
    df = pd.read_html("https://space-facts.com/mars/")[0]
    df = df.rename(columns={0:"Description",1:"Value"})
    df = df.set_index("Description")
    return df.to_dict()['Value']


# In[13]:


def get_MARS_hemisphere_data():
    browser = init_browser()
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hms_soup = BeautifulSoup(browser.html,"html.parser")
    items = hms_soup.find("div",{"id":"product-section"}).find_all("div",{"class":"item"})

    hemisphere_data = []

    for item in items:
        img_main_url = "https://astrogeology.usgs.gov"+item.find("a")["href"]
        img_title = item.find("div",{"class":"description"}).find("a").find("h3").text
        browser.visit(img_main_url)
        time.sleep(1)
        img_soup = BeautifulSoup(browser.html,"html.parser")
        download_item = img_soup.find("div",{"class":"downloads"})
        hemisphere_item = {
            "title":img_title,
            "img_url": download_item.find("li").find("a")["href"]
        }
        hemisphere_data.append(hemisphere_item)
        
    return hemisphere_data
    


# In[14]:


def scrape():
    mars_news = get_latest_NASA_news()
    mars_img = get_MARS_img()
    mars_facts = get_MARS_facts()
    mars_temp = get_MARS_temperature()
    mars_hm_data = get_MARS_hemisphere_data()
    return {
        "date":datetime.now(),
        "news":mars_news,
        "featured_img":mars_img,
        "facts":mars_facts,
        "temperature":mars_temp,
        "hemisphere_data":mars_hm_data
    }
