import scrape


if __name__ == '__main__':
    scrape.cookiesPopup()
    chosen_categ = scrape.select_category()
    _,vals,_ = scrape.pick_all_per_page()
    manu,models,_,links = scrape.get_listed_items_links(vals)
    img_src = scrape.open_new_tabs(links,vals)
    scrape.download_pics(img_src,manu,models,chosen_categ)
