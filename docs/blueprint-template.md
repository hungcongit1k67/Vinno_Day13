# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: VINNO
- [REPO_URL]: https://github.com/hungcongit1k67/Vinno_Day13
- [MEMBERS]:
  - Member A: Chu Thành Thông  | Role: Logging & PII
  - Member B: Bùi Đức Tiến | Role: Tracing & Enrichment
  - Member C: Phùng Hữu Phú | Role: SLO & Alerts
  - Member D: Nguyễn Công Hùng | Role: Load Test & Dashboard & Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: /100
- [TOTAL_TRACES_COUNT]: 
- [PII_LEAKS_FOUND]: 

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: ![EVIDENCE_CORRELATION_ID_SCREENSHOT](image/EVIDENCE_CORRELATION_ID_SCREENSHOT.jpg)
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: ![EVIDENCE_PII_REDACTION_SCREENSHOT](image/EVIDENCE_PII_REDACTION_SCREENSHOT.jpg)
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: ![EVIDENCE_TRACE_WATERFALL_SCREENSHOT](image/EVIDENCE_TRACE_WATERFALL_SCREENSHOT.jpg)
- [TRACE_WATERFALL_EXPLANATION]: Span rag_retrieve chạy trước và hoàn thành gần như tức thì (<1ms), tiếp theo generate mất ~150ms — cho thấy bottleneck nằm ở tầng LLM generation, không phải retrieval. Tổng trace run là 0.15s, nằm trong ngưỡng SLO 3000ms.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: ![_6_PANELS_SCREENSHOT](image/6_panels.png)
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | |
| Error Rate | < 2% | 28d | |
| Cost Budget | < $2.5/day | 1d | |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: ![ALERT_RULES_SCREENSHOT](image/Alert_rule_screenshot.jpg)
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#L...]

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: (e.g., rag_slow)
- [SYMPTOMS_OBSERVED]: 
- [ROOT_CAUSE_PROVED_BY]: (List specific Trace ID or Log Line)
- [FIX_ACTION]: 
- [PREVENTIVE_MEASURE]: 

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: (Link to specific commit or PR)

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
