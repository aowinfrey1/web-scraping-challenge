# imports
# import splinter, beautifulsoup and chrome driver
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
# scrape all function
def scrape_all():
    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #goal is to return json with all the data, so it can be loaded into MongoDB

    #get info from the news page
    news_title, news_p = scrape_news(browser)

    # build dictionary using info from scrapes
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_p,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    # stop webdriver
    browser.quit()

    #display output
    return marsData

# scrape mars news page
def scrape_news(browser): 
    # go to Mars Nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert browser html into soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    
    # grab title
    news_title = slide_elem.find('div', class_='content_title').get_text()

    # grab paragraph
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text() 

    #return title and news paragraph
    return news_title, news_p

# scrape through featured image page
def scrape_feature_img(browser):
    #visit url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # find full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    #parse resulting html with soup
    html = browser.html
    image_soup = soup(html, 'html.parser')

    #find image url
    img_url_rel = image_soup.find('img', class_='fancybox-image').get('src')

    #use base url to create absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    #return image url
    return img_url

# scrape through facts page
def scrape_facts_page(browser):
    url = 'https://galaxyfacts-mars.com/'
    #browser.visit(url)
    tb=pd.read_html(url)
    table=tb[1]
    table.to_html()

    html = browser.html
    fact_soup = soup(html, 'html.parser')

    #facts location
    #factsLocation = fact_soup.find('div', class_="diamgram mt-4")
    #factsTable = factsLocation.find('table') # grab the html code for table

    #create empty string
    facts = ""

    #add text to empty string then return
    #facts += str(factsTable)

    return facts


# scrape through hemispheres pages
def scrape_hemispheres(browser):
    #base url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []
    #set up loop
    for i in range(4):
        #loops through each page
        #hemisphere info dictionary
        hemisphereInfo = {}
        
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo["img_url"] = sample['href']
        
        # Get Hemisphere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphereInfo)
        
        # Finally, we navigate backwards
        browser.back()
        
    #return hemisphere urls with titles
    return hemisphere_image_urls
    




# set up as flask app
if __name__ == "__main__":
    print(scrape_all())