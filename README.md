# Iron Proxy — Firewall & Corporate Proxy Server

A network-level security gateway that intercepts and inspects web traffic for a network, enforcing corporate-style employee authentication, real-time threat detection, and full request/response logging — similar in spirit to enterprise proxy/firewall solutions used in corporate IT environments.

---

## Overview

Iron Proxy sits between client devices and the internet. Once a network is proxied through it, every HTTP(S) request is intercepted, inspected, and evaluated before being allowed through. It combines three responsibilities into one system:

1. **Corporate-style access control** — employees must authenticate before their traffic is allowed out, and every login/logout is timestamped and tracked per device (by IP).
2. **Real-time threat detection** — outgoing requests are checked against URL reputation data, and malicious or suspicious destinations are blocked or flagged with a warning page before the user reaches them.
3. **Live traffic monitoring** — every request and response flowing through the network is logged and streamed in real time to an admin dashboard, giving full visibility into network activity.

---

## How It Works

The system is composed of three services working together:

```
┌────────────┐   intercepts traffic    ┌───────────────┐   WebSocket    ┌─────────────┐
│   Client    │ ───────────────────▶  │  Proxy Server  │ ─────────────▶ │   Backend    │
│  Network    │                        │   (mitmproxy)  │ ◀───────────── │  (FastAPI)   │
└────────────┘                        └───────────────┘                └─────────────┘
                                                                                 │
                                                                     ┌───────────┼───────────┐
                                                                     ▼                       ▼
                                                              PostgreSQL                  Redis
                                                          (sessions, logs,           (rate limiting,
                                                           employees)                 request cache)
                                                                     │
                                                                     ▼
                                                          Next.js Admin Dashboard
                                                        (live logs, employee mgmt)
```

1. **Proxy Server** (built on `mitmproxy`) intercepts every outgoing request from the network. For each user-initiated request, it asks the backend — over a persistent WebSocket connection — whether the requesting device is authenticated and within its rate limit.
2. If the device **isn't logged in**, the request is redirected to a corporate-style login page. If the device has **exceeded its request limit**, it's redirected to a limit-reached page.
3. Otherwise, the proxy asks the backend to check the destination URL's safety via the **VirusTotal API**. Based on the threat score, the request either passes through, or the user is redirected to a **risk warning** or **suspicious activity warning** page.
4. Every request and response is logged to PostgreSQL and **broadcast live over WebSockets** to a Next.js admin dashboard, so administrators can watch network activity as it happens.
5. **Redis** is used for fast rate-limiting per IP and for short-lived request/response correlation caching.

---

## Key Features

- **Corporate-style authentication** — employees must log in before their traffic is allowed through; login and logout timestamps are recorded per device
- **Per-device rate limiting** — Redis-backed request throttling with configurable limits per time window
- **Real-time threat detection** — integrates with the VirusTotal API to classify destination URLs as safe, suspicious, or malicious before allowing access
- **Warning/block pages** — suspicious or malicious requests are intercepted and redirected to a warning page instead of the actual destination
- **Live traffic monitoring** — all requests/responses are streamed in real time over WebSockets to an admin dashboard
- **Employee management** — add, search, paginate, and remove employees from the admin panel
- **Session history** — view historical browsing sessions and the full request/response log for any session
- **Ad-request blocking** — pattern-based blocking of known ad request URLs

---

## Tech Stack

| Component | Technology |
|---|---|
| Proxy Engine | mitmproxy (Python), WebSocket client |
| Backend API | FastAPI, WebSockets, SQLAlchemy, Alembic |
| Database | PostgreSQL |
| Caching / Rate Limiting | Redis |
| Threat Intelligence | VirusTotal API |
| Admin Dashboard | Next.js, React, TanStack Query, Zustand, Radix UI, Tailwind CSS |

---

## Project Structure

```
Backend/          # FastAPI service — auth, employee mgmt, session/request logs, WebSocket hub
├── app/
│   ├── modules/      # Auth, Employee, Log, Session, Security routers
│   ├── helpers/       # DB helper, Redis helper, VirusTotal API handler
│   ├── models/         # SQLAlchemy models (Employee, Request, Response, Session)
│   └── templates/      # Login, logout, warning, and rate-limit HTML pages
└── alembic/          # Database migrations

ProxyServer/       # mitmproxy addon — intercepts traffic, talks to Backend over WebSocket
└── app/
    └── utils/         # Ad-pattern matching, logging, action types

frontend/          # Next.js admin dashboard — employee management & live traffic logs
└── src/
    ├── app/            # Employees, sessions, and log pages
    └── components/     # SocketProvider for live log streaming, tables, forms
```

---

## Getting Started

### Prerequisites

- Python 3.x
- Node.js
- PostgreSQL
- Redis
- A [VirusTotal API key](https://www.virustotal.com/) (for URL threat scanning)

### 1. Backend Setup

```bash
cd Backend
pip install -r requirements.txt   # or install FastAPI, SQLAlchemy, Alembic, redis, requests manually
```

Create a `.env` file with:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/ironproxy
VIRUS_TOTAL_API_KEY=your_virustotal_api_key
```

Run database migrations and start the server:
```bash
python setup.py         # creates database tables
alembic upgrade head
uvicorn app.main:app --reload
```

### 2. Proxy Server Setup

```bash
cd ProxyServer
pip install mitmproxy websockets python-dotenv
```

Create a `.env` file with:
```env
WEBSOCKET_SERVER=ws://localhost:8000/ws
```

Run mitmproxy with the addon:
```bash
mitmdump -s app/main.py
```

Point your network/device proxy settings to the machine running mitmproxy (default port `8080`).

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The admin dashboard will be available at `http://localhost:3000`.

---

## Roadmap

- [ ] Configurable rate-limit thresholds per employee/role
- [ ] Exportable audit logs
- [ ] Role-based access control for admin dashboard
- [ ] HTTPS certificate automation for seamless traffic interception

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Author

**MD Rehan**
[GitHub](https://github.com/mdrehan369) · [LinkedIn](https://linkedin.com/in/md-rehan-169411232)
