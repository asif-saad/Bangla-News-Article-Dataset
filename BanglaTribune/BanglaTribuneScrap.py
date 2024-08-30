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
d={'BanglaTribune':Dataset.from_dict({'Title':titleFinal,'Category':categoryFinal,'Time':timeFinal,'Content':contentFinal,'Tags':tagsFinal})}
raw_datasets=DatasetDict(d)

with open('C:/Users/asifs/OneDrive/Desktop/News-Article-Dataset/BanglaTribune/last_val.txt','r') as file:
    cnt=int(file.read())



while True:
    print(cnt)
    url='https://www.banglatribune.com/'+str(cnt)+'/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tag=soup.find('span')
        title= soup.find('h1',class_='title mb10')
        content=soup.find('div',class_='viewport jw_article_body')
        time=soup.find('span',class_='tts_time')
        categories=soup.find('div',class_='breadcrumb')
        tags=soup.find('div',class_='topic_list')



        if title and content:
            with open('BanglaTribune/output.txt','a',encoding='utf-8') as file2:
                with jsonlines.open("C:/Users/asifs/OneDrive/Desktop/dataset/BanglaTribune.jsonl", "a") as writer:
                    title=title.text
                    titleFinal=title
                    file2.write(str(cnt)+'\n'+titleFinal+'\n')
                    # take title
                    news=str()
                    for contents in content:
                        news+=contents.text
                    contentFinal=news.strip()
                    file2.write(contentFinal+'\n')
                    # take news
                    time=time.text
                    timeFinal=time
                    file2.write(timeFinal+'\n')
                    # take time    
                    category=str()
                    if categories:
                        categories=categories.find_all('strong')
                        if categories:
                            for x in range(1,len(categories)):
                                category+=categories[x].text
                                if categories[x].text!=categories[-1].text:
                                    category+=', '
                            # take category
                            categoryFinal=category
                            file2.write(categoryFinal+'\n')

                    tag=str()
                    if tags:
                        tags=tags.find_all('strong')
                        for i in tags:
                            tag+=i.text
                            if i.text!=tags[-1].text:
                                tag+=', '
                    # take tag
                    tagsFinal=tag
                    file2.write('\ntags:'+tagsFinal)

                    file2.write('\n\n\n')
                    writer.write({'Title':titleFinal,'Category':categoryFinal,'Time':timeFinal,
                                    'Content':contentFinal,'Tags':tagsFinal})
    cnt+=1
    with open('BanglaTribune/last_val.txt','w') as file1:
        file1.write(str(cnt))

