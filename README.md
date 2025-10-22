# Digital Business Card Backend (Flask + SQLite + Cashfree)

## Setup
1. `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. Copy `.env.example` → `.env` and fill the values.
4. `python run.py`

## Migrations (optional but recommended)
- `flask --app run.py db init`
- `flask --app run.py db migrate -m "init"`
- `flask --app run.py db upgrade`

## API Highlights
- `POST /api/auth/register` {name,email,password}
- `POST /api/auth/login` {email,password}
- `GET  /api/cards/public/<handle>`
- `GET  /api/cards/me` (Bearer token)
- `PUT  /api/cards/me` (Bearer token) — update card
- `POST /api/payments/create-order` (Bearer token) {amount, return_url}
- `POST /api/payments/webhook` (Cashfree callback)
- `GET  /api/admin/overview` (Bearer token – admin only)

## Notes
- Amounts are in INR (integer rupees for simplicity).
- Webhook signature HMAC (hex) verified via `CASHFREE_WEBHOOK_SECRET`.
- For production, use `CASHFREE_BASE_URL=https://api.cashfree.com/pg`.