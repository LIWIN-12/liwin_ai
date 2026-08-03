from backend.rag import search

query = input("Ask something: ")

results = search(query)

print("\nResults:\n")

for i, doc in enumerate(results, start=1):
    print(f"Result {i}")
    print("-" * 40)
    print(doc)
    print()