import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines

# Initialize variables
title_final = category_final = time_final = content_final = tags_final = meta_final = str()
output_text = 'DhakaTribuneBangla/output.txt'
last_val_text = 'DhakaTribuneBangla/last_val.txt'
jsonl_path = 'DhakaTribuneBangla/dataset/DhakaTribuneBangla.jsonl'
data_dict = {'DhakaTribuneBangla': Dataset.from_dict({'Title': [], 'Category': [], 'Time': [], 'Meta': [], 'Content': [], 'Tags': []})}
raw_datasets = DatasetDict(data_dict)

# Read the last processed value
with open(last_val_text, 'r') as file:
    cnt = int(file.read())

while True:
    print(cnt)
    url = f'https://bangla.dhakatribune.com/{cnt}/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', class_='title mb10')
        meta = soup.find('div', class_='content_highlights jw_detail_content_holder content mb16')
        content = soup.find('div', class_='viewport jw_article_body').find_all('p')
        tag = soup.find('div', class_="content_tags")
        category = soup.find('div', class_='breadcrumb').find('ul').find_all('li')[1].find('a').find('strong')
        time = soup.find('div', class_='each_row time').find_all('span')[0]

        if title and content:
            with open(output_text, 'a', encoding='utf-8') as file2:
                with jsonlines.open(jsonl_path, "a") as writer:
                    # Process title
                    title_final = title.text
                    file2.write(f'{cnt}\n{title_final}\n')

                    # Process content
                    content_final = ''.join([p.get_text() for p in content]).strip()
                    file2.write(content_final + '\n')

                    # Process time
                    time_final = time.get_text()
                    file2.write(time_final + '\n')

                    # Process category
                    if category:
                        category_final = category.get_text()
                    file2.write(category_final + '\n')

                    # Process tags
                    tag_final = ''
                    if tag:
                        tag_div = tag.find('div')
                        if tag_div:
                            tag_strong = tag_div.find_all('strong')
                            if tag_strong:
                                tag_final = ', '.join([i.get_text() for i in tag_strong])
                    tags_final = tag_final
                    file2.write('\n' + tags_final)

                    # Process metadata
                    meta_final = ''
                    if meta:
                        meta_p = meta.find('p')
                        if meta_p:
                            meta_strong = meta_p.find('strong')
                            if meta_strong:
                                meta_final = meta_strong.get_text()
                    file2.write(meta_final + '\n')

                    # Write to JSONL
                    writer.write({'Title': title_final, 'Category': category_final, 'Time': time_final, 'Meta': meta_final, 'Content': content_final, 'Tags': tags_final})

    cnt += 1
    with open(last_val_text, 'w') as file1:
        file1.write(str(cnt))
