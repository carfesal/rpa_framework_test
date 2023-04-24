import re
import os.path as path
def count_of_ocurrences_in_text(text:str, word:str):
    if text is None or word is None:
        return 0
    return text.lower().count(word.lower())

def get_filename(url:str)-> str:
    '''Get the filename from a url
    :param url: url to get the filename from
    :return: filename
    '''
    if url is None:
        return None
    
    fragment_removed = url.split("#")[0] # remove fragment
    query_string_removed = fragment_removed.split("?")[0] # remove query string
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    if scheme_removed.find("/") == -1:
        return None
    return path.basename(scheme_removed)

def format_date(date:str, format:str="%m/%d/%Y")-> str:
    '''Format a date
    :param date: date to format
    :param format: format to use
    :return: formatted date
    '''
    return date.strftime(format)

def download_image(url:str, filename:str, folder:str="images")-> str:
    '''Download an image
    :param url: url of the image
    :param filename: filename to save the image as
    :param folder: folder to save the image in
    :return: path to the image
    '''
    import requests
    import os.path as path
    import os
    if not path.exists(folder):
        os.makedirs(folder)
    response = requests.get(url)
    if response.status_code == 200:
        with open(path.join(folder, filename), "wb") as f:
            f.write(response.content)
    return path.join(folder, filename)

def check_if_text_contains_money(text:str)-> bool:
    '''Check if the text contains money
    :param text: text to check
    :return: True if the text contains money, False otherwise
    '''
    if text is None:
        return False
    return re.search(r"(\$(\d{1,3}(\,\d{3})*|(\d+))(\.\d+)?)|((\d{1,3}(\,\d{3})*|(\d+))(\.\d+)? (dollars|USD))", text) is not None