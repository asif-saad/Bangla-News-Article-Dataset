import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines
import re

titleFinal=str()
categoryFinal=str()
timeFinal=str()
contentFinal=str()
keywordsFinal=str()
metaFinal=str()
outputText='AjkerPatrika/output.txt'
lastvalText='AjkerPatrika/last_val.txt'
jsonl='C:/Users/asifs/OneDrive/Desktop/dataset/AjkerPatrika.jsonl'
d={'AjkerPatrika':Dataset.from_dict({'Title':titleFinal,'Category':categoryFinal,
                                           'Time':timeFinal,'Content':contentFinal,
                                           'Keywords': keywordsFinal,'Meta':metaFinal})}
raw_datasets=DatasetDict(d)
with open(lastvalText,'r') as file:
    cnt=int(file.read())

while True:
    print(cnt)
    url='https://www.ajkerpatrika.com/'+str(cnt)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title=soup.find('h1',class_='title')
        time=soup.find('span',class_='tts_time content_published_time')
        content=soup.find('div',class_='viewport jw_article_body')
        meta=soup.find('div',class_='content_highlights jw_detail_content_holder content mb16')
        category=soup.find('div',class_='breadcrumb')
        keyword=soup.find('div',class_='more_and_tag')





        if title and content:
            with open(outputText,'a',encoding='utf-8') as file2:
                with jsonlines.open(jsonl, "a") as writer:
                    titleFinal=str()
                    categoryFinal=str()
                    timeFinal=str()
                    contentFinal=str()
                    keywordsFinal=str()
                    metaFinal=str()




                    contentFinal=content.text.strip()
                    file2.write(contentFinal+'\n')



                    # news title
                    titleFinal=title.text
                    file2.write(str(cnt)+'\n'+titleFinal+'\n')



                    # time date
                    timeFinal=time.text  
                    file2.write(timeFinal+'\n')

                    # category
                    if category:
                        category=category.find_all('li')[1:]
                        if category:
                            for i in category:
                                i=i.find('strong')
                                categoryFinal+=i.text
                                if i.text != category[-1].find('strong').text:
                                    categoryFinal+=', '
                    file2.write('category: ')   
                    file2.write(categoryFinal+'\n')  



                    # keyword
                    if keyword:
                        keyword=keyword.find_all('strong')
                        for i in keyword:
                            keywordsFinal+=i.text
                            if i.text != keyword[-1].text:
                                keywordsFinal+=', '
                    file2.write('keywords: ')   
                    file2.write(keywordsFinal+'\n')  




                    # meta data
                    if meta:
                        if meta.find('p'):
                            metaFinal=meta.find('p').text    
                    file2.write('meta: ')                
                    file2.write(metaFinal+'\n')  




                    file2.write('\n\n\n')
                    writer.write({'Title':titleFinal,'Category':categoryFinal,
                                           'Time':timeFinal,'Content':contentFinal,
                                           'Keywords': keywordsFinal,'Meta':metaFinal})
    cnt+=1
    with open(lastvalText,'w') as file1:
        file1.write(str(cnt))

