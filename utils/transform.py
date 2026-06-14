import re

def is_valid_price(item):
    price = item.get("price", "")
    if isinstance(price, int):
        return price > 0
    if isinstance(price, str):
        # longkapi string "Price Unavailable", kosong, dan teks invalid
        if not price or "Unavailable" in price or price.startswith("Price Unavailable"):
            return False
        # coba parsing string mata uang
        try:
            val = float(price.replace("$", ""))
            return val > 0
        except ValueError:
            return False
    return False

def filter_unknown_product(items):
    return [item for item in items if item.get("title") != "Unknown Product"]

def deduplicate_items(items):
    seen = set()
    unique = []
    for item in items:
        key = (
            item.get("title"),
            item.get("size"),
            item.get("gender")
        )
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique

def transform_price_to_idr(item, rate=16000):
    price_str = item["price"]
    price_num = float(price_str.replace("$", ""))
    item["price"] = int(price_num*rate)
    return item

def transform_rating(item):
    rating_val = item.get("rating")
    # kalau sudah berupa float, keluar fungsi
    if isinstance(rating_val, float):
        return item
    # ekstrak floating point dari teks rating, jika tidak ada yang cocok, ubah menjadi none
    if isinstance(rating_val, str):
        match = re.search(r"⭐\s*([0-9]+(?:\.[0-9]+)?)\s*/", rating_val)
        # jika tidak ada rating valid, set ke None
        item["rating"] = float(match.group(1)) if match else None
    else:
        # jika tipe lain (None, int, etc), set ke None
        item["rating"] = None
    return item

def clean_size_gender(item):
    if isinstance(item.get("size"), str):
        item["size"] = item["size"].replace("Size: ", "").strip()
    if isinstance(item.get("gender"), str):
        item["gender"] = item["gender"].replace("Gender: ", "").strip()
    return item