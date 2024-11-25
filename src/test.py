from weaviate import Client

# Connect to Weaviate
client = Client(url="http://localhost:8080")

# Inspect the schema
schema = client.schema.get()
print("Schema:", schema)
