import requests as rq
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import os

pics_folder_path = 'C:\\Users\\Cristian-Eduard\\Desktop\\CODE\\Guitarus\\pics'
 
# SELENIUM
options = Options()
options.add_experimental_option("detach",True)
options.add_argument('--headless')
browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
browser.get('https://www.thomann.de/ro/chitare_electrice.html')
 
def cookiesPopup():
    #Wait for the Popup to emerge
    browser.implicitly_wait(10)
    #Find the "Accept cookies" button and click it
    browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[2]/button[1]').click()
 
def return_main_categs():
    categories = browser.find_elements(By.CSS_SELECTOR,'.fx-category-grid')
    print(len(categories))
    categ_names = []
    for i in categories:
        categ_names.append(i.text)
    categ_names = categ_names[0].split('\n')
    return categ_names
 
def show_categories(categ=return_main_categs()):
    categ_no = []
    categ_title = []
    for i,val in enumerate(categ):
        print(i,'. ',val)
        categ_no.append(i)
        categ_title.append(val)
    return categ_no,categ_title
 
def select_category(categ_title = show_categories()[1]):
    categ_input = int(input('\nSelect the number of the category you want to see: '))
    print('Showing the '+categ_title[categ_input]+' subcategory.\n')
    browser.implicitly_wait(5)
    browser.find_element(By.LINK_TEXT,categ_title[categ_input]).click()
    chosen_categ = categ_title[categ_input]
    return chosen_categ

def pick_all_per_page():
    items = browser.find_elements(By.CLASS_NAME,'fx-product-list-entry')
    #print(items,'\n',len(items),'\n') #WebElements list[][] and length
    item_val = []
    item_index = []
    for i,val in enumerate(items):
        print("INDEX ITEM: ",i,"\nVALOARE ITEM: \n",val.text,'\n')
        item_val.append(val.text)
        item_index.append(i)
    return item_index,item_val,items

def get_listed_items_links(vals):
    browser.implicitly_wait(5)
    just_item_titles = []
    for i in vals:
        just_item_titles.append(i.split('\n'))
    #print(just_item_titles,'\n\n') 

    #Get all manufacturers on the page
    manufacturers = []
    span_brandName = browser.find_elements(By.CLASS_NAME,'title__manufacturer')
    for i,val in enumerate(span_brandName):
        manufacturers.append(span_brandName[i].text)
    print(manufacturers,'\n\n') 

    #Get all models on the page
    models = []
    span_model = browser.find_elements(By.CLASS_NAME,'title__name')
    for i,val in enumerate(span_model):
        models.append(span_model[i].text)
    print(models,'\n\n') 

    #Get model name links
    listed_item = []
    links = []
    for i,val in enumerate(models):
        item = browser.find_elements(By.PARTIAL_LINK_TEXT,models[i])
        listed_item.append(item)
        link = browser.find_elements(By.PARTIAL_LINK_TEXT,models[i])[0]
        links.append(link.get_attribute('href'))
    print(listed_item,'\n\n',links,'\n\n')
    return manufacturers,models,listed_item,links

def open_new_tabs(links,vals):
    #Open links in new tabs \\
    #switches to new tab    \\
    #finds image            \\
    #appends to img_src list\\
    img_src = []
    for i,val in enumerate(links):
        print('\n\n',i,'\n',val,'\n\n')
        browser.execute_script("window.open();")
        browser.switch_to.window(browser.window_handles[i])
        browser.get(links[i])
        browser.find_element(By.CSS_SELECTOR,'body > div.thomann-page.thomann-page-ro.fx-page > div > div.thomann-content.thomann-content-module-prod.thomann-content-route-main > div > div > div.fx-container.fx-container--with-margin.fx-product-orderable.product-main-content.fx-content-product-grid__col > div > div.fx-grid__col.fx-col--12.fx-col--lg-8 > div.product-media-gallery.product-media-gallery--type-defaultimage > div.spotlight.js-product-media-gallery-spotlight.fx-media-zoom-gallery.fx-media-zoom-gallery--skin-inline.zgZoomGallery.DefaultImage > div > div > div > div.zgItem.DefaultImage.zgStateSeen > div > picture > img').click()
        img_src.append(browser.find_element(By.CSS_SELECTOR,'body > div.thomann-page.thomann-page-ro.fx-page > div > div.thomann-content.thomann-content-module-prod.thomann-content-route-main > div > div > div.fx-container.fx-container--with-margin.fx-product-orderable.product-main-content.fx-content-product-grid__col > div > div.fx-grid__col.fx-col--12.fx-col--lg-8 > div.product-media-gallery.product-media-gallery--type-defaultimage > div.spotlight.js-product-media-gallery-spotlight.fx-media-zoom-gallery.fx-media-zoom-gallery--skin-inline.zgZoomGallery.DefaultImage > div > div > div > div.zgItem.DefaultImage.zgStateSeen > div > picture > img').get_attribute('src'))
    print("************IMAGE SOURCE img_src IS:************ \n\n",img_src,'\n')
    return img_src

def download_pics(img_src,manufacturers,models,chosen_categ):
    #Creates the location where the images get saved
    new_fold_path = pics_folder_path+'\\'+chosen_categ
    try:
        os.mkdir(os.path.join(os.getcwd(),pics_folder_path))
        os.mkdir(os.path.join(os.getcwd(),new_fold_path))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(),new_fold_path))

    #Creates the image names
    pic_name = []
    for i,j in zip(manufacturers,models):
        pic_name.append(i+' '+j)

    #Write the images in the 'pics' folder
    for i_src,pic in zip(img_src,pic_name):
        with open(pic + '.jpg','wb') as f:
            if pic:
                pass
            else:
                f.write(rq.get(i_src).content)
                print('Writing:\t',pic)



#TODO:
# --- automate the creation of folders by subcategory
# --- scrape ALL under selected subcateg.
# --- check for duplicates 
# --- MAYBE download all the photos of one given product + create a folder for each product


