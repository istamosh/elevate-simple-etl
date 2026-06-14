import json

from utils.transform import (
    is_valid_price,
    filter_unknown_product,
    deduplicate_items,
    transform_price_to_idr,
    transform_rating,
    clean_size_gender,
)

EXTRACTED_FILE = "extracted_data.json"
CLEANED_FILE = "cleaned_data.json"
TRANSFORMED_FILE = "transformed_data.json"


def run_transform(
    input_file: str = EXTRACTED_FILE,
    cleaned_file: str = CLEANED_FILE,
    output_file: str = TRANSFORMED_FILE,
):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_price = [item for item in data if is_valid_price(item)]
    cleaned_title = filter_unknown_product(cleaned_price)
    unique = deduplicate_items(cleaned_title)

    with open(cleaned_file, "w", encoding="utf-8") as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)

    for entry in unique:
        transform_price_to_idr(entry)
        transform_rating(entry)
        clean_size_gender(entry)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(unique)} transformed records to {output_file}")
    return unique


def main():
    run_transform()


if __name__ == "__main__":
    main()