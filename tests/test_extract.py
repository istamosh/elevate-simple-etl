from bs4 import BeautifulSoup as bs
from utils.extract import build_urls, parse_product_card, parse_page

def test_build_urls():
    urls = build_urls()
    assert len(urls) == 50
    assert urls[0] == "https://fashion-studio.dicoding.dev/"
    assert urls[-1] == "https://fashion-studio.dicoding.dev/page50"

def test_parse_product_card():
    html = """
    <div class="product-details">
        <h3 class="product-title">Hoodie 999</h3>
        <div class="price-container"><span class="price">$533.39</span></div>
        <p>Rating: ⭐ 4.8 / 5</p>
        <p>3 Colors</p>
        <p>Size: XL</p>
        <p>Gender: Unisex</p>
    </div>
    """
    soup = bs(html, "html.parser")
    item = soup.find(class_="product-details")
    result = parse_product_card(item)

    assert result["title"] == "Hoodie 999"
    assert result["price"] == "$533.39"
    assert result["rating"] == "Rating: ⭐ 4.8 / 5"
    assert result["color"] == "3 Colors"
    assert result["size"] == "Size: XL"
    assert result["gender"] == "Gender: Unisex"

def test_parse_page_multiple_cards():
    html = """
    <div class="product-details">
        <h3 class="product-title">T-shirt 2</h3>
        <span class="price">$102.15</span>
        <p>Rating: ⭐ 3.9 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Women</p>
    </div>
    <div class="product-details">
        <h3 class="product-title">Hoodie 3</h3>
        <span class="price">$496.88</span>
        <p>Rating: ⭐ 4.8 / 5</p>
        <p>3 Colors</p>
        <p>Size: L</p>
        <p>Gender: Unisex</p>
    </div>
    """
    result = parse_page(html)
    assert len(result) == 2
    assert result[0]["title"] == "T-shirt 2"
    assert result[1]["title"] == "Hoodie 3"

def test_parse_page_empty():
    assert parse_page("<html></html>") == []