# Elasticsearch NYC Traffic Analysis

<p align="center">
  <img src="https://via.placeholder.com/1280x640/1E3A8A/FFFFFF?text=Elasticsearch+NYC+Traffic+Analysis" alt="Project Banner" width="100%"/>
</p>

**Elasticsearch NYC Traffic Analysis** là dự án nghiên cứu và ứng dụng thực tiễn nhằm khai thác sức mạnh của **Elasticsearch** trong việc lưu trữ, truy vấn và phân tích dữ liệu lớn về tốc độ giao thông thời gian thực tại thành phố New York. Dự án tập trung vào việc triển khai một cụm Elasticsearch phân tán, xử lý bộ dữ liệu **NYC Real-Time Traffic Speed Data** (hơn 64,9 triệu bản ghi), đồng thời xây dựng hệ thống trực quan hóa thông minh thông qua **Kibana**.

Dự án được thực hiện trong khuôn khổ môn học **Phân tích Dữ liệu Lớn** tại Khoa Công nghệ Thông tin, Trường Đại học Thủy Lợi, nhằm đánh giá hiệu năng, độ tin cậy và khả năng mở rộng của Elasticsearch trong các bài toán Big Data thời gian thực.

## 📄 Mục tiêu nghiên cứu

- Triển khai và vận hành cụm Elasticsearch 3 node (1 master + 2 data nodes) trong môi trường phân tán.
- Xây dựng pipeline nạp dữ liệu lớn từ định dạng NDJSON vào Elasticsearch với hiệu suất tối ưu.
- Thực hiện các truy vấn tổng hợp (aggregation) phức tạp để phân tích xu hướng giao thông theo thời gian, khu vực và mối quan hệ giữa các chỉ số.
- Phát triển dashboard Kibana chuyên nghiệp để trực quan hóa dữ liệu giao thông đô thị.
- Đánh giá toàn diện về hiệu năng truy vấn, khả năng chịu lỗi (fault tolerance) và tính sẵn sàng cao (high availability).

## ✨ Tính năng chính

- **Cụm Elasticsearch phân tán**: 3 node với cấu hình shard/replica hợp lý, trạng thái cluster luôn duy trì **green**.
- **Bulk indexing hiệu suất cao**: Sử dụng `helpers.streaming_bulk` với chunk_size 10.000 bản ghi, hỗ trợ progress bar (tqdm) để theo dõi tiến trình nạp dữ liệu.
- **Tiền xử lý dữ liệu**: Chuẩn hóa trường thời gian, loại bỏ giá trị ngoại lai, chuyển đổi sang múi giờ UTC, lọc nhiễu để đảm bảo chất lượng dữ liệu.
- **Truy vấn phân tích nâng cao**:
  - Tốc độ trung bình theo ngày, theo quận.
  - Thời gian di chuyển trung bình theo khu vực.
  - Tỷ lệ đóng góp dữ liệu theo quận.
  - Mối tương quan giữa tốc độ và thời gian di chuyển.
  - Phân bố dữ liệu theo khoảng thời gian cao điểm.
- **Dashboard Kibana**: Biểu đồ trực quan hóa xu hướng tắc nghẽn, so sánh hiệu quả giao thông giữa các quận (Manhattan thấp nhất ~23 mph, Staten Island cao nhất ~40 mph).
- **Kiểm tra khả năng chịu lỗi**: Thử nghiệm tự động rebalancing khi mất 1–2 node, đảm bảo tính sẵn sàng cao và phục hồi nhanh chóng.

## 🛠 Công nghệ sử dụng

| Công nghệ              | Mô tả                                                                 |
|------------------------|-----------------------------------------------------------------------|
| **Elasticsearch**      | Phiên bản 8.x – Lõi lưu trữ và truy vấn phân tán, hỗ trợ aggregation và time-series data |
| **Kibana**             | Trực quan hóa dữ liệu, xây dựng dashboard giao thông thời gian thực   |
| **Python**             | Ngôn ngữ lập trình chính cho pipeline nạp dữ liệu                     |
| **elasticsearch-py**   | Thư viện chính thức để tương tác với Elasticsearch cluster            |
| **tqdm**               | Hiển thị progress bar chuyên nghiệp khi bulk upload                   |
| **NDJSON**             | Định dạng dữ liệu tối ưu cho bulk indexing                            |

## 📊 Kết quả nổi bật

- Xử lý thành công hơn **64,9 triệu bản ghi** với tốc độ lập chỉ mục ổn định (~25 docs/giây).
- Thời gian phản hồi truy vấn trung bình **4–6 ms** ngay cả với aggregation phức tạp.
- Tốc độ trung bình toàn thành phố: **~28–33 mph**, Manhattan thấp nhất (~23 mph), Staten Island cao nhất (~40 mph).
- Xu hướng rõ ràng: Giảm tốc độ mạnh vào giờ cao điểm (7–9h và 17–19h).
- Khả năng chịu lỗi: Cluster tự động phục hồi khi mất 1–2 node, duy trì tính toàn vẹn dữ liệu.

## 🚀 Hướng dẫn triển khai nhanh

### Yêu cầu
- Elasticsearch cluster (3 node) đã chạy (cổng 9200, 9201, 9202).
- Python 3.8+ với các thư viện: `elasticsearch`, `tqdm`.
- File dữ liệu: `nyc_traffic_all.ndjson`.

### Cài đặt
```bash
pip install elasticsearch tqdm
Chạy pipeline nạp dữ liệu
Bashpython upload_nyc_traffic_progress.py
Kết nối Kibana
Truy cập: http://localhost:5601 → Tạo index pattern nyc_traffic* → Xây dựng visualization và dashboard.
📚 Tài liệu dự án

Báo cáo chi tiết: big data 3.docx
Mã nguồn pipeline: upload_nyc_traffic_progress.py
Bộ dữ liệu mẫu: NYC Real-Time Traffic Speed Data (Kaggle)

📜 Giấy phép
Dự án phục vụ mục đích học tập và nghiên cứu, không sử dụng cho mục đích thương mại.
🙏 Lời tri ân
Nhóm xin chân thành cảm ơn các giảng viên Khoa Công nghệ Thông tin, Trường Đại học Thủy Lợi đã hướng dẫn và tạo điều kiện để hoàn thành bài tập lớn môn Phân tích Dữ liệu Lớn.
Dự án khẳng định tiềm năng của Elasticsearch trong xử lý dữ liệu lớn thời gian thực, đặc biệt trong lĩnh vực giao thông thông minh và đô thị hóa bền vững.
