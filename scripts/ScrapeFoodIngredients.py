#Scrapes all food articles and saves content and external links to a text file in data/articles. 
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('WikipediaFoodCategoryIngredients (nae28@cornell.edu)', 'en')



def print_categorymembers(categorymembers, level=0, max_level=2):
        for c in categorymembers.values():
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)
cat_name = "Category:Foods_by_cooking_technique"
cat = wiki_wiki.page(cat_name)
print("Category members: " + cat_name)
print_categorymembers(cat.categorymembers)