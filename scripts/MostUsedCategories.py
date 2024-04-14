#Scrapes all food articles and saves content and external links to a text file in data/articles. 
import wikipediaapi
import json 

wiki_wiki = wikipediaapi.Wikipedia('WikipediaFoodCategoryIngredients (nae28@cornell.edu)', 'en')

#Create list of all categories in the class

possible_categories = set()
def find_categorymembers(categorymembers, level=0, max_level=8):
    for c in categorymembers.values():
        possible_categories.add(c.title)
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            find_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)


cat_name = "Category:Foods_by_cooking_technique"
cat = wiki_wiki.page(cat_name) 
print("Category members: " + cat_name)
find_categorymembers(cat.categorymembers)
print(possible_categories)


#Report category
category_frequncy_dict = {
    
}

def print_categorymembers(categorymembers, level=0, max_level=2):
    for c in categorymembers.values():
        print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        for cat in c.categories:
            if cat in category_frequncy_dict and cat in possible_categories:
                category_frequncy_dict[cat] +=1 
            else:
                category_frequncy_dict[cat] = 1
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)



print_categorymembers(cat.categorymembers)
print(category_frequncy_dict)

with open("data/categoryfreq.json", "w") as outfile: 
    json.dump(category_frequncy_dict, outfile, indent=4)