from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
print(pd.__version__)
print(requests.__version__)


def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

def getInfo(url, dump_filepath):
    start_page = 1

    repo_url_cache = []
    description_cache = []
    lang_cache = []
    tags_cache = []
    
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
            repo_url_cache.append(url+'/'+repo_url)

            description = r.find('p', attrs={'itemprop': 'description'})
            if description:
                description_cache.append(remove_non_ascii(description.text).strip())
            else:
                description_cache.append(None)
            
            lang = r.find('span', attrs={'itemprop': 'programmingLanguage'})
            if lang:
                lang_cache.append(lang.text)
            else:
                lang_cache.append(None)
            
            tags = r.find('div', attrs={'class': 'flex-items-center flex-wrap d-inline-flex col-9 f6 my-1'})
            if tags:
                tags = tags.find_all('a', attrs={'class': 'topic-tag topic-tag-link f6 my-1'})
                tags_cache.append([t.text.strip() for t in tags])
            else:
                tags_cache.append([None])


    df = {
        'url': repo_url_cache,
        'description': description_cache,
        'language': lang_cache,
        'tags': tags_cache
    }

    return pd.DataFrame(df).to_csv(dump_filepath)
 
        
    




if __name__ == "__main__":
    url ='https://github.com/github'
    #print(getInfo(url).head(10))
    getInfo(url, 'data/repositories.csv')
