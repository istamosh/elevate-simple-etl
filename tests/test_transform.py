from utils.transform import (
    is_valid_price,
    filter_unknown_product,
    deduplicate_items,
    transform_price_to_idr,
    transform_rating,
    clean_size_gender,
)

def test_is_valid_price_valid_string():
    assert is_valid_price({"price": "$102.15"}) is True

def test_is_valid_price_unavailable():
    assert is_valid_price({"price": "Price Unavailable"}) is False

def test_is_valid_price_empty():
    assert is_valid_price({"price": ""}) is False

def test_is_valid_price_numeric():
    assert is_valid_price({"price": 150000}) is True

def test_is_valid_price_bad_string():
    assert is_valid_price({"price": "$abc"}) is False

def test_filter_unknown_product():
    items = [
        {"title": "Unknown Product"},
        {"title": "T-shirt 2"},
    ]
    result = filter_unknown_product(items)
    assert len(result) == 1
    assert result[0]["title"] == "T-shirt 2"

def test_deduplicate_items_same_title_size_gender():
    items = [
        {"title": "T-shirt 2", "size": "M", "gender": "Women"},
        {"title": "T-shirt 2", "size": "M", "gender": "Women"},
    ]
    result = deduplicate_items(items)
    assert len(result) == 1

def test_deduplicate_items_keep_different_size():
    items = [
        {"title": "T-shirt 2", "size": "M", "gender": "Women"},
        {"title": "T-shirt 2", "size": "L", "gender": "Women"},
    ]
    result = deduplicate_items(items)
    assert len(result) == 2

def test_transform_price_to_idr():
    item = {"price": "$100.00"}
    result = transform_price_to_idr(item.copy())
    assert result["price"] == 1600000

def test_transform_rating_string():
    item = {"rating": "Rating: ⭐ 4.8 / 5"}
    result = transform_rating(item.copy())
    assert result["rating"] == 4.8

def test_transform_rating_already_float():
    item = {"rating": 4.8}
    result = transform_rating(item.copy())
    assert result["rating"] == 4.8

def test_transform_rating_invalid():
    item = {"rating": "Rating: ⭐ Invalid Rating / 5"}
    result = transform_rating(item.copy())
    assert result["rating"] is None

def test_clean_size_gender():
    item = {"size": "Size: XL", "gender": "Gender: Unisex"}
    result = clean_size_gender(item.copy())
    assert result["size"] == "XL"
    assert result["gender"] == "Unisex"