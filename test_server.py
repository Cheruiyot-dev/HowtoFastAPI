import requests
# response = requests.get("http://127.0.0.1:8000/items?name=Nails")
# print(response.status_code)
# print(response.text)


# print(requests.get("http://127.0.0.1:8000/items/0").json())
# print(requests.get("http://127.0.0.1:8000/items?name=Nails").json())

# print("Adding an item")
# print(requests.post("http://127.0.0.1:8000/",
#       json={"name": "Screwdriver", "price": 4.89, "count": 23, "id": 4,
#             "category": "tools"},
#       ).json())

# print("Getting all items")
# print(requests.get("http://127.0.0.1:8000/").json())
# print()

# print("Updating an item:")
# print(requests.put("http://127.0.0.1:8000/items/1?count=67").json())
# print(requests.get("http://127.0.0.1:8000/").json())
# print()


print("Deleting an item:")
print(requests.delete("http://127.0.0.1:8000/items/1").json())
print(requests.get("http://127.0.0.1:8000/").json())
print()
