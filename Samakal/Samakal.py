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
outputText='Samakal/output.txt'
lastvalText='Samakal/last_val.txt'
jsonl='C:/Users/asifs/OneDrive/Desktop/dataset/Samakal.jsonl'
d={'Samakal':Dataset.from_dict({'Title':titleFinal,'Time':timeFinal,
                                'Content':contentFinal,'Tags':tagsFinal})}
raw_datasets=DatasetDict(d)

with open(lastvalText,'r') as file:
    cnt=int(file.read())
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

while True:
    print(cnt)
    url='https://www.samakal.com/politics/article/'+str(cnt)+'/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('div', class_='dheading')
        time=soup.find('div',class_='dateAndTime')
        content=soup.find('div',class_='dNewsDesc')
        tag=soup.find('div',class_='tagArea')
        if title and content:
            with open(outputText,'a',encoding='utf-8') as file2:
                with jsonlines.open(jsonl, "a") as writer:
                    #title
                    if title:
                        title = title.find('h1')
                        if title:
                            titleFinal=title.text
                    file2.write(str(cnt)+'\n'+titleFinal+'\n')
                    # news content
                    contentFinal=content.text.replace('﻿', '').replace('\n', '')
                    file2.write(contentFinal+'\n')
                    # time date
                    if time:
                        time=time.find('p')
                        if time:
                            time.find('i')
                            timeFinal=time.text
                    file2.write(timeFinal+'\n')

                    # tag
                    tags_=str()
                    if tag:
                        tag=tag.find('ul')
                        if tag:
                            tag=tag.find_all('a')
                            if tag:
                                for i in tag:
                                    tags_+=i.text
                                    if i.text!=tag[-1].text:
                                        tags_+=', '
                    
                    tagsFinal=tags_
                    file2.write('\n'+tagsFinal)
                    



                    file2.write('\n\n\n')
                    writer.write({'Title':titleFinal,'Time':timeFinal,
                                'Content':contentFinal,'Tags':tagsFinal})
    cnt+=1
    with open(lastvalText,'w') as file1:
        file1.write(str(cnt))


