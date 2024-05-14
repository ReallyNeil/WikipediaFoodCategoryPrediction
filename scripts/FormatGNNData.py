import os.path
import json
import torch
from torch_geometric.data import Data
from torch_geometric.transforms import RemoveDuplicatedEdges
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance

def get_categories_from_json(file):
    with open(file, 'r') as f:
        data = json.load(f)

    categories = [key.split(":")[1] for key in data.keys()]
    return categories

# def get_articles_from_json(file, categories, n):
def get_articles_from_json(file, categories):
    with open(file, 'r') as f:
        data = json.load(f)
    # data = dict(list(data.items())[:n])

    articles = [key for key in data.keys()]
    article_pages = []
    article_categories = []
    for _, value in data.items():
        article_pages.append(value['pages'])
        article_categories.append([category.split(":")[1] for category in value['categories']])

    indices = []
    for i in range(len(articles)):
        for j in range(len(article_categories[i])):
            if article_categories[i][j] in categories:
                indices.append(i)
    indices = list(set(indices))
    indices.sort()

    articles = [articles[i] for i in indices]
    article_pages = [article_pages[i] for i in indices]
    article_categories = [article_categories[i] for i in indices]

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

def get_sentence_embeddings(articles):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    sentence_embeddings = model.encode(articles)    
    embeddings_dict = dict(zip(articles, sentence_embeddings))
    return embeddings_dict

def get_cosine_sim(article1, article2, embeddings_dict):
    embedding1 = embeddings_dict[article1]
    embedding2 = embeddings_dict[article2]

    cosine_sim = 1 - distance.cosine(embedding1, embedding2)
    return cosine_sim

def create_x(articles, embeddings_dict):
    return torch.tensor([embeddings_dict[a] for a in articles], dtype=torch.float)

def create_edges(articles, article_links, embeddings_dict):
    start, end, weight = [], [], []
    for i in range(len(article_links)):
        for j in range(len(article_links[i])):
            idx = articles.index(article_links[i][j])
            cosine_sim = get_cosine_sim(articles[i], articles[idx], embeddings_dict)

            if cosine_sim > 0.5:
                start.append(i)
                end.append(idx)
                weight.append(cosine_sim)

                start.append(idx)
                end.append(i)
                weight.append(cosine_sim)

    edge_index = torch.tensor([start, end], dtype=torch.long)
    edge_attr = torch.tensor(weight, dtype=torch.float)
    return edge_index, edge_attr

def create_y(categories, article_categories):
    return torch.tensor([[a.count(c) for c in categories] for a in article_categories], dtype=torch.float)

def create_data(categories, articles, articles_links, article_categories):
    embeddings_dict = get_sentence_embeddings(articles)
    x = create_x(articles, embeddings_dict)
    edge_index, edge_attr = create_edges(articles, articles_links, embeddings_dict)
    y = create_y(categories, article_categories)
    data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y, articles=articles, categories=categories)
    transform = RemoveDuplicatedEdges()
    return transform(data)

if __name__ == '__main__':
    path = os.path.dirname(__file__)

    # n = 200
    # n = 500
    # categories = get_categories_from_json(path + '/../data/categoryfreq.json')
    # articles, articles_links, article_categories = get_articles_from_json(path + '/../data/sample.json', categories, n)
    categories = get_categories_from_json(path + '/../data/categoryfreq.json')
    articles, articles_links, article_categories = get_articles_from_json(path + '/../data/sample.json', categories)

    data = create_data(categories, articles, articles_links, article_categories)
    # torch.save(data, path + '/../data/sample_GNN_data_high_cosine.pt')
    # torch.save(data, path + '/../data/large_sample_GNN_data_node_feature.pt')
    torch.save(data, path + '/../data/GNN_data_high_cosine.pt')