import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines
import time

# Initialize variables
title_final = category_final = time_final = content_final = tags_final = str()
output_text = 'EkattorTv/output.txt'
jsonl_path = 'EkattorTv/dataset/ekattorTv.jsonl'
data_dict = {'EkattorTv': Dataset.from_dict({'Title': [], 'Category': [], 'Time': [], 'Content': [], 'Tags': []})}
raw_datasets = DatasetDict(data_dict)

# Base URL
url_base = 'https://ekattor.tv/'
cnt = 52174

while True:
    url = f'{url_base}{cnt}/'
    print(cnt)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        h1 = soup.find('h1', class_='title')
        category = soup.find('div', class_="breadcrumb")
        div = soup.find('div', class_='viewport jw_article_body')
        tag = soup.find('div', class_='topic_list')
        
        if h1 and div:
            h1_text = h1.text
            with open(output_text, 'a', encoding='utf-8') as file:
                with jsonlines.open(jsonl_path, "a") as writer:
                    # Process title
                    title_final = h1_text
                    file.write(f'{cnt-1587},{cnt}\n{title_final}\n')

                    # Process category
                    category_final = ''
                    if category:
                        ul = category.find('ul')
                        if ul:
                            li_elements = ul.find_all('li')
                            if len(li_elements) > 1:
                                category_final = li_elements[1].text
                                file.write(f'{category_final}\n')

                    # Process time
                    time_element = soup.find('span', class_='tts_time published_time')
                    if time_element:
                        time_final = time_element.get('content')
                        file.write(f'{time_final}\n')

                    # Process content
                    content_final = ''.join([p.text for p in div.find_all('p')])
                    file.write(f'{content_final}\n')

                    # Process tags
                    tags_final = ''
                    if tag:
                        tag_strong = tag.find_all('strong')
                        tags_final = ', '.join([x.text for x in tag_strong])
                        file.write(f'tags: {tags_final}\n\n\n')

                    # Write to JSONL
                    writer.write({'Title': title_final, 'Category': category_final, 'Time': time_final, 'Content': content_final, 'Tags': tags_final})
    else:
        print('Failed to retrieve the web page. Status code:', response.status_code)

    if cnt % 300 == 0:
        time.sleep(50)
    
    cnt += 1
