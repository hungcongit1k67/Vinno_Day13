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
app/
  main.py                Ứng dụng FastAPI chính
  agent.py               Pipeline agent cốt lõi
  logging_config.py      Cấu hình structlog
  middleware.py          Middleware correlation ID
  pii.py                 Các hàm hỗ trợ che/lọc dữ liệu nhạy cảm
  tracing.py             Các hàm hỗ trợ Langfuse
  schemas.py             Các model cho request/response/log
  metrics.py             Các hàm hỗ trợ metrics lưu trong bộ nhớ
  incidents.py           Các công tắc bật/tắt lỗi được chèn vào để mô phỏng sự cố
  mock_llm.py            LLM giả lập có đầu ra xác định trước
  mock_rag.py            Bộ truy xuất giả lập có đầu ra xác định trước

config/
  slo.yaml               Các SLO mẫu khởi đầu
  alert_rules.yaml       Các rule cảnh báo mẫu khởi đầu
  logging_schema.json    Schema log mong đợi

scripts/
  load_test.py           Tạo request để test tải
  inject_incident.py     Bật/tắt các tình huống sự cố mô phỏng
  validate_logs.py       Kiểm tra schema của log

data/
  sample_queries.jsonl   Các request mẫu để test
  expected_answers.jsonl Các đáp án mong đợi mẫu để kiểm tra chất lượng
  incidents.json         Mô tả các kịch bản sự cố
  logs.jsonl             File đích để app ghi log ra
  audit.jsonl            File log audit đầu ra (tùy chọn)

docs/
  blueprint-template.md  Mẫu nộp bài của nhóm
  alerts.md              Runbook + phiếu bài tập về cảnh báo
  dashboard-spec.md      Checklist dashboard 6 biểu đồ
  grading-evidence.md    Phiếu thu thập minh chứng chấm điểm
  mock-debug-qa.md       Các câu hỏi debug mô phỏng để hỏi đáp hoặc làm bài viết
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
