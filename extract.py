from bs4 import BeautifulSoup as bs

def build_urls():
    return ['https://fashion-studio.dicoding.dev/'] + [f'https://fashion-studio.dicoding.dev/page{i}' for i in range(2, 51)]

def parse_product_card(item):
    title = item.find(class_="product-title").get_text(strip=True)
    price = item.find(class_="price").get_text(strip=True)

    ps = item.find_all("p")
    rating = ps[0].get_text(strip=True)
    color = ps[1].get_text(strip=True)
    size = ps[2].get_text(strip=True)
    gender = ps[3].get_text(strip=True)

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "color": color,
        "size": size,
        "gender": gender,
    }

def parse_page(html):
    soup = bs(html, "html.parser")
    items = soup.find_all(class_="product-details")
    return [parse_product_card(item) for item in items]