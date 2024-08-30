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
d={'EkattorTv':Dataset.from_dict({'Title':titleFinal,'Category':categoryFinal,'Time':timeFinal,'Content':contentFinal,'Tags':tagsFinal})}
raw_datasets=DatasetDict(d)






url1='https://ekattor.tv/'
cnt=52174

while True:
    url=url1+str(cnt)+"/"
    print(cnt)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        h1=soup.find('h1',class_='title')
        category=soup.find('div',class_="breadcrumb")
        div=soup.find('div',class_='viewport jw_article_body')
        tag=soup.find('div',class_='topic_list')
        if h1 and div:
            h1=h1.text
            with open('output.txt','a',encoding='utf-8') as file:
                with jsonlines.open("C:/Users/asifs/OneDrive/Desktop/dataset/ekattorTv.jsonl", "a") as writer:
                    titleFinal=str()
                    categoryFinal=str()
                    timeFinal=str()
                    contentFinal=str()
                    tagsFinal=str()




                    file.write(str(cnt-1587)+','+cnt+'\n'+h1+'\n')
                    titleFinal=h1
                    
                

                    # category
                    if category:
                        category=category.find('ul')
                        if category:
                            category=category.find_all('li')
                            if category:
                                category=category[1].text
                                # print(category)
                                file.write(category+'\n')
                                categoryFinal=category
                                

                
                    # time
                    time=soup.find('span',class_='tts_time published_time')
                    if time:
                        file.write(time.get('content')+'\n')
                        timeFinal=time.get('content')
                        



                    # content
                    p=div.find_all('p')
                    content=str()
                    if p:
                        for x in p:
                            content+=x.text
                        file.write(content+'\n')
                        contentFinal=content
                        


                    # tags
                    if tag:
                        tag=tag.find_all('strong')
                        tags=str()
                        for x in tag:
                            tags+=x.text
                            if x!=tag[-1]:
                                tags+=', '
                        file.write('tags:'+tags+'\n\n\n')
                        tagsFinal=tags
                    

                    writer.write({'Title':titleFinal,'Category':categoryFinal,'Time':timeFinal,
                                  'Content':contentFinal,'Tags':tagsFinal})

    else:
        print('Failed to retrieve the web page. Status code:', response.status_code)
        
    
    if cnt%300==0:
        import time
        time.sleep(50)
    cnt+=1
    







