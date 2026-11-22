# City Bus Pass & Tracking System — Upgraded Demo

A Streamlit + SQLite academic project. This version adds:
1. QR-code generation for every digital bus pass, with camera/upload QR validation.
2. Route-based digital pass pricing (7, 30 and 90 days).
3. Simulated moving-bus GPS map, status, ETA and refresh.
4. Simulated delay alerts.
5. Price persistence and safe SQLite migration for existing databases.

## Run locally
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Open the local URL printed by Streamlit (usually http://localhost:8501).

## Demo administrator
- Email: `admin@citybus.local`
- Password: `Admin@123`

Change this demo password before using the app outside a classroom demonstration.

## Pricing rules
The sample daily fares are configured in `app.py`:
- Hadapsar – Magarpatta – Shivajinagar: ₹20/day
- Katraj – Swargate – Deccan: ₹15/day
- Wakad – Aundh – University: ₹18/day
- Pune Station – Shivajinagar – Hinjawadi: ₹25/day

Suggested discounts:
- 7 days: 0%
- 30 days: 20%
- 90 days: 40%

Formula: `daily route fare × validity days × (1 - discount)`.
These are illustrative academic-project fares, not official PMPML prices.

## Simulated GPS
`tracking.py` provides sample coordinates around Pune and moves selected buses over time.
The map and status/ETA are simulated. No physical bus, driver phone, or live GPS device is connected.
Firebase can be integrated later by replacing the data source in `tracking.py`.

## Existing database migration
If `citybus.db` already exists, the app checks the `passes` table and adds the `price` column if missing. Keep a backup of your database before replacing project files.

## Tests
```bash
python -m pytest -v
```
