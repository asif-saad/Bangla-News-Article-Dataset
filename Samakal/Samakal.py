import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines

# Initialize variables
title_final = time_final = content_final = tags_final = str()
output_text = 'Samakal/output.txt'
last_val_text = 'Samakal/last_val.txt'
jsonl_path = 'Samakal/dataset/Samakal.jsonl'
data_dict = {'Samakal': Dataset.from_dict({'Title': [], 'Time': [], 'Content': [], 'Tags': []})}
raw_datasets = DatasetDict(data_dict)

# Read the last processed value
with open(last_val_text, 'r') as file:
    cnt = int(file.read())

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

while True:
    print(cnt)
    url = f'https://www.samakal.com/politics/article/{cnt}/'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('div', class_='dheading')
        time = soup.find('div', class_='dateAndTime')
        content = soup.find('div', class_='dNewsDesc')
        tag = soup.find('div', class_='tagArea')

        if title and content:
            with open(output_text, 'a', encoding='utf-8') as file2:
                with jsonlines.open(jsonl_path, "a") as writer:
                    # Process title
                    title_h1 = title.find('h1')
                    if title_h1:
                        title_final = title_h1.text
                    file2.write(f'{cnt}\n{title_final}\n')

                    # Process content
                    content_final = content.text.replace('﻿', '').replace('\n', '')
                    file2.write(f'{content_final}\n')

                    # Process time
                    if time:
                        time_p = time.find('p')
                        if time_p:
                            time_i = time_p.find('i')
                            if time_i:
                                time_final = time_p.text
                    file2.write(f'{time_final}\n')

                    # Process tags
                    tags_final = ''
                    if tag:
                        tag_ul = tag.find('ul')
                        if tag_ul:
                            tag_a = tag_ul.find_all('a')
                            if tag_a:
                                tags_final = ', '.join([i.text for i in tag_a])
                    file2.write(f'\n{tags_final}\n\n\n')

                    # Write to JSONL
                    writer.write({'Title': title_final, 'Time': time_final, 'Content': content_final, 'Tags': tags_final})
    
    cnt += 1
    with open(last_val_text, 'w') as file1:
        file1.write(str(cnt))
