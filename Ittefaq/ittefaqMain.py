import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines

# Initialize variables
title_final = category_final = time_final = content_final = tags_final = str()
output_text = 'IttefaqNews/output.txt'
last_val_text = 'IttefaqNews/last_val.txt'
jsonl_path = 'IttefaqNews/dataset/ittefaq.jsonl'
data_dict = {'IttefaqNews': Dataset.from_dict({'Title': [], 'Category': [], 'Time': [], 'Content': [], 'Tags': []})}
raw_datasets = DatasetDict(data_dict)

# Base URL
url_base = 'https://www.ittefaq.com.bd/'
cnt = 381863

# Read the last processed value
with open(last_val_text, "r") as file:
    cnt = int(file.read())

while True:
    with open(last_val_text, "w") as file:
        url = f'{url_base}{cnt}/'
        print(cnt)
        response = requests.get(url)
        
        if response.status_code == 200:
            file.write(str(cnt))
            soup = BeautifulSoup(response.text, 'html.parser')
            h1 = soup.find('h1', class_='title mb10')
            contents = soup.find('div', class_='viewport jw_article_body')
            category = soup.find('h2', class_='secondary_logo')
            date = soup.find('div', class_='each_row time')
            tags = soup.find('div', class_='topic_list')

            if h1 and contents:
                with open(output_text, 'a', encoding='utf-8') as file:
                    with jsonlines.open(jsonl_path, "a") as writer:
                        # Process title
                        title_final = h1.text
                        file.write(f'{cnt-15817},{cnt}\n{title_final}\n')

                        # Process category
                        if category:
                            category_span = category.find('span')
                            if category_span:
                                category_final = category_span.text
                                file.write(f'{category_final}\n')

                        # Process time
                        if date:
                            date_span = date.find('span', class_='tts_time')
                            if date_span:
                                time_final = date_span.text
                                file.write(time_final)

                        # Process content
                        content_final = ''.join([x.text for x in contents])
                        file.write(content_final)

                        # Process tags
                        if tags:
                            tags_strong = tags.find_all('strong')
                            if tags_strong:
                                tags_final = ', '.join([x.text for x in tags_strong])
                                file.write(f'\ntags:{tags_final}')

                        file.write('\n\n\n')
                        writer.write({'Title': title_final, 'Category': category_final, 'Time': time_final, 'Content': content_final, 'Tags': tags_final})
        
        else:
            print('Failed to retrieve the web page. Status code:', response.status_code)
        
        cnt += 1
