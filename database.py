import sqlite3, uuid, hashlib, os
from datetime import date, timedelta

DB_NAME = os.environ.get("CITYBUS_DB", "citybus.db")

def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password, salt=None):
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120000).hex()
    return salt, digest

def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL, salt TEXT NOT NULL, password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user')""")
        c.execute("""CREATE TABLE IF NOT EXISTS passes(
            id INTEGER PRIMARY KEY AUTOINCREMENT, pass_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL, route TEXT NOT NULL, validity_days INTEGER NOT NULL,
            start_date TEXT NOT NULL, end_date TEXT NOT NULL, price REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Active', qr_token TEXT UNIQUE NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id))""")
        # Safe migration for databases created by the earlier project version.
        cols = [r["name"] for r in c.execute("PRAGMA table_info(passes)").fetchall()]
        if "price" not in cols:
            c.execute("ALTER TABLE passes ADD COLUMN price REAL NOT NULL DEFAULT 0")
        # Seed a demo administrator only if it does not already exist.
        if not c.execute("SELECT id FROM users WHERE email=?", ("admin@citybus.local",)).fetchone():
            salt, digest = hash_password("Admin@123")
            c.execute("INSERT INTO users(name,email,salt,password_hash,role) VALUES(?,?,?,?,?)",
                      ("System Admin","admin@citybus.local",salt,digest,"admin"))

def register_user(name, email, password):
    salt, digest = hash_password(password)
    try:
        with connect() as c:
            c.execute("INSERT INTO users(name,email,salt,password_hash) VALUES(?,?,?,?)",
                      (name,email,salt,digest))
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(email, password):
    with connect() as c:
        row = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not row: return None
    _, digest = hash_password(password, row["salt"])
    if digest != row["password_hash"]: return None
    return {"id":row["id"],"name":row["name"],"email":row["email"],"role":row["role"]}

def create_pass(user_id, route, days, start_date, price):
    start = date.fromisoformat(start_date)
    end = start + timedelta(days=int(days)-1)
    pass_id = "CBP-" + uuid.uuid4().hex[:8].upper()
    token = uuid.uuid4().hex
    with connect() as c:
        c.execute("""INSERT INTO passes(pass_id,user_id,route,validity_days,start_date,end_date,price,status,qr_token)
                     VALUES(?,?,?,?,?,?,?,'Active',?)""",
                  (pass_id,user_id,route,int(days),start.isoformat(),end.isoformat(),float(price),token))
    return pass_id

def get_user_passes(user_id):
    with connect() as c:
        return [dict(r) for r in c.execute("SELECT * FROM passes WHERE user_id=? ORDER BY id DESC",(user_id,)).fetchall()]

def get_all_passes():
    with connect() as c:
        return [dict(r) for r in c.execute("""SELECT p.pass_id,u.name,u.email,p.route,p.validity_days,
            p.start_date,p.end_date,p.price,p.status FROM passes p JOIN users u ON u.id=p.user_id
            ORDER BY p.id DESC""").fetchall()]

def validate_pass_token(token):
    if not token: return None
    with connect() as c:
        row = c.execute("SELECT * FROM passes WHERE qr_token=?", (token,)).fetchone()
    if not row or row["status"] != "Active" or row["end_date"] < date.today().isoformat():
        return None
    return dict(row)

def update_pass_status(pass_id, status):
    if status not in ("Active","Revoked"): return False
    with connect() as c:
        cur = c.execute("UPDATE passes SET status=? WHERE pass_id=?",(status,pass_id))
        return cur.rowcount > 0

def get_stats():
    with connect() as c:
        users = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        passes = c.execute("SELECT COUNT(*) FROM passes").fetchone()[0]
        active = c.execute("SELECT COUNT(*) FROM passes WHERE status='Active'").fetchone()[0]
    return {"users":users,"passes":passes,"active":active}
