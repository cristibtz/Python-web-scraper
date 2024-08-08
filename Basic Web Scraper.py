import requests
import sys
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="HTML Tag Finder", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--tag", required=True, help="HTML Tag --> example: h4, p, script, etc.")
parser.add_argument("-u", "--url", required=True, help="Page URL --> example: http://some_random_url/resource")
parser.add_argument("-a", "--attribute", required=False, help="Get the value of an attribute of a given tag: if used -t img, use-a src")
parser.add_argument("-c", "--get-text", required=False, action='store_true', help="Get the text content of a given tag: just -c")
parser.add_argument("-d", "--get-text-adv", required=False, help="Get the text content of a tag with a given attribute; example: -d 'class=name'")
#To add output to file flag
parser.add_argument("-o", "--output", required=False, help="Write output to file: -o file.txt")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

#Get code and transform in soup
def getCode(url):
    request = requests.get(url, headers=headers)

    html_code = request.text

    soup = BeautifulSoup(html_code, "html.parser")

    return soup

#Search tag in given HTML code soup
def searchTag(tag, url):

    soup = getCode(url)

    result = soup.find_all(tag)

    if result:
        return result

#Get attribute value of a given tag
def searchAttr(tag_list, attribute):
    
    values = []

    if tag_list:
        for tag in tag_list:
            value = tag.get(attribute)
            if value != None:
                if isinstance(value, list):
                    value = ' '.join(value)
                values.append(value)

    return values

#Get the text between given tag
# -c and --get-text
def getText(tag_list):
    
    values = []

    if tag_list:
        for tag in tag_list:
            value = tag.get_text(separator='\n', strip=True)
            if value:
                values.append(value)

    return values

#Get the text of tags that have a certain attribute
# -d and --get-text-adv
def getTextAdvanced(tag_list, attribute_name, attribute_value):
    
    values = []

    if tag_list:
        for tag in tag_list:
            if tag.has_attr(attribute_name):
                if attribute_value in tag.get(attribute_name):
                    text = tag.get_text(separator='\n', strip=True).strip()
                    if text:  
                        values.append(text)

    return values

#Main code
if __name__ == "__main__":

    args = parser.parse_args()
    tag = args.tag
    url = args.url
    content = args.get_text
    content_adv = args.get_text_adv
    attribute = args.attribute

#Firstly, check optional flags
#Check if get tag content flag is set
    if content:

        values = getText(searchTag(tag, url))
        
        if values:
            for value in values:
                print(value)
        else: 
            print(f"No content in {tag} tag.")

#Check if get text advanced is flag is set
    elif content_adv :

        attribute_name, attribute_value = content_adv.split('=')

        values = getTextAdvanced(searchTag(tag, url), attribute_name.strip(), attribute_value.strip())

        if values:
            for value in values:
                print(value)
        else:
            print(f"Not {tag} tags with attribute value {content_adv} found on the page.")

#Check if get attribute value from tag is set 
    elif attribute != None:

        values = searchAttr(searchTag(tag, url), attribute)
        if values: 
            for value in values:
                print(value)
        else:
            print(f"No {tag} tags with attribute {attribute} found on the page.")

#Check if basic tag search is set
    elif tag != None:
        result = searchTag(tag, url)
        if result:
            for tag in result:
                print(tag)
        else:
            print(f"{tag} not found in the page.")


