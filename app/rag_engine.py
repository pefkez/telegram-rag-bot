from pathlib import Path

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

_user_indexes: dict[int, VectorStoreIndex] = {}


def _get_llm() -> OpenAI:
    return OpenAI(model="gpt-4o-mini", temperature=0)


def _get_embed_model() -> OpenAIEmbedding:
    return OpenAIEmbedding(model="text-embedding-3-small")


def index_document(user_id: int, file_path: str) -> int:
    from llama_index.core import SimpleDirectoryReader

    reader = SimpleDirectoryReader(input_files=[file_path])
    docs = reader.load_data()
    embed_model = _get_embed_model()
    index = VectorStoreIndex.from_documents(docs, embed_model=embed_model)
    _user_indexes[user_id] = index
    return len(docs)


def ask_question(user_id: int, question: str) -> tuple[str, list[str]]:
    index = _user_indexes.get(user_id)
    if not index:
        return "No documents uploaded yet. Send me a PDF first.", []

    llm = _get_llm()
    query_engine = index.as_query_engine(llm=llm, similarity_top_k=3)
    response = query_engine.query(question)

    sources = []
    for node in response.source_nodes:
        if hasattr(node.node, "metadata") and "file_name" in node.node.metadata:
            sources.append(node.node.metadata["file_name"])

    return str(response), sources
