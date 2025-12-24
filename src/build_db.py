# DB 구축용 스크립트

import json
import os
import chromadb
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from config import init_settings, DATA_DIR, DB_DIR

def load_json_data():
    documents = []
    # source 폴더 내의 모든 json 파일을 읽음
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    # 텍스트와 메타데이터를 분리하여 Document 객체 생성
                    doc = Document(
                        text=item["text"],
                        metadata=item.get("metadata", {})
                    )
                    documents.append(doc)
    return documents

def build():
    init_settings()
    print("데이터 로딩 중...")
    documents = load_json_data()
    print(f"총 {len(documents)}개의 데이터 청크를 찾았습니다.")

    # ChromaDB 연결 (영구 저장소)
    db = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db.get_or_create_collection("genshin_lore")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("임베딩 및 인덱싱 시작...")
    VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
    print("지맥 정보를 세계수에 추가하였습니다. data/vector_db 폴더에 저장되었습니다.")

if __name__ == "__main__":
    build()