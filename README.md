# Day 13 Observability Lab Template

Template repo for a 4-hour hands-on lab on Monitoring, Logging, and Observability.

## What students will build

A small FastAPI "agent" instrumented with:
- structured JSON logging
- correlation ID propagation
- PII scrubbing
- Langfuse tracing
- minimal metrics aggregation
- SLOs, alerts, and a blueprint report

This template is intentionally incomplete. Teams are expected to finish TODOs during the lab.

## Suggested lab flow (Gapped Template)

1. **Run the starter app**: Observe that logs are basic and correlation IDs are missing.
2. **Implement Correlation IDs**: Fix `app/middleware.py` so every request has a unique `x-request-id`.
3. **Enrich Logs**: Update `app/main.py` to bind user, session, and feature context to every log.
4. **Sanitize Data**: Implement the PII scrubber in `app/logging_config.py`.
5. **Verify with Script**: Run `python scripts/validate_logs.py` to check your progress.
6. **Tracing**: Send 10-20 requests and verify traces in Langfuse (ensure `observe` decorator is used).
7. **Dashboards**: Build your 6-panel dashboard from exported metrics.
8. **Alerting**: Configure alert rules in `config/alert_rules.yaml` and test them.

## Quick start

```bash
python -m venv .venv (VD: python -m venv day13)
source .venv/bin/activate (VD: day13\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Tooling

```bash
# Generate requests (use --concurrency 5 to test parallel bottlenecks)
python scripts/load_test.py --concurrency 5

# Inject failures live
python scripts/inject_incident.py --scenario rag_slow

# Check your implementation progress
python scripts/validate_logs.py
```

## Repo map

```text
app/                     Là nơi chạy hệ thống và gắn observability vào hệ thống.
  main.py                FastAPI app chính, khai báo API và gắn middleware/logging
  agent.py               Pipeline xử lý chính của agent: RAG -> LLM -> kết quả
  logging_config.py      Cấu hình structlog và định dạng log JSON
  middleware.py          Gắn correlation ID cho từng request và thêm vào response
  pii.py                 Hàm che/lọc dữ liệu nhạy cảm như email, SĐT, CCCD
  tracing.py             Hàm hỗ trợ tracing với Langfuse
  schemas.py             Định nghĩa model cho request, response và log
  metrics.py             Thu thập metrics đơn giản như latency, error, cost, token
  incidents.py           Bật/tắt các sự cố giả lập để test hệ thống
  mock_llm.py            LLM giả lập để test mà không cần gọi model thật
  mock_rag.py            RAG giả lập để test retrieval và lỗi liên quan

config/                  Là nơi định nghĩa tiêu chuẩn cần đạt: log schema, SLO, alert rules.
  slo.yaml               Mẫu SLO để theo dõi mục tiêu dịch vụ
  alert_rules.yaml       Mẫu rule cảnh báo khi hệ thống có vấn đề
  logging_schema.json    Schema chuẩn mà log của app cần tuân theo

scripts/                 Là bộ công cụ để sinh traffic, gây sự cố, tự chấm tiến độ.
  load_test.py           Tạo request hàng loạt để test tải và sinh log/metrics
  inject_incident.py     Bật/tắt các kịch bản sự cố mô phỏng
  validate_logs.py       Kiểm tra log có đúng schema, đủ field, có lộ PII hay không

data/                    Là dữ liệu seed và output phục vụ test/đánh giá.
  sample_queries.jsonl   Dữ liệu request mẫu để test app
  expected_answers.jsonl Dữ liệu đáp án mẫu để kiểm tra chất lượng output
  incidents.json         Mô tả các kịch bản sự cố dùng trong bài lab
  logs.jsonl             Nơi app ghi log đầu ra
  audit.jsonl            Nơi ghi audit log nếu có dùng

docs/                    Là nơi biến kết quả kỹ thuật thành dashboard, runbook, evidence và báo cáo nộp bài.
  blueprint-template.md  Mẫu báo cáo/biểu mẫu nộp bài của nhóm
  alerts.md              Hướng dẫn xử lý cảnh báo và runbook
  dashboard-spec.md      Checklist dashboard 6 biểu đồ cần có
  grading-evidence.md    Danh sách minh chứng cần thu thập để chấm điểm
  mock-debug-qa.md       Câu hỏi mô phỏng để luyện debug và giải thích sự cố
```

## Team role suggestion

- Member A: logging + PII
- Member B: tracing + tags
- Member C: SLO + alerts
- Member D: load test + incident injection
- Member E: dashboard + evidence
- Member F: blueprint + demo lead

## Grading policy (60/40 Split)

Your final grade is calculated as follows:

1. **Group Score (60%)**: 
   - **Technical Implementation (30 pts)**: Verified by `validate_logs.py` and live system state.
   - **Incident Response (10 pts)**: Accuracy of your root cause analysis in the report.
   - **Live Demo (20 pts)**: Team presentation and system demonstration.
2. **Individual Score (40%)**:
   - **Individual Report (20 pts)**: Quality of your specific contributions in `docs/blueprint-template.md`.
   - **Git Evidence (20 pts)**: Traceable work via commits and code ownership.

**Passing Criteria**: 
- All `TODO` blocks must be completed.
- Minimum of 10 traces must be visible in Langfuse.
- Dashboard must show all 6 required panels.
