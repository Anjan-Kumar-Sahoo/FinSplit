Here's The structure of the project:

FinSplit/
│
├── core/                 # Main app for business logic
│   ├── models.py         # User, Pool, PoolMember, Bill, etc.
│   ├── views.py          # Core logic for APIs
│   ├── serializers.py    # (If using DRF later)
│   ├── urls.py           # App-level routing
│   └── ...
│
├── FinSplit/             # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── templates/            # (optional if you use HTML)
├── static/               # For static files
└── manage.py


Here's the workflow :

🔹 1. User Management (via UPI)
Users are identified by UPI ID only — no login/passwords

UPI IDs will be verified (simulated) when added

User info is stored: full_name, upi_id, etc.

🔹 2. Pool (Group) Management
A user creates a pool (like “Trip to Goa”)

Creator is stored in created_by

Other users are added as PoolMembers by their verified UPI IDs

🔹 3. Add Expenses
Anyone in the pool can add an expense

While adding, they will specify:

Amount

Who paid

Split method (equal / percentage / manual)

Who shares it

🔹 4. Split Logic
Split amount is calculated based on:

Equal: divide among all

Percentage: custom percent each

Manual: fixed custom amounts

Each split entry is stored as a debt record, with:

Who owes

Who is owed

Amount

Linked to which pool & which bill

🔹 5. Debt Tracking
System tracks how much each user owes to others inside a pool

This is like a running balance

🔹 6. Settle Payments (via UPI)
Users can settle their debts by clicking "Settle"

The app simulates sending a UPI request (no real payment integration)

Once settled, the debt record is marked as paid

🔹 7. Activity & Summary
Pool Summary: who paid what, who owes how much

User Summary: what each user owes/gets across pools

💡 Future Add-ons (not in core 15 steps but possible later)
QR/UPI integration (via Razorpay, BharatPe, etc.)

Login with Google (optional)

Real-time updates with channels/sockets

REST API using Django REST Framework

------------------------------------------------------------------------------------------------------XXX------------------------------------------------------------------------------------------------------------
