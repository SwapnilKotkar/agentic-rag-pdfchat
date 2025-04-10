import os
from opensearchpy import OpenSearch
from dotenv import load_dotenv
from typing import Optional, Tuple

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "agent_db")


def craeteIndex(client, index_name):
    mapping = {
        "settings": {"index": {"knn": True}},  # Enable k-NN on the index level
        "mappings": {
            "properties": {
                "content": {"type": "text"},
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 768,  # ✔️ Correct keyword, no 'dims'
                },
            }
        },
    }

    # Create the index
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body=mapping)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")


def connectToOpensearch() -> Optional[Tuple[OpenSearch, str]]:
    client = OpenSearch(
        "https://localhost:9200",
        http_auth=("admin", "Swapnil@1234#"),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )

    index_name = "pdf_chunks_data"

    if client.ping():
        print("Connected to OpenSearch.")
        craeteIndex(client, index_name)
        return client, index_name
    else:
        print("Connection to OpenSearch failed.1111")
        return None
