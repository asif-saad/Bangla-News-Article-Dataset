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
d={'IttefaqNews':Dataset.from_dict({'Title':titleFinal,'Category':categoryFinal,'Time':timeFinal,'Content':contentFinal,'Tags':tagsFinal})}
raw_datasets=DatasetDict(d)

url1='https://www.ittefaq.com.bd/'
cnt=381863
with open("last_val.txt","r") as file:
    cnt=int(file.read())




while True:
    with open("last_val.txt","w") as file:
        url=url1+str(cnt)+"/"
        print(cnt)
        response = requests.get(url)
        if response.status_code == 200:
            file.write(str(cnt))
            soup = BeautifulSoup(response.text, 'html.parser')
            h1=soup.find('h1',class_='title mb10')
            contents=soup.find('div',class_='viewport jw_article_body')
            category=soup.find('h2',class_='secondary_logo')
            date=soup.find('div',class_='each_row time')
            tags=soup.find('div',class_='topic_list')

            if h1 and contents:
                with open('output.txt','a',encoding='utf-8') as file:
                    with jsonlines.open("C:/Users/asifs/OneDrive/Desktop/dataset/ittefaq.jsonl", "a") as writer:
                        titleFinal=str()
                        categoryFinal=str()
                        timeFinal=str()
                        contentFinal=str()
                        tagsFinal=str()

                        # titles
                        h1=h1.text
                        titleFinal=h1
                        file.write(str(cnt-15817)+','+str(cnt)+'\n'+titleFinal+'\n')

                        # category
                        if category:
                            category=category.find('span')
                            # print(category.text)
                            if category:
                                categoryFinal=category.text
                                file.write(categoryFinal+'\n')

                        # time
                        if date:
                            date=date.find('span',class_='tts_time')
                            # print(date.text)
                            if date:
                                timeFinal=date.text
                                file.write(timeFinal)

                        # contents
                        content=str()
                        for x in contents:
                            content+=x.text
                        contentFinal=content
                        file.write(contentFinal)

                        # tags
                        if tags:
                            tags=tags.find_all('strong')
                            if tags:
                                tag=str()
                                for x in tags:
                                    tag+=x.text
                                    if x.text!=tags[-1].text:
                                        tag+=', '
                                tagsFinal=tag
                                file.write('\ntags:'+tagsFinal)


                        file.write('\n\n\n')
                        writer.write({'Title':titleFinal,'Category':categoryFinal,'Time':timeFinal,
                                    'Content':contentFinal,'Tags':tagsFinal})

                            
        else:
            print('Failed to retrieve the web page. Status code:', response.status_code)
        cnt+=1

