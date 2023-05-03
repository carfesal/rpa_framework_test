import re
import requests
import os
import zipfile
import glob
from src.util.logging import logger

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
    return os.path.basename(scheme_removed)

def download_image(url:str, filename:str, folder:str="./output")-> str:
    ''' Download an image
    :param url: url of the image
    :param filename: filename to save the image as
    :param folder: folder to save the image in
    :return: path to the image
    '''
   
    if not os.path.exists(folder):
        os.makedirs(folder)
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder, filename), "wb") as f:
            f.write(response.content)
    return os.path.join(folder, filename)

def check_if_text_contains_money(text:str)-> bool:
    '''
    Check if the text contains money
    :param text: text to check
    :return: True if the text contains money, False otherwise
    '''
    if text is None:
        return False
    return re.search(r"(\$(\d{1,3}(\,\d{3})*|(\d+))(\.\d+)?)|((\d{1,3}(\,\d{3})*|(\d+))(\.\d+)? (dollars|USD))", text) is not None

def zip_folder(folder:str = "./output/images", output:str = "./output/compressed.zip")-> str:
    '''
    Zip a folder
    :param folder: folder to zip
    :param output: output file
    :return: path to the zip file
    '''
    with zipfile.ZipFile(output, 'w') as f:
        for file in glob.glob(folder + '/*'):
            f.write(file)
    return output

def get_size_of_file(filename:str)-> int:
    '''
    Get the size of a file
    :param filename: filename to get the size of
    :return: size of the file
    '''
    return os.path.getsize(filename)

def get_size_of_folder(folder:str = "./output")-> int:
    '''
    Get the size of a folder
    :param folder: folder to get the size of
    :return: size of the folder
    '''
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def print_variables(title:str = "**ENV VARIABLES**", variables:dict = {})-> None:
    '''
    Print the variables
    :param variables: variables to print
    :return: None
    '''
    logger.info(title)
    if variables is None:
        return
    for key, value in variables.items():
        logger.info(f"{key}: {value}")

