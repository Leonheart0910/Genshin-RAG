import json
import os
import chromadb
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from config import init_settings, DATA_DIR, DB_DIR


def load_json_data():
    documents = []
    # source 폴더 내의 모든 json 파일을 읽음
    if not os.path.exists(DATA_DIR):
        print(f"경로가 없습니다: {DATA_DIR}")
        return []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # 데이터가 리스트가 아니라 딕셔너리 하나인 경우 리스트로 감싸기
                    if isinstance(data, dict):
                        data = [data]

                    for item in data:
                        # [핵심 수정] 메타데이터 전처리: 리스트([])가 있으면 문자열로 변환
                        # 예: ["리월", "캐릭터"] -> "리월, 캐릭터"
                        meta = item.get("metadata", {})
                        clean_metadata = {}

                        for key, value in meta.items():
                            if isinstance(value, list):
                                clean_metadata[key] = ", ".join(str(v) for v in value)
                            else:
                                clean_metadata[key] = value

                        # 텍스트와 전처리된 메타데이터로 Document 생성
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
            print("로딩된 데이터가 없습니다. data/source 폴더에 JSON 파일이 있는지 확인해주세요.")
            return

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
        print("지맥 구축완료! data/vector_db 폴더에 저장되었습니다.")

    except Exception as e:
        print(f"\n 치명적인 오류 :\n{e}")


if __name__ == "__main__":
    build()