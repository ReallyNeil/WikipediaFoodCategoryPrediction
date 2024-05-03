#Scrapes all food articles and saves content and external links to a text file in data/articles. 
import wikipediaapi
import json 

wiki_wiki = wikipediaapi.Wikipedia('WikipediaFoodCategoryIngredients (nae28@cornell.edu)', 'en')

article_name_dict = {
    
}
possible_categories_pages = set()
def find_categorymembers(categorymembers, level=0, max_level=8):
    for c in categorymembers.values():
        possible_categories_pages.add(c.title)
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            find_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)


cat_name = "Category:Foods_by_cooking_technique"
cat = wiki_wiki.page(cat_name) 
print("Category members: " + cat_name)
find_categorymembers(cat.categorymembers)
print(possible_categories_pages)

def print_categorymembers(categorymembers, level=0, max_level=2):
    for c in categorymembers.values():
        print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        title = c.title 
        
        body = c.text
        categories = []
        pages = []
        for title in c.links.keys():
            if title in possible_categories_pages:
                pages.append(title)
        for cat in c.categories.keys():
            if cat in possible_categories_pages:
                categories.append(cat)
        subDict = {
            "body": body,
            "pages": pages,
            "categories": categories
        }
        article_name_dict[title] = subDict
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)



print_categorymembers(cat.categorymembers)
print(article_name_dict)

with open("data/sample.json", "w") as outfile: 
    json.dump(article_name_dict, outfile, indent=4)