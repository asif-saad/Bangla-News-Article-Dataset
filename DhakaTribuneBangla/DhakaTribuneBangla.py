import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines

titleFinal=str()
categoryFinal=str()
timeFinal=str()
contentFinal=str()
tagsFinal=str()
metaFinal=str()
outputText='DhakaTribuneBangla/output.txt'
lastvalText='DhakaTribuneBangla/last_val.txt'
jsonl='C:/Users/asifs/OneDrive/Desktop/dataset/DhakaTribuneBangla.jsonl'
d={'DhakaTribuneBangla':Dataset.from_dict({'Title':titleFinal,'Category':categoryFinal,
                                           'Time':timeFinal,'Meta':metaFinal,
                                           'Content':contentFinal,'Tags':tagsFinal})}
raw_datasets=DatasetDict(d)

with open('DhakaTribuneBangla/last_val.txt','r') as file:
    cnt=int(file.read())



while True:
    print(cnt)
    url='https://bangla.dhakatribune.com/'+str(cnt)+'/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title=soup.find('h1',class_='title mb10')
        meta=soup.find('div',class_='content_highlights jw_detail_content_holder content mb16')
        content=soup.find('div',class_='viewport jw_article_body').find_all('p')
        tag=soup.find('div',class_="content_tags")
        category=soup.find('div',class_='breadcrumb').find('ul').find_all('li')[1].find('a').find('strong')
        time=soup.find('div',class_='each_row time').find_all('span')[0]
        if title and content:
            with open('DhakaTribuneBangla/output.txt','a',encoding='utf-8') as file2:
                with jsonlines.open("C:/Users/asifs/OneDrive/Desktop/dataset/DhakaTribuneBangla.jsonl", "a") as writer:
                    title=title.text
                    titleFinal=title
                    # take title
                    file2.write(str(cnt)+'\n'+titleFinal+'\n')
                    # news content
                    news=str()
                    for contents in content:
                        news+=contents.get_text()
                    contentFinal=news.strip()
                    file2.write(contentFinal+'\n')
                    # time date
                    time=time.get_text()
                    timeFinal=time
                    file2.write(timeFinal+'\n')
                    # category
                    if category:
                        category=category.get_text()
                    categoryFinal=category
                    file2.write(categoryFinal+'\n')   

                    # tag
                    tag_=str()
                    if tag:
                        tag=tag.find('div')
                        if tag:
                            tag=tag.find_all('strong')
                            if tag:
                                for i in tag:
                                    tag_+=i.get_text()
                                    if i.get_text()!=tag[-1].get_text():
                                        tag_+=', '
                    tagsFinal=tag_
                    file2.write('\n'+tagsFinal)
                    

                    # metadata
                    metaData=str()
                    if meta:
                        meta=meta.find('p')
                        if meta:
                            meta=meta.find('strong')
                            if meta:
                                metaData=meta.get_text()
                    metaFinal=metaData
                    file2.write(metaFinal+'\n')


                    file2.write('\n\n\n')
                    writer.write({'Title':titleFinal,'Category':categoryFinal,
                                'Time':timeFinal,'Meta':metaFinal,
                                'Content':contentFinal,'Tags':tagsFinal})
    cnt+=1
    with open('DhakaTribuneBangla/last_val.txt','w') as file1:
        file1.write(str(cnt))


