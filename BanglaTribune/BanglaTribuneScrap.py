import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines

# Define constants and initialize variables
OUTPUT_TEXT = 'BanglaTribune/output.txt'
LAST_VAL_TEXT = 'BanglaTribune/last_val.txt'
JSONL_PATH = 'BanglaTribune/dataset/BanglaTribune.jsonl'
DATA_DICT = {'BanglaTribune': Dataset.from_dict({'Title': [], 'Category': [], 'Time': [], 'Content': [], 'Tags': []})}
raw_datasets = DatasetDict(DATA_DICT)

# Read the last processed value
with open(LAST_VAL_TEXT, 'r') as file:
    cnt = int(file.read())

while True:
    print(cnt)
    url = f'https://www.banglatribune.com/{cnt}/'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', class_='title mb10')
        content = soup.find('div', class_='viewport jw_article_body')
        time = soup.find('span', class_='tts_time')
        categories = soup.find('div', class_='breadcrumb')
        tags = soup.find('div', class_='topic_list')

        if title and content:
            with open(OUTPUT_TEXT, 'a', encoding='utf-8') as file2:
                with jsonlines.open(JSONL_PATH, "a") as writer:
                    # Extract and clean the content
                    content_final = ''.join([c.text for c in content]).strip()
                    title_final = title.text
                    time_final = time.text if time else ''
                    category_final = ', '.join([c.text for c in categories.find_all('strong')[1:]]) if categories else ''
                    tags_final = ', '.join([t.text for t in tags.find_all('strong')]) if tags else ''

                    # Write data to output file
                    file2.write(f'{cnt}\n{title_final}\n{content_final}\n{time_final}\n{category_final}\ntags: {tags_final}\n\n\n')

                    # Write data to JSONL file
                    writer.write({'Title': title_final, 'Category': category_final, 'Time': time_final, 'Content': content_final, 'Tags': tags_final})

    # Increment and save the last processed value
    cnt += 1
    with open(LAST_VAL_TEXT, 'w') as file1:
        file1.write(str(cnt))
