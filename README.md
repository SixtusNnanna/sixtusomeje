# Habit Tracker API


An async backend API for ecommerce platform — built with **FastAPI**, **async SQLAlchemy**, and **JWT authentication**.

**Live demo:** https://boma-project-2-0.onrender.com/docs
**Repo:** `https://github.com/sixtusNnanna/SixtusOmeje`

---

## What it does

Think of it as the backend engine behind a ecommerce platform like amazon and co — the part that stores data, enforces rules, and exposes an API for a frontend (or Swagger UI) to consume.

a is strictly scoped per user — no user can ever read, edit, or delete another user's data

---

## Tech stack

| Layer | Choice |
|---|---|
| Framework | FastAPI (async) |
| ORM | SQLAlchemy 2.0 (async, `Mapped[]` style) |
| Database | PostgreSQL (async, via `asyncpg`) |
| Migrations | Alembic |
| Auth | JWT (HS256) via `python-jose`, password hashing via `passlib` |
| Validation | Pydantic v2 |


---

## Architecture

```
app/
├── api/
    ├── v1/
        ├── endpoints/  # Route handlers (thin — delegate to services)
        ├── base.py/    #base endpoint
│   ├── routers/
│   ├── schemas/         # Pydantic request/response models
│   └── dependencies.py  # Shared FastAPI dependencies (auth, DB session)
├── core/
│   ├── security.py      # JWT creation/verification, password hashing
│   └── enum.py        # Handle the Enum Types
├── database/
│   ├── models.py         # SQLAlchemy models (User, Habit, HabitLog)
│   ├── base.py            # Declarative base
│   └── session.py         # Async engine + session factory
├── services/              # Business logic — one service per resource
│   ├── base.py             # Generic CRUD service (Generic[ModelType])
│   ├── customer.py
│   ├── inventory.py
│   ├── order.py
│   ├── product.py
│   ├── user.py
│   └── warehouse.py
├── config.py                   # Environment-driven settings
├── exceptions.py              #Customer Exceptions
├── main.py                   # App entrypoint, startup lifecycle
└── utils.py                  # other utilies eg (access token creation and decode)
```

**Design principles followed throughout:**
- **Thin routers, fat services** — routes handle HTTP concerns only (status codes, request/response shape); all business logic lives in services.
- **Ownership scoping at the query level** — every fetch/update/delete filters by the requesting user's ID directly in the SQL `WHERE` clause, not via a fetch-then-check pattern. A user requesting another user's resource gets an identical `404` to a resource that doesn't exist — no information leakage about what IDs exist.
- **Services raise `CustomerErrors`, never `HTTPException`** — keeps business logic decoupled from the HTTP layer; routes translate exceptions into the appropriate status codes.
- **Derived data over stored data** — completion rates, due-days, and streaks are computed live from raw logs + habit schedules rather than cached/duplicated, keeping the data model minimal and always consistent.

---

## Key features

### Authentication & security
- Signup with password strength validation (Pydantic `field_validator`)

- JWT-based login (HS256)
- Passwords hashed with `passlib` (bcrypt)


### Analytics
- Due-day and completion-rate calculation over arbitrary date ranges
- Week-over-week and month-over-month completion trend comparison

---

## Assumptions Made

- I introduced an order_item table that handles individaul order, it relates with order in a One to many relationship

- A linking table between order item, that helps allocate the quantity from several inventory containing the item ordered



## Getting started

**Prerequisites:** This project uses Docker Compose to manage application and its variables.
Make sure you have installed
- Docker
- Docker Compose

```bash
⚙️ 2. Environment Variables

Create a .env file in the root directory and add your configuration:

DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256

p▶️ 3. Start the Application

Run the following command:

docker-compose up --build

Or (recommended for background mode):

🌐 4. Access the Application

Open your browser:

http://localhost:8000

Swagger docs:

http://localhost:8000/docs
```

---

## Third party packes
- Pydantic for type validation
- pydantic-email for email validation
- pydantic-other_types phone for

## Challenges Encountered
- Not able to implement the seletin lazy
- not able to deploy on vercel


---

## Future improvement
- Implement seletin lazy to select related tables
- CI/CID
- The remaining endpoints(currently working on them)
---

## Author

Sixtus Omeje
