import logging
import weaviate.classes as wvc
from .client import client

# Set up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_schema() -> None:
    existing_collections = await client.collections.list_all()
    
    if any(collection == "Images" for collection in existing_collections):
        logger.info("Schema for 'Images' already exists.")
        return 

    await client.collections.create(
        name="Images",
        vectorizer_config=wvc.config.Configure.Vectorizer.img2vec_neural(["image"]),
        vector_index_config=wvc.config.Configure.VectorIndex.hnsw(),
        properties=[
            wvc.config.Property(
                name="cpf",
                data_type=wvc.config.DataType.TEXT,
            ),
            wvc.config.Property(
                name="image",
                data_type=wvc.config.DataType.BLOB,
            ),
        ]
    )
    logger.info("Schema for 'Images' created successfully.")
