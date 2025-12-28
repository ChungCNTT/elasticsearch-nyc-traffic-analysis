from elasticsearch import Elasticsearch, helpers
import json
import urllib3
from tqdm import tqdm  # ✅ hiển thị progress bar
import os

# ⚠️ Bỏ cảnh báo SSL do dùng chứng chỉ tự ký
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ⚙️ Kết nối tới 3 node trong cluster
es = Elasticsearch(
    hosts=[
        "https://127.0.0.1:9200",
        "https://127.0.0.1:9201",
        "https://127.0.0.1:9202"
    ],
    basic_auth=("elastic", "u3DXEPWQ7fp8z-Npn6fn"),
    verify_certs=False
)

INDEX_NAME = "nyc_traffic"

# 🧱 Tạo index nếu chưa có
if not es.indices.exists(index=INDEX_NAME):
    mapping = {
        "settings": {
        "number_of_shards": 6,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "link_id": {"type": "integer"},
            "link_name": {"type": "text"},
            "borough": {"type": "keyword"},
            "speed": {"type": "float"},
            "travel_time": {"type": "float"},
            "data_as_of": {"type": "date"},
            "status": {"type": "integer"}
        }
    }
    }
    es.indices.create(index=INDEX_NAME, body=mapping)
    print(f"✅ Created index '{INDEX_NAME}'")
else:
    print(f"ℹ️ Index '{INDEX_NAME}' already exists")

# 🧮 Đếm số dòng trong file để setup progress bar
def count_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)

# 🚀 Generator đọc dữ liệu theo dòng (ít tốn RAM)
def generate_actions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            doc = json.loads(line)
            unique_id = f"{doc.get('id')}_{doc.get('data_as_of')}"  
            yield {
                "_index": INDEX_NAME,
                "_id": unique_id,
                "_source": doc
            }

# 📦 Upload dữ liệu bằng Bulk API với thanh tiến trình
def bulk_upload(file_path):
    total_lines = count_lines(file_path)
    print(f"📊 File có khoảng {total_lines:,} dòng\n")

    with tqdm(total=total_lines, unit="docs", desc="Uploading") as pbar:
        success, failed = 0, 0
        for ok, _ in helpers.streaming_bulk(
            es, 
            generate_actions(file_path),
            chunk_size=10000,  # upload 10k bản ghi/lần
            request_timeout=300
        ):
            if ok:
                success += 1
            else:
                failed += 1
            pbar.update(1)
    print(f"\n✅ Hoàn tất: Uploaded = {success:,}, Failed = {failed:,}")

if __name__ == "__main__":
    file_path = r"E:\data json\nyc_traffic_all.ndjson"
    if os.path.exists(file_path):
        bulk_upload(file_path)
    else:
        print("❌ Không tìm thấy file dữ liệu!")






