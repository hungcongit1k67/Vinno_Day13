# Đặc tả Dashboard

## Nguồn dữ liệu

Ứng dụng cung cấp một endpoint metrics duy nhất:

```
GET http://localhost:8000/metrics
```

Cấu trúc phản hồi (từ `app/metrics.py` → `snapshot()`):

```json
{
  "traffic": 42,
  "latency_p50": 160.0,
  "latency_p95": 290.0,
  "latency_p99": 510.0,
  "avg_cost_usd": 0.0012,
  "total_cost_usd": 0.0504,
  "tokens_in_total": 3200,
  "tokens_out_total": 5400,
  "error_breakdown": { "ValueError": 2 },
  "quality_avg": 0.81
}
```

### Cài đặt khuyến nghị (Grafana + plugin Infinity)

1. Cài plugin **Infinity** trong Grafana.
2. Thêm datasource mới → chọn **Infinity** → đặt tên `lab-metrics`.
3. Nhập Base URL: `http://localhost:8000`.
4. Mỗi panel truy vấn đường dẫn `/metrics`, kiểu JSON, phân tích cú pháp JSONata hoặc UQL.

> **Lựa chọn thay thế:** Dùng `scripts/load_test.py` để tạo traffic liên tục, sau đó đọc
> `data/logs.jsonl` qua datasource Loki hoặc Elasticsearch nếu môi trường hỗ trợ.

---

## 6 Panel bắt buộc (Layer-2)

### Panel 1 — Độ trễ P50 / P95 / P99

| Thuộc tính | Giá trị |
|---|---|
| Loại biểu đồ | Stat (3 giá trị) hoặc Time series (nếu polling liên tục) |
| Trường dữ liệu | `latency_p50`, `latency_p95`, `latency_p99` |
| Đơn vị | mili giây (ms) |
| Đường ngưỡng SLO | **3 000 ms** tại P95 (nguồn: `config/slo.yaml`) |
| Ngưỡng cảnh báo | > 5 000 ms trong 30 phút → Mức P2 (`alert_rules.yaml`) |
| Màu ngưỡng | Xanh lá < 1 000 ms / Vàng < 3 000 ms / Đỏ ≥ 3 000 ms |

### Panel 2 — Lưu lượng (Số lượng yêu cầu / QPS)

| Thuộc tính | Giá trị |
|---|---|
| Loại biểu đồ | Stat hoặc Time series |
| Trường dữ liệu | `traffic` (tổng tích luỹ) |
| Đơn vị | requests hoặc req/s nếu tính theo khoảng polling |
| Ghi chú | Để tính QPS: lấy delta của `traffic` chia cho chu kỳ polling (ví dụ 15 giây) |

### Panel 3 — Tỷ lệ lỗi và phân loại

| Thuộc tính | Giá trị |
|---|---|
| Loại biểu đồ | Stat (tỷ lệ) + Bar chart (phân loại) |
| Trường dữ liệu | `error_breakdown` (object), `traffic` |
| Giá trị tính toán | `error_rate_pct = tổng(error_breakdown.values) / traffic × 100` |
| Đơn vị | phần trăm (%) |
| Đường ngưỡng SLO | **2%** (nguồn: `config/slo.yaml`) |
| Ngưỡng cảnh báo | > 5% trong 5 phút → Mức P1 (`alert_rules.yaml`) |
| Màu ngưỡng | Xanh lá < 1% / Vàng < 2% / Đỏ ≥ 2% |
| Phân loại | Bar chart theo khoá của `error_breakdown` (tên lớp lỗi) |

### Panel 4 — Chi phí theo thời gian

| Thuộc tính | Giá trị |
|---|---|
| Loại biểu đồ | Time series hoặc Stat |
| Trường dữ liệu | `total_cost_usd`, `avg_cost_usd` |
| Đơn vị | USD (ký hiệu $, 4 chữ số thập phân) |
| Đường ngưỡng SLO | **$2,50 / ngày** (nguồn: `config/slo.yaml`) |
| Ngưỡng cảnh báo | > 2× baseline trong 15 phút → Mức P2 (`alert_rules.yaml`) |
| Màu ngưỡng | Xanh lá < $1,00 / Vàng < $2,50 / Đỏ ≥ $2,50 |
| Ghi chú | `total_cost_usd` được đặt lại khi khởi động lại server; cần ghi rõ nhãn trục |

### Panel 5 — Token đầu vào / đầu ra

| Thuộc tính | Giá trị |
|---|---|
| Loại biểu đồ | Bar chart (nhóm đôi) hoặc hai Stat panel riêng biệt |
| Trường dữ liệu | `tokens_in_total`, `tokens_out_total` |
| Đơn vị | tokens |
| Ghi chú | Tỷ lệ `tokens_out / tokens_in` là chỉ số phụ hữu ích để theo dõi |

### Panel 6 — Chỉ số chất lượng (Quality Proxy)

| Thuộc tính | Giá trị |
|---|---|
| Loại biểu đồ | Gauge hoặc Stat |
| Trường dữ liệu | `quality_avg` |
| Đơn vị | điểm số (0,00 – 1,00) |
| Đường ngưỡng SLO | **0,75** (nguồn: `config/slo.yaml`) |
| Màu ngưỡng | Đỏ < 0,60 / Vàng < 0,75 / Xanh lá ≥ 0,75 |
| Ghi chú | Điểm mang tính heuristic (độ khớp tài liệu + độ dài câu trả lời + từ khoá) — ghi rõ nhãn "quality proxy" |

---

## Tiêu chuẩn chất lượng

- Khoảng thời gian mặc định: **1 giờ**
- Tự động làm mới: **mỗi 15 giây** (cấu hình trong Grafana ở góc trên bên phải)
- Mỗi panel có SLO phải hiển thị **đường ngưỡng tham chiếu** rõ ràng tại giá trị SLO
- Tất cả trục và giá trị Stat phải có **nhãn đơn vị** rõ ràng
- Layer chính: **không quá 6–8 panel**
- Tiêu đề panel phải khớp hoặc tương đương với tên đã đặt ở trên

---

## Gợi ý bố cục

```
┌──────────────────────────────┬─────────────────────┐
│  Độ trễ P50 / P95 / P99      │  Lưu lượng (QPS)    │
├────────────────┬─────────────┴─────────────────────┤
│  Tỷ lệ lỗi    │  Phân loại lỗi (Bar chart)         │
├────────────────┴──────────────────┬────────────────┤
│  Chi phí theo thời gian           │  Token vào/ra  │
├───────────────────────────────────┴────────────────┤
│  Chất lượng (Gauge, có thể trải rộng toàn bộ)      │
└────────────────────────────────────────────────────┘
```

---

## Tiêu chí nghiệm thu

Dashboard được coi là hoàn chỉnh khi:

1. Đủ 6 panel, tiêu đề đúng theo đặc tả.
2. Các panel Độ trễ, Tỷ lệ lỗi, Chi phí và Chất lượng đều có đường ngưỡng SLO hiển thị.
3. Tất cả panel có nhãn đơn vị trên trục hoặc giá trị hiển thị.
4. Auto-refresh được đặt ≤ 30 giây.
5. Ảnh chụp màn hình dashboard đang chạy được đính kèm trong `docs/grading-evidence.md`.
