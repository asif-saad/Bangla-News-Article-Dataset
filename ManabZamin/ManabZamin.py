import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines

titleFinal=str()
categoryFinal=str()
timeFinal=str()
contentFinal=str()
outputText='ManabZamin/output.txt'
lastvalText='ManabZamin/last_val.txt'
jsonl='C:/Users/asifs/OneDrive/Desktop/dataset/ManabZamin.jsonl'
d={'ManabZamin':Dataset.from_dict({'Title':titleFinal,'Category':categoryFinal,
                                           'Time':timeFinal,'Content':contentFinal})}
raw_datasets=DatasetDict(d)
with open(lastvalText,'r') as file:
    cnt=int(file.read())

while True:
    print(cnt)
    url='https://mzamin.com/news.php?news='+str(cnt)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title=soup.find('h1',class_='lh-base fs-1')
        time=soup.find('div',class_='col-sm-8')
        content=soup.find('div',class_='col-sm-10 offset-sm-1 fs-5 lh-base mt-4 mb-5')
        category=soup.find('h4',class_='sectitle')
        if title and content:
            with open(outputText,'a',encoding='utf-8') as file2:
                with jsonlines.open(jsonl, "a") as writer:
                    title=title.text
                    titleFinal=title
                    # take title
                    file2.write(str(cnt)+'\n'+titleFinal+'\n')
                    # news content
                    contentFinal=content.text.replace('\n','')
                    file2.write(contentFinal+'\n')
                    # time date
                    if time:
                        timeP=time.find('p')
                        if timeP:
                            timeFinal=timeP.text
                        else:
                            timeFinal=time.find('h5').text
                        
                    file2.write(timeFinal+'\n')
                    # category
                    categoryFinal=category.text
                    file2.write(categoryFinal+'\n')   



                    file2.write('\n\n\n')
                    writer.write({'Title':titleFinal,'Category':categoryFinal,
                                'Time':timeFinal, 'Content':contentFinal})
    cnt+=1
    with open(lastvalText,'w') as file1:
        file1.write(str(cnt))



