#Scrapes all food articles and saves content and external links to a text file in data/articles. 
import wikipediaapi
import json 
import requests 
import re

wiki_wiki = wikipediaapi.Wikipedia('WikipediaFoodCategoryIngredients (nae28@cornell.edu)', 'en')

article_name_dict = {
    
}

cat_name = "Category:Foods_by_cooking_technique"
cat = wiki_wiki.page(cat_name) 

with open('data/categoryfreq.json', 'r') as file:
    data = json.load(file)
possible_categories_pages = set(data.keys())


def get_internal_links_from_content(title):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    # Set the parameters for the query
    PARAMS = {
        "action": "parse",
        "page": title,
        "format": "json",
        "prop": "wikitext"
    }

    response = S.get(url=URL, params=PARAMS)
    data = response.json()

    wikitext = data["parse"]["wikitext"]["*"]

    # Regular expression to find links in wikitext
    link_pattern = re.compile(r'\[\[(?!File:|Category:)([^|\]]+?)(?:\|.*?)?\]\]')
    links = link_pattern.findall(wikitext)

    # Clean and format link names
    clean_links = [link.split('#')[0].replace('_', ' ').strip() for link in links]
    
    # Filter duplicates
    unique_links = list(set(clean_links))

    return unique_links


def print_categorymembers(categorymembers, level=0, max_level=4):
    for c in categorymembers.values():
        print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        title = c.title 
        body = c.text
        categories = []
        for cat in c.categories.keys():
            if cat in possible_categories_pages:
                categories.append(cat)
        pages = get_internal_links_from_content(title)
        subDict = {
            "body": body,
            "pages": pages,
            "categories": categories
        }
       # print(pages)
        article_name_dict[title] = subDict
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)



print_categorymembers(cat.categorymembers)
print(article_name_dict)

with open("data/sample.json", "w") as outfile: 
    json.dump(article_name_dict, outfile, indent=4)


