import argparse
import os
import json
from datetime import datetime

def is_valid_flight_id(x):
    return x.isalnum() and 2 <= len(x) <= 8

def is_valid_airport(x):
    return len(x) == 3 and x.isalpha() and x.isupper()

def is_valid_datetime(x):
    try:
        datetime.strptime(x, "%Y-%m-%d %H:%M")
        return True
    except:
        return False

def is_chronological(dep, arr):
    d = datetime.strptime(dep, "%Y-%m-%d %H:%M")
    a = datetime.strptime(arr, "%Y-%m-%d %H:%M")
    return a > d

def is_valid_price(x):
    try:
        return float(x) >= 0
    except:
        return False

def parse_csv(path):
    valid = []
    invalid = []

    if not os.path.exists(path):
        return valid, invalid

    with open(path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    header = lines[0]
    rows = lines[1:]

    for line in rows:
        parts = line.split(",")
        if len(parts) != 6:
            invalid.append((line, "wrong number of fields"))
            continue

        flight_id, origin, dest, dep, arr, price = parts

        if not is_valid_flight_id(flight_id):
            invalid.append((line, "invalid flight_id"))
            continue

        if not is_valid_airport(origin):
            invalid.append((line, "invalid origin"))
            continue

        if not is_valid_airport(dest):
            invalid.append((line, "invalid destination"))
            continue

        if not is_valid_datetime(dep):
            invalid.append((line, "invalid departure datetime"))
            continue

        if not is_valid_datetime(arr):
            invalid.append((line, "invalid arrival datetime"))
            continue

        if not is_chronological(dep, arr):
            invalid.append((line, "arrival before departure"))
            continue

        if not is_valid_price(price):
            invalid.append((line, "invalid price"))
            continue

        valid.append({
            "flight_id": flight_id,
            "origin": origin,
            "destination": dest,
            "departure_datetime": dep,
            "arrival_datetime": arr,
            "price": float(price)
        })

    return valid, invalid

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def save_errors(path, errors):
    with open(path, "w", encoding="utf-8") as f:
        for line, reason in errors:
            f.write(f"{reason}: {line}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    args = parser.parse_args()

    valid, invalid = parse_csv(args.input)

    os.makedirs("output", exist_ok=True)

    save_json("output/valid.json", valid)
    save_errors("output/errors.txt", invalid)

    print("Valid rows:", len(valid))
    print("Invalid rows:", len(invalid))

if __name__ == "__main__":
    main()
