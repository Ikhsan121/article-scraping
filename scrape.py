import requests
from html_table_parser import HTMLTableParser
from text_processing import remove_tags, renumber_ulist, renumber_olist, create_table
from bs4 import BeautifulSoup
import os
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}


def scrape_tool(start, end, data, name):
    for i in range(start, end):  #change the start and end bounds of the index
        r = requests.get(data[i], headers=headers)
        print(f"status code: {r.status_code}")
        print(f"scraping: {data[i]}")

        if r.status_code != 404:
            soup = BeautifulSoup(r.content, 'html.parser')
            try:
                # Defining the HTMLTableParser object
                p = HTMLTableParser()
                # feeding the html contents in the  HTMLTableParser object
                p.feed(r.text)
                # membuat variabel yang menyimpan semua tabel dalam soup
                tables = p.tables
                # membuat list teks pengganti
                replacement_texts = []
                # retrieve all captions
                captions = soup.find_all('caption')
                captions_text = []
                for item in captions:
                    captions_text.append(item.text)
                for k in range(len(tables)):
                    replacement_text = create_table(data=tables[k], caption=captions_text[k])
                    replacement_texts.append(replacement_text)
                # Mengganti setiap tabel dengan teks pengganti yang sesuai
                table_tags = soup.find_all('table')
                for j, table_tag in enumerate(table_tags):
                    table_tag.replace_with(replacement_texts[j])

                main_content = str(soup.find('div', class_='content-main-wrap ato-content').find_next('div', class_='widgetBody'))

                numbering_ol = renumber_olist(main_content)
                numbering_ul = renumber_ulist(numbering_ol)
                clean_text = remove_tags(numbering_ul)
                # Open the file in write mode
                file_name = f"{name}_{i}.txt"
                folder_path = f"./{name}"  # Replace with the desired folder path
                # Create the folder if it doesn't exist
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                # Create the file inside the folder
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    # Write the content to the file
                    file.write(clean_text)
                    print(f"{file_name} successfully created")
            except:
                print("no article")
        else:
            print(f"err 404 : {name}_{i}")
        sleep(1)
