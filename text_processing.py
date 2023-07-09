import re
from html_table_parser.parser import HTMLTableParser

def remove_tags(text):
    # Remove all HTML tags using regex
    clean_text = re.sub('<.*?>', '', text)
    return clean_text


def renumber_ulist(text):
    # remove hidden text
    text = re.sub(r'<span[^>]*hidden[^>]*>.*?</span>', '', text)
    # Delete the "on this page" text
    text = re.sub(r'<p><b>On this page:</b></p>\s*<ul>.*?</ul>', '', text, flags=re.DOTALL)
    # remove hidden tag
    text = re.sub(r'<div class="callout attention hidePrevious">.*?</div>', '', text, flags=re.DOTALL)
    # remove see also text
    text = re.sub(r'<p><b>See also:</b></p>\s*<ul>.*?</ul>', '', text, flags=re.DOTALL)

    # Search for all <ul> tags and their contents
    ul_pattern = r'<ul>(.*?)<\/ul>'
    ul_matches = re.findall(ul_pattern, text, re.DOTALL)
    for ul_match in ul_matches:
        ul_match_old = ul_match
        # Replacing <li> tags with numbers
        li_pattern = r'<li>(.*?)<\/li>'
        li_matches = re.findall(li_pattern, ul_match)
        for i, li_match in enumerate(li_matches, start=1):
            # Replace the <li> element with a number and cleaned text
            numbered_li = f'{i}. {remove_tags(li_match.strip())}'
            ul_match = ul_match.replace(f'<li>{li_match}</li>', f'<li>{numbered_li}</li>')
        text = text.replace(f'<ul>{ul_match_old}</ul>', f'<ul>{ul_match}</ul>', 1).strip()
    return text


def renumber_sub_olist(text, index):
    index = int(index)
    ul_pattern = r'<ul>(.*?)<\/ul>'
    ul_matches = re.findall(ul_pattern, text, re.DOTALL)
    for ul_match in ul_matches:
        ul_match_old = ul_match
        # change tag <li> with a number
        li_pattern = r'<li>(.*?)<\/li>'
        li_matches = re.findall(li_pattern, ul_match)
        for i, li_match in enumerate(li_matches, start=1):
            # Replace the <li> element with a number and cleaned text
            numbered_li = f'{index}.{i}. {remove_tags(li_match.strip())}'
            ul_match = ul_match.replace(f'<li>{li_match}</li>', f'{numbered_li}') # disini tag li dihapus
        text = text.replace(f'<ul>{ul_match_old}</ul>', f'<ul>{ul_match}</ul>', 1).strip()
    return text


def renumber_olist(text):
    ol_attr = r'<ol\s+start="(\d+)"' # start attribute of ol tag
    ol_attr_matches = re.findall(ol_attr, text)
    ol_attr_matches.insert(0, "1")
    # find ol pattern
    ol_pattern = r'<ol\b[^>]*>(.*?)<\/ol>'
    ul_pattern = r'<\/?ul>'
    ol_matches = re.findall(ol_pattern, text, re.DOTALL)

    for index, ol_match in enumerate(ol_matches):
        ol_match_old = ol_match
        ol_match = renumber_sub_olist(text=ol_match, index=ol_attr_matches[index]) # numbering list inside ul tag
        ol_match = re.sub(ul_pattern, '', ol_match, flags=re.DOTALL) # remove ul tag
        li_pattern = r'<li>(.*?)</li>'
        li_matches = re.findall(li_pattern, ol_match, re.DOTALL)

        for i, li_match in enumerate(li_matches, start=int(ol_attr_matches[index])):
            numbered_li = f'{i}. {remove_tags(li_match.strip())}'
            ol_match = ol_match.replace(f'<li>{li_match}</li>', f'<li>{numbered_li}</li>')

        # replace element inside ol tags with numbered list
        text = text.replace(f'<ol start="{int(ol_attr_matches[index])}">{ol_match_old}</ol>', f'<ol>{ol_match}</ol>', 1).strip()
        text = text.replace(f'<ol>{ol_match_old}</ol>', f'<ol>{ol_match}</ol>', 1).strip()
    return text


def create_table(data, caption):
    # Determine the maximum length of each column
    max_lengths = [max(len(str(item)) for item in column) for column in zip(*data)]
    # caption =
    # Generate the table structure
    table = ''
    for row in data:
        table += ' | '.join(f'{str(item):<{max_len}}' for item, max_len in zip(row, max_lengths))
        table += '\n'
    table = "\n" + caption + "\n" + table
    return table


