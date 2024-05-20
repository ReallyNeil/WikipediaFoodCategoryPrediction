#Scrapes all food articles and saves content and external links to a text file in data/articles. 
import wikipediaapi
import json 


wiki_wiki = wikipediaapi.Wikipedia('WikipediaFoodCategoryIngredients (nae28@cornell.edu)', 'en')

article_name_dict = {
    
}

cat_name = "Category:Foods_by_cooking_technique"
cat = wiki_wiki.page(cat_name) 

with open('data/categoryfreq.json', 'r') as file:
    data = json.load(file)

possible_categories_pages = set(data.keys())

removed_sections = ['See also', 'References','External Links']

print(possible_categories_pages)

def print_categorymembers(categorymembers, level=0, max_level=4):
    for c in categorymembers.values():
        print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        title = c.title 
        body = c.text
        pages = set()
        categories = []
        for section in c.sections:
            if section.title in removed_sections:
                continue
            print(section.title)
            for page_title in section.links.keys():
                pages.add(page_title)
            for cat in section.categories.keys():
                if cat in possible_categories_pages:
                    categories.add(cat)
        subDict = {
            "body": body,
            "pages": list(pages),
            "categories": categories
        }
        article_name_dict[title] = subDict
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)



print_categorymembers(cat.categorymembers)
print(article_name_dict)

with open("data/sample.json", "w") as outfile: 
    json.dump(article_name_dict, outfile, indent=4)