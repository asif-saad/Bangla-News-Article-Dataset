import requests
from bs4 import BeautifulSoup
from datasets.dataset_dict import DatasetDict
from datasets import Dataset
import jsonlines

# Initialize variables
title_final = category_final = time_final = content_final = str()
output_text = 'ManabZamin/output.txt'
last_val_text = 'ManabZamin/last_val.txt'
jsonl_path = 'ManabZamin/dataset/ManabZamin.jsonl'
data_dict = {'ManabZamin': Dataset.from_dict({'Title': [], 'Category': [], 'Time': [], 'Content': []})}
raw_datasets = DatasetDict(data_dict)

# Read the last processed value
with open(last_val_text, 'r') as file:
    cnt = int(file.read())

while True:
    print(cnt)
    url = f'https://mzamin.com/news.php?news={cnt}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', class_='lh-base fs-1')
        time = soup.find('div', class_='col-sm-8')
        content = soup.find('div', class_='col-sm-10 offset-sm-1 fs-5 lh-base mt-4 mb-5')
        category = soup.find('h4', class_='sectitle')

        if title and content:
            with open(output_text, 'a', encoding='utf-8') as file2:
                with jsonlines.open(jsonl_path, "a") as writer:
                    # Process title
                    title_final = title.text
                    file2.write(f'{cnt}\n{title_final}\n')

                    # Process content
                    content_final = content.text.replace('\n', '')
                    file2.write(f'{content_final}\n')

                    # Process time
                    if time:
                        time_p = time.find('p')
                        if time_p:
                            time_final = time_p.text
                        else:
                            time_final = time.find('h5').text
                    file2.write(f'{time_final}\n')

                    # Process category
                    category_final = category.text
                    file2.write(f'{category_final}\n')

                    file2.write('\n\n\n')

                    # Write to JSONL
                    writer.write({'Title': title_final, 'Category': category_final, 'Time': time_final, 'Content': content_final})
    
    cnt += 1
    with open(last_val_text, 'w') as file1:
        file1.write(str(cnt))
