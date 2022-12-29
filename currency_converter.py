import requests, json

x = input()
x = x.lower()

# getting data od currency rates
with requests.get(f"http://www.floatrates.com/daily/{x}.json") as r:
    diction = json.loads(r.text)

# creating cache
table = ["usd", "eur"]
if x in table:
    table.remove(x)
    cache = { table[0]: diction[table[0]]["rate"] }
else:
    cache = { "usd": diction["usd"]["rate"], "eur": diction["eur"]["rate"]}

#while loop that computes money
while(True):
    currency = input()
    if currency == '':
        break
    currency = currency.lower()
    n = float(input())
    print("Checking the cache...")
    if cache.get(currency) == None:
        print("Sorry, but it is not in the cache!")
        cache[currency] = diction[currency]["rate"]
    else:
        print("Oh! It is in the cache!")
    print(f"You received {n * float(cache[currency]):.2f} {currency.upper()}.")