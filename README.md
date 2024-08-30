#  [BNAD: Bangla News Article Dataset](https://www.sciencedirect.com/science/article/pii/S2352340924008382?via%3Dihub)

**size: 16.7GB**
## Overview

Explore over 1.9 million Bangla news articles from nine major websites, categorized across topics like sports, economy, politics, local news, tech, tourism, entertainment, education, health, the arts, and many more. Each article includes rich metadata, perfect for advancing Bangla natural language processing. This dataset is ideal for building domain-specific models and innovative AI solutions in the context of Bangladesh.

## Dataset Specifications:


### **Features:**

| **Features**              | **Our Dataset**                                                                                                       |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------|
|  **Type of Data**          |      JSONL files                                                                                                                 |
| **Number of Articles**     | 1,927,229                                                                                                             |
| **Number of Attributes**   | At most 6, ranging from at least 4                                                                                     |
| **Number of Newspapers**   | 9 newspapers                                                                                                           |
| **News Timespan**          | Well updated to the latest                                                                                             |
| **Use Cases**              | Keyword similarity and dissimilarity maps, text generation, part-of-speech tagging, named entity recognition, and question answering |

### **Data Collection:**  
This dataset comprises articles collected from nine major Bangla news websites using web-scraping tools. The time range of the articles varies per newspaper, depending on the availability of their online archives. Categories include national, politics, international, sports, education, entertainment, health, science and technology, and more. Each newspaper provides various attributes, including Date and Time, Category, Title, Content, Tags, and Meta. Data was collected using Python, with **Requests** and **BeautifulSoup** as the main tools.

### **News Source Locations:**  
**The news articles were collected from the following news websites:**  
>- **[ajkerpatrika.com](https://www.ajkerpatrika.com)**  
>- **[banglatribune.com](https://www.banglatribune.com)**  
>- **[dailyinqilab.com](https://www.dailyinqilab.com)**  
>- **[bangla.dhakatribune.com](https://bangla.dhakatribune.com)**  
>- **[ekattor.tv](https://www.ekattor.tv)**  
>- **[ittefaq.com.bd](https://www.ittefaq.com.bd)**  
>- **[dailyjanakantha.com](https://www.dailyjanakantha.com)**  
>- **[mzamin.com](https://www.mzamin.com)**  
>- **[samakal.com](https://www.samakal.com)**


 ### **📂 Data Accessibility**
 - **Repository Name:** [**Zenodo**](https://zenodo.org/records/11111869)  
 - **Direct Access:** [https://zenodo.org/records/11111869](https://zenodo.org/records/11111869)  
 - **Access Instructions:** The dataset is publicly accessible through the provided URL
### Usage:
The following diagram provides an overview of the dataset's usage:
![Dataset Usage](https://ars.els-cdn.com/content/image/1-s2.0-S2352340924008382-gr4_lrg.jpg)




## License

Contents of this repository are restricted to only non-commercial research purposes under the [license name ](link). Copyright of the dataset contents belongs to the original copyright holders.

## **Citation** 👍
If you use our data, please cite the following paper:



```bibtex
@article{SAAD2024110874,
title = {Bangla news article dataset},
journal = {Data in Brief},
pages = {110874},
year = {2024},
issn = {2352-3409},
doi = {https://doi.org/10.1016/j.dib.2024.110874},
url = {https://www.sciencedirect.com/science/article/pii/S2352340924008382},
author = {Asif Mohammed Saad and Umme Niraj Mahi and Md. Shahidul Salim and Sk Imran Hossain},
keywords = {Data analysis, Classification, Natural language processing},
abstract = {In this research, we present an updated standard Bangla dataset based on gathered Bangla news articles. In total, more than 1.9 million articles from nine Bangla news websites were gathered; the selection process was led by a number of categories, including sports, economy, politics, local news, tech, tourism, entertainment, education, health, the arts, and many more. The dataset per newspaper contains varying attributes, such as title, content, time, tags, meta, category, etc. This dataset will enable data scientists to investigate and assess theories related to Bangla natural language processing. Furthermore, there is a greater chance that the dataset will be utilized for domain-specific large language models in the context of Bangladesh, and it may be used to develop deep learning and machine learning models that categorize articles according to subjects.}
}
