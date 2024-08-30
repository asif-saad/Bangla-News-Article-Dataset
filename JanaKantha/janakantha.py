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
outputText='JanaKantha/output.txt'
lastvalText='JanaKantha/last_val.txt'
jsonl='C:/Users/asifs/OneDrive/Desktop/dataset/JanaKantha.jsonl'
d={'JanaKantha':Dataset.from_dict({'Title':titleFinal,'Category':categoryFinal,
                                           'Time':timeFinal,'Content':contentFinal})}
raw_datasets=DatasetDict(d)
with open(lastvalText,'r') as file:
    cnt=int(file.read())

while True:
    print(cnt)
    url='https://www.dailyjanakantha.com/news/'+str(cnt)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title=soup.find('div',class_='DDetailsTitle')
        category=soup.find('div',class_='InnerCatTitle')
        time=soup.find('div',class_='pDate')
        content_class=['col-lg-10 col-12 offset-lg-1','DDetailsBody DMarginTop10 col-sm-12','contentDetails']

        if title:
            with open(outputText,'a',encoding='utf-8') as file2:
                with jsonlines.open(jsonl, "a") as writer:

                    for i in content_class:
                        if(soup.find('div',class_=content_class)):
                            contentFinal=re.sub(r'\s+', ' ', soup.find('div',class_=content_class).text.strip())
                            break
                    # news content
                    if contentFinal==None:
                        continue
                    file2.write(contentFinal+'\n')



                    # news title
                    title=title.find('h1')
                    if title:
                        titleFinal=title.text

                    print(titleFinal)
                    # take title
                    file2.write(str(cnt)+'\n'+titleFinal+'\n')



                    # time date
                    if time:
                        timeFinal=time.text.strip()
                        
                    file2.write(timeFinal+'\n')

                    # category
                    if category:
                        category=category.find('h2')
                        if category:
                            categoryFinal=category.text

                    file2.write(categoryFinal+'\n')   



                    file2.write('\n\n\n')
                    writer.write({'Title':titleFinal,'Category':categoryFinal,
                                'Time':timeFinal, 'Content':contentFinal})
    cnt+=1
    with open(lastvalText,'w') as file1:
        file1.write(str(cnt))

