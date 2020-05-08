from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

def getInfo(url, dump_filepath):
    start_page = 1

    cache = {
        'url': [],
        'description': [],
        'language': [],
        'tags': []
    }
    
    while True:
        r = requests.get(url+"?page={}".format(start_page), timeout=10)

        # Sleep 1 second so the website is not bombed by requests
        time.sleep(1)
        start_page += 1
        page = BeautifulSoup(r.text, "html.parser")
        repo_list= page.find('div', attrs={'class': 'org-repos repo-list'})

        # Find the repo 
        repo_list = repo_list.find_all('li')
        
        # Check if repos have run out
        if len(repo_list) == 0:
            print('Finished scraping')
            break

        for r in repo_list:
              
            repo_url = r.find('a', attrs={'class': 'd-inline-block', 'itemprop': 'name codeRepository'})['href'].split('/')[2]
            cache["url"].append(url+'/'+repo_url)

            description = r.find('p', attrs={'itemprop': 'description'})
            if description:
                cache["description"].append(remove_non_ascii(description.text).strip())
            else:
                cache["description"].append(None)
            
            lang = r.find('span', attrs={'itemprop': 'programmingLanguage'})
            if lang:
                cache["language"].append(lang.text)
            else:
                cache["language"].append(None)
            
            tags = r.find('div', attrs={'class': 'flex-items-center flex-wrap d-inline-flex col-9 f6 my-1'})
            if tags:
                tags = tags.find_all('a', attrs={'class': 'topic-tag topic-tag-link f6 my-1'})
                cache["tags"].append([t.text.strip() for t in tags])
            else:
                cache["tags"].append([None])

    return pd.DataFrame(cache).to_csv(dump_filepath)
 

if __name__ == "__main__":
    url ='https://github.com/github'
    getInfo(url, 'scrape/data/repositories.csv')
