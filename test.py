from models.embedding_model import EmbeddingModel

from document_categories.vectordb_document_categories.chunked_documents.post_chunked_document import PostChunkedDocument
from document_categories.vectordb_document_categories.embedded_documents.embedded_post_document import EmbeddedPostDocument
from data_preprocessors.data_embedders.post_data_embedder import PostDataEmbedder
from uuid import UUID

from document_categories.rag_document_categories.query_document import Query

model=EmbeddingModel()


if __name__=="__main__":
    document_content="instead it drags on for five or ten. Being right stops meaning much when proving it takes a decade. He also mentioned that the pain of growing a business is higher in India than in the US or other Western democracies. The cost isn't the tax rate. It's what an honest business spends defending itself, and the years it loses waiting on a system that takes too long to decide. Full episode out now, watch here:"

    post_doc=PostChunkedDocument(
        content=document_content
    )

    embedded_doc=PostDataEmbedder().embed(chunk=post_doc)

    similar_docs=EmbeddedPostDocument.search(
        query_vector=embedded_doc.embedding,
        limit=3
    )

    for ind,doc in enumerate(similar_docs):
        print(f"Doc: {ind}")
        print(f"Platform: {doc.platform}")
        print(f"Published Date: {doc.published_date}")
        print(f"Content: {doc.content}")
        print(50*"-")