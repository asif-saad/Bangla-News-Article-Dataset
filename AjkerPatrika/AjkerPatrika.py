import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines

# Define constants and initialize variables
OUTPUT_TEXT = 'AjkerPatrika/output.txt'
LAST_VAL_TEXT = 'AjkerPatrika/last_val.txt'
JSONL_PATH = 'AjkerPatrika/dataset/AjkerPatrika.jsonl'
DATA_DICT = {'AjkerPatrika': Dataset.from_dict({'Title': [], 'Category': [], 'Time': [], 'Content': [], 'Keywords': [], 'Meta': []})}
raw_datasets = DatasetDict(DATA_DICT)

# Read the last processed value
with open(LAST_VAL_TEXT, 'r') as file:
    cnt = int(file.read())

while True:
    print(cnt)
    url = f'https://www.ajkerpatrika.com/{cnt}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', class_='title')
        time = soup.find('span', class_='tts_time content_published_time')
        content = soup.find('div', class_='viewport jw_article_body')
        meta = soup.find('div', class_='content_highlights jw_detail_content_holder content mb16')
        category = soup.find('div', class_='breadcrumb')
        keyword = soup.find('div', class_='more_and_tag')

        if title and content:
            with open(OUTPUT_TEXT, 'a', encoding='utf-8') as file2:
                with jsonlines.open(JSONL_PATH, "a") as writer:
                    content_final = content.text.strip()
                    title_final = title.text
                    time_final = time.text if time else ''
                    category_final = ', '.join([i.find('strong').text for i in category.find_all('li')[1:]]) if category else ''
                    keywords_final = ', '.join([i.text for i in keyword.find_all('strong')]) if keyword else ''
                    meta_final = meta.find('p').text if meta and meta.find('p') else ''

                    # Write data to output file
                    file2.write(f'{cnt}\n{title_final}\n{time_final}\ncategory: {category_final}\nkeywords: {keywords_final}\nmeta: {meta_final}\n\n\n')

                    # Write data to JSONL file
                    writer.write({'Title': title_final, 'Category': category_final, 'Time': time_final, 'Content': content_final, 'Keywords': keywords_final, 'Meta': meta_final})

    # Increment and save the last processed value
    cnt += 1
    with open(LAST_VAL_TEXT, 'w') as file1:
        file1.write(str(cnt))
