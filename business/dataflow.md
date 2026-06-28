```markdown
# dataflow.md

## 1️⃣ External Data Sources
| Source | Type | Frequency | Auth Boundary |
|--------|------|-----------|---------------|
| GitHub PR & Commit events | Webhook | Real‑time | OAuth2 (GitHub App) |
| CI/CD Pipeline logs (GitHub Actions, Jenkins) | API | Near‑real‑time | Personal Access Token |
| Issue trackers (GitHub Issues, Jira) | API | Polling (5 min) | OAuth2 / API token |
| Static analysis tools (SonarQube, CodeQL) | API | Daily | API key |
| User‑generated quality rules (JSON/YAML) | File upload | On‑demand | JWT |
| External quality benchmarks (ISO, OWASP) | FTP/HTTPS | Weekly | Basic Auth |

> **Auth boundaries**  
> • All external integrations use OAuth2 or API keys scoped to read‑only.  
> • User‑generated data is protected by JWT signed by the platform’s auth service.  
> • Internal services communicate over mTLS within the VPC.

---

## 2️⃣ Ingestion Layer
```
┌───────────────────────┐
│  External Webhooks    │
│  (GitHub, CI, Issue)  │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  Ingestion API (FastAPI) │
│  - Auth: JWT/OAuth2      │
│  - Idempotency handling │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  Kafka Topic: raw_events │
│  - Partitioned by repo   │
│  - Exactly‑once semantics│
└───────────────────────┘
```

- **FastAPI**: REST/WS endpoints, rate‑limited, validates payload schemas.  
- **Kafka**: Durable event store, supports replay for re‑processing.

---

## 3️⃣ Processing / Transform Layer
```
┌───────────────────────┐
│  Event Processor (Kafka Streams) │
│  - Parses raw JSON → Domain Events │
│  - Enriches with repo metadata      │
│  - Emits to downstream topics      │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  Quality Rule Engine (Node.js) │
│  - Loads user rules from S3   │
│  - Executes against codebase  │
│  - Emits QualityScore events │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  Aggregator (Python) │
│  - Computes metrics per PR, repo, org │
│  - Stores snapshots in Redis for quick read │
└───────────────────────┘
```

- **Kafka Streams**: Stateless & stateful ops, low latency.  
- **Node.js Rule Engine**: Uses `vm2` sandbox for safe rule execution.  
- **Python Aggregator**: Periodic jobs (every 5 min) push to Redis.

---

## 4️⃣ Storage Tier
```
┌───────────────────────┐
│  PostgreSQL (Primary) │
│  - Relational store for: users, repos, quality rules, audit logs │
│  - Replicated (async) to read replicas │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  TimescaleDB (TSDB)   │
│  - Time‑series metrics (quality scores, trend data) │
│  - Continuous aggregates for dashboards │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  S3 (Object Store)    │
│  - Raw event backups   │
│  - User rule files     │
│  - Artifact snapshots  │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  Redis (Cache)        │
│  - Hot metrics, session data │
└───────────────────────┘
```

- **PostgreSQL**: ACID guarantees for user data.  
- **TimescaleDB**: Efficient down‑sampling and retention policies.  
- **S3**: Immutable storage, lifecycle policies (30 days for raw events, 1 year for artifacts).  
- **Redis**: 5 s TTL for aggregated metrics.

---

## 5️⃣ Query / Serving Layer
```
┌───────────────────────┐
│  GraphQL API (Apollo) │
│  - Auth: JWT, scopes  │
│  - Resolvers hit Postgres/Timescale │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  REST API (FastAPI)   │
│  - Legacy endpoints   │
│  - Webhooks for CI    │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  CDN (CloudFront)     │
│  - Static assets (React UI) │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  Frontend (React)     │
│  - Uses Apollo Client  │
│  - Auth via Auth0      │
└───────────────────────┘
```

- **GraphQL**: Flexible queries for dashboards, supports pagination & filtering.  
- **REST**: Simple CRUD for rule management.  
- **CDN**: Edge caching, 99.99% SLA.

---

## 6️⃣ Egress to User
- **Web UI**: Interactive dashboards, rule editor, PR status widget.  
- **Slack/Teams Bot**: Push notifications on quality score changes.  
- **Email Reports**: Weekly quality health summaries.  
- **Webhooks**: Allow downstream services to react to quality events.

---

### Auth & Security Highlights
| Layer | Auth Mechanism | Notes |
|-------|----------------|-------|
| External | OAuth2 (GitHub App) | Scoped to read events |
| Ingestion API | JWT (Auth0) | Signed, short‑lived |
| Internal services | mTLS + API keys | Mutual TLS within VPC |
| Frontend | Auth0 + OIDC | Role‑based access |
| Data Stores | IAM roles, encryption at rest | PostgreSQL, Timescale, S3 |
| Egress | JWT + CSRF tokens | For webhooks & APIs |

--- 

**End of dataflow.md**