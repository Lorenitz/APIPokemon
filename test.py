url = "https://example.com/" + first_id

A = json.load(urllib.urlopen(url))
print(A)