from functools import reduce
from typing import List, Set


def reduce_list_of_urls(urls: List[Set[str]]) -> Set[str]:
    return reduce(lambda x, y: x | y, urls, set())
