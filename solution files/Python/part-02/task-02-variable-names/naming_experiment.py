from typing import List


class Product:
    def __init__(self, name: str) -> None:
        self.name = name


def process(d):
    # return the result
    return d


def extract_product_names(products: List[Product]) -> List[str]:
    # iterate over products and return a list of each product's name
    return [product.name for product in products]
