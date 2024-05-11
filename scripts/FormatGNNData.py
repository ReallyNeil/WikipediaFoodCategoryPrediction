import os.path
import json
import torch
from torch_geometric.data import Data
from torch_geometric.transforms import RemoveDuplicatedEdges

def get_categories_from_json(file):
    with open(file, 'r') as f:
        data = json.load(f)

    categories = [key.split(":")[1] for key in data.keys()]
    return categories

def get_articles_from_json(file, n):
    with open(file, 'r') as f:
        data = json.load(f)
    data = dict(list(data.items())[:n])

    articles = [key for key in data.keys()]
    article_pages = []
    article_categories = []
    for _, value in data.items():
        article_pages.append(value['pages'])
        categories = [category.split(":")[1] for category in value['categories']]
        article_categories.append(categories)

    article_links = []
    indices = []
    for i in range(len(article_pages)):
        article_links.append([])
        for j in range(len(article_pages[i])):
            if article_pages[i][j] in articles:
                article_links[i].append(article_pages[i][j])
                indices.append(i)
                indices.append(articles.index(article_pages[i][j]))
    indices = list(set(indices))
    indices.sort()

    articles = [articles[i] for i in indices]
    article_links = [article_links[i] for i in indices]
    article_categories = [article_categories[i] for i in indices]

    return articles, article_links, article_categories

def create_x(n):
    return torch.tensor([[] for _ in range(n)], dtype=torch.float)

def create_edge_index(articles, article_links):
    start, end = [], []
    for i in range(len(article_links)):
        for j in range(len(article_links[i])):
            idx = articles.index(article_links[i][j])
            start.append(i)
            end.append(idx)
            start.append(idx)
            end.append(i)
    return torch.tensor([start, end], dtype=torch.long)

def create_y(categories, article_categories):
    return torch.tensor([[a.count(c) for c in categories] for a in article_categories], dtype=torch.float)

def create_data(categories, articles, articles_links, article_categories):
    x = create_x(len(articles))
    edge_index = create_edge_index(articles, articles_links)
    y = create_y(categories, article_categories)
    data = Data(x=x, edge_index=edge_index, y=y)

    transform = RemoveDuplicatedEdges()
    return transform(data)

if __name__ == '__main__':
    path = os.path.dirname(__file__)

    n = 200
    categories = get_categories_from_json(path + '/../data/categoryfreq.json')
    articles, articles_links, article_categories = get_articles_from_json(path + '/../data/sample.json', n)

    data = create_data(categories, articles, articles_links, article_categories)
    torch.save(data, path + '/../data/sample_GNN_data.pt')