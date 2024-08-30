import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines

# Initial setup
cnt = 560772
url = 'https://dailyinqilab.com/international/news/'
response = requests.get(url + str(cnt))

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('div', class_='col-md-9 mt-3')
    time = soup.find('p', class_='news-date-time mt-1 mb-0')
    content = soup.find('div', class_='description')
    category = soup.find('a', class_='active')
    meta = soup.find('b', class_='sub-heading')

    if title:
        title = title.find('h2')
        print(title.text.strip())

    if time:
        print(time.text.strip().replace('\n', ' '))

    if category:
        print(category.text)

    if meta:
        print(meta.text)

# Define constants and initialize variables
title_final = category_final = time_final = content_final = meta_final = str()
output_text = 'DailyInqilab/output.txt'
last_val_text = 'DailyInqilab/last_val.txt'
jsonl_path = 'DailyInqilab/dataset/DailyInqilab.jsonl'
data_dict = {'DailyInqilab': Dataset.from_dict({'Title': [], 'Category': [], 'Time': [], 'Content': [], 'Meta': []})}
raw_datasets = DatasetDict(data_dict)

# Read the last processed value
with open(last_val_text, 'r') as file:
    cnt = int(file.read())

while True:
    print(cnt)
    url = f'https://dailyinqilab.com/international/news/{cnt}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('div', class_='col-md-9 mt-3')
        time = soup.find('p', class_='news-date-time mt-1 mb-0')
        content = soup.find('div', class_='description')
        category = soup.find('a', class_='active')
        meta = soup.find('b', class_='sub-heading')

        if title and content:
            with open(output_text, 'a', encoding='utf-8') as file2:
                with jsonlines.open(jsonl_path, "a") as writer:
                    # Process title
                    title = title.find('h2')
                    if title:
                        title_final = title.text.strip()
                    file2.write(f'{cnt}\n{title_final}\n')

                    # Process content
                    content_final = content.text.strip().replace('\n', '')
                    file2.write(f'content: {content_final}\n')

                    # Process time
                    time_final = time.text.strip().replace('\n', ' ')
                    file2.write(f'{time_final}\n')

                    # Process category
                    category_final = category.text
                    file2.write(f'{category_final}\n')

                    # Process meta data
                    if meta:
                        meta_final = meta.text
                        file2.write(f'{meta_final}\n')

                    # Write to JSONL
                    writer.write({'Title': title_final, 'Category': category_final, 'Time': time_final, 'Content': content_final, 'Meta': meta_final})

    # Increment and save the last processed value
    cnt += 1
    with open(last_val_text, 'w') as file1:
        file1.write(str(cnt))
