import json
import os
import chromadb
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from config import init_settings, DATA_DIR, DB_DIR


def load_json_data():
    documents = []
    if not os.path.exists(DATA_DIR):
        print(f"경로가 없습니다: {DATA_DIR}")
        return []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        data = [data]

                    for item in data:
                        meta = item.get("metadata", {})
                        clean_metadata = {}
                        for key, value in meta.items():
                            if isinstance(value, list):
                                clean_metadata[key] = ", ".join(str(v) for v in value)
                            else:
                                clean_metadata[key] = value

                        doc = Document(
                            text=item.get("text", ""),
                            metadata=clean_metadata
                        )
                        documents.append(doc)
            except Exception as e:
                print(f"파일 로드 중 에러 발생 ({filename}): {e}")
    return documents


def build():
    try:
        init_settings()
        print("데이터 로딩 중...")
        documents = load_json_data()

        if not documents:
            print("로딩된 데이터가 없습니다.")
            return

        print(f"총 {len(documents)}개의 데이터 청크를 찾았습니다.")

        # ChromaDB 연결
        db = chromadb.PersistentClient(path=DB_DIR)

        # [핵심 수정] 기존 컬렉션이 있다면 삭제하여 초기화 (Overwrite 로직)
        collection_name = "genshin_lore"
        try:
            db.delete_collection(collection_name)
            print(f"기존 '{collection_name}' 컬렉션을 초기화했습니다.")
        except ValueError:
            # 컬렉션이 없어서 삭제에 실패한 경우 무시
            print(f"새로운 '{collection_name}' 컬렉션을 생성합니다.")

        chroma_collection = db.create_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        print("임베딩 및 인덱싱 시작 (데이터를 새로 굽는 중)...")
        VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )
        print("재구축 완료 중복 없이 최신 데이터만 존재합니다.")

    except Exception as e:
        print(f"\n오류 발생: {e}")


if __name__ == "__main__":
    build()