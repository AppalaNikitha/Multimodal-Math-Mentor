from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from pathlib import Path

class VectorStore:
    def __init__(self, db_path="embeddings/vector_store.faiss"):
        self.db_path = Path(db_path)
        self.embeddings = OpenAIEmbeddings()
        self.store = None
        self.load_index()

    def load_index(self):
        if self.db_path.exists():
            self.store = FAISS.load_local(str(self.db_path), self.embeddings)

    def build_index(self, knowledge_base_folder):
        """
        Rebuild FAISS index from knowledge base after feedback updates.
        """
        from langchain.text_splitter import CharacterTextSplitter
        from langchain.docstore.document import Document

        docs = []
        for file in Path(knowledge_base_folder).glob("*.txt"):
            content = file.read_text()
            splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_text(content)
            for chunk in chunks:
                docs.append(Document(page_content=chunk, metadata={"source": str(file)}))

        self.store = FAISS.from_documents(docs, self.embeddings)
        self.store.save_local(str(self.db_path))

    def retrieve(self, query, k=3):
        if not self.store:
            return []
        return self.store.similarity_search(query, k=k)
