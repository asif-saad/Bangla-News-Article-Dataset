import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines
import re

# Initialize variables
title_final = category_final = time_final = content_final = str()
output_text = 'JanaKantha/output.txt'
last_val_text = 'JanaKantha/last_val.txt'
jsonl_path = 'JanaKantha/dataset/JanaKantha.jsonl'
data_dict = {'JanaKantha': Dataset.from_dict({'Title': [], 'Category': [], 'Time': [], 'Content': []})}
raw_datasets = DatasetDict(data_dict)

# Read the last processed value
with open(last_val_text, 'r') as file:
    cnt = int(file.read())

while True:
    print(cnt)
    url = f'https://www.dailyjanakantha.com/news/{cnt}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('div', class_='DDetailsTitle')
        category = soup.find('div', class_='InnerCatTitle')
        time = soup.find('div', class_='pDate')
        content_classes = ['col-lg-10 col-12 offset-lg-1', 'DDetailsBody DMarginTop10 col-sm-12', 'contentDetails']

        content_final = None
        for class_name in content_classes:
            content_div = soup.find('div', class_=class_name)
            if content_div:
                content_final = re.sub(r'\s+', ' ', content_div.text.strip())
                break

        if title and content_final:
            with open(output_text, 'a', encoding='utf-8') as file2:
                with jsonlines.open(jsonl_path, "a") as writer:
                    # Write content
                    file2.write(f'{content_final}\n')

                    # Write title
                    title_h1 = title.find('h1')
                    if title_h1:
                        title_final = title_h1.text
                    file2.write(f'{cnt}\n{title_final}\n')

                    # Write time
                    if time:
                        time_final = time.text.strip()
                    file2.write(f'{time_final}\n')

                    # Write category
                    if category:
                        category_h2 = category.find('h2')
                        if category_h2:
                            category_final = category_h2.text
                    file2.write(f'{category_final}\n')

                    file2.write('\n\n\n')

                    # Write to JSONL
                    writer.write({'Title': title_final, 'Category': category_final, 'Time': time_final, 'Content': content_final})
    
    cnt += 1
    with open(last_val_text, 'w') as file1:
        file1.write(str(cnt))
