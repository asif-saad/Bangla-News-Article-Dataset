import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines




cnt=560772
url='https://dailyinqilab.com/international/news/'
response = requests.get(url+str(cnt))
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    title=soup.find('div',class_='col-md-9 mt-3')
    time=soup.find('p',class_='news-date-time mt-1 mb-0')
    content=soup.find('div',class_='description')
    category=soup.find('a',class_='active')
    meta=soup.find('b',class_='sub-heading')




    if title:
        title=title.find('h2')
        print(title.text.strip())

    if time:
        print(time.text.strip().replace('\n',' '))

    
    # print(content.text.strip().replace('\n',''))


    if category:
        print(category.text)

    
    if meta:
        print(meta.text)
    







titleFinal=str()
categoryFinal=str()
timeFinal=str()
contentFinal=str()
metaFinal=str()
outputText='DailyInqilab/output.txt'
lastvalText='DailyInqilab/last_val.txt'
jsonl='C:/Users/asifs/OneDrive/Desktop/dataset/DailyInqilab.jsonl'
d={'DailyInqilab':Dataset.from_dict({'Title':titleFinal,'Category':categoryFinal,
                                           'Time':timeFinal,'Content':contentFinal,
                                           'Meta':metaFinal})}
raw_datasets=DatasetDict(d)
with open(lastvalText,'r') as file:
    cnt=int(file.read())

while True:
    print(cnt)
    url='https://dailyinqilab.com/international/news/'+str(cnt)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title=soup.find('div',class_='col-md-9 mt-3')
        time=soup.find('p',class_='news-date-time mt-1 mb-0')
        content=soup.find('div',class_='description')
        category=soup.find('a',class_='active')
        meta=soup.find('b',class_='sub-heading')




        if title and content:
            with open(outputText,'a',encoding='utf-8') as file2:
                with jsonlines.open(jsonl, "a") as writer:
                    # title
                    title=title.find('h2')
                    if title:
                        titleFinal=title.text.strip()
                    
                    file2.write(str(cnt)+'\n'+titleFinal+'\n')





                    # content
                    contentFinal=content.text.strip().replace('\n','')
                    file2.write('content:'+contentFinal+'\n')




                    # time date
                    timeFinal=time.text.strip().replace('\n',' ')
                    file2.write(timeFinal+'\n')



                    # category
                    categoryFinal=category.text
                    file2.write(categoryFinal+'\n')   



                    # meta data
                    if meta:
                        metaFinal=meta.text
                        file2.write(metaFinal+'\n')


                    file2.write('\n\n\n')
                    writer.write({'Title':titleFinal,'Category':categoryFinal,
                                'Time':timeFinal, 'Content':contentFinal,
                                'Meta':metaFinal})


    cnt+=1
    with open(lastvalText,'w') as file1:
        file1.write(str(cnt))




