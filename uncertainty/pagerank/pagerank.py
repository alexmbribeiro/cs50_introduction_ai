import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    probabilities = dict()

    # Choose a link at random, chosen from all pages in the corpus
    for key, values in corpus.items():
        if key not in probabilities.keys():
            probabilities[key] = (1 - damping_factor)/len(corpus.keys())


    # Choose a link at random linked to by `page`
    for key, values in corpus.items():
        if key == page:
            for value in values:
                random_probability = probabilities[value]
                probabilities[value] = random_probability + (damping_factor * 1/len(values))

    return probabilities

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # start PR dictionary with the keys, and count to 0
    page_rank = dict()

    for key in corpus:
        page_rank[key] = 0

    # get all pages
    keys = list(corpus.keys())

    # choose first page randomly and add it to the PR count
    random_key = random.choices(list(keys))[0]
    page_rank[random_key] += 1

    # iterate n times
    for _ in range(0, n):

        # empty weights
        weights = []

        # get transition model of current page
        transition_mod = transition_model(corpus, random_key, damping_factor)

        # get weights for each of possible link
        for key in transition_mod:
            weights.append(transition_mod[key])

        # select random page, taking into count the probability of each link
        random_key = random.choices(list(transition_mod.keys()), weights=weights, k=1)[0]

        # add it to the PR count
        page_rank[random_key] += 1

    # divide by n to get probability of each page
    for key in page_rank:
        page_rank[key] /= n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    threshold=0.001
    N = len(corpus)
    page_rank = {page: 1 / N for page in corpus}

    for page in corpus:
        if not corpus[page]: 
            corpus[page] = set(corpus.keys())

    while True:
        new_rank = {}
        for page in corpus:
            rank = (1 - damping_factor) / N

            for other_page in corpus:
                if page in corpus[other_page]:
                    rank += damping_factor * page_rank[other_page] / len(corpus[other_page])

            new_rank[page] = rank

        if all(abs(new_rank[page] - page_rank[page]) < threshold for page in page_rank):
            break

        page_rank = new_rank

    total_rank = sum(page_rank.values())
    page_rank = {page: rank / total_rank for page, rank in page_rank.items()}

    return page_rank

if __name__ == "__main__":
    main()
