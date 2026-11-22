import streamlit as st
import pandas as pd
import io
import cv2
import numpy as np
import qrcode
from datetime import date, datetime, timedelta
from database import (
    init_db, register_user, authenticate_user, create_pass, get_user_passes,
    get_all_passes, update_pass_status, get_stats
)
from tracking import get_bus_positions, get_route_options
from pricing import calculate_pass_price, route_base_fare

st.set_page_config(page_title="City Bus Pass & Tracking", page_icon="🚌", layout="wide")
init_db()

ROUTES = {
    "Hadapsar – Magarpatta – Shivajinagar": {"fare": 20, "duration_km": 18},
    "Katraj – Swargate – Deccan": {"fare": 15, "duration_km": 13},
    "Wakad – Aundh – University": {"fare": 18, "duration_km": 16},
    "Pune Station – Shivajinagar – Hinjawadi": {"fare": 25, "duration_km": 22},
}
VALIDITIES = [7, 30, 90]

def init_session():
    for key, default in {"user": None, "page": "Home"}.items():
        if key not in st.session_state:
            st.session_state[key] = default
init_session()

def sidebar():
    st.sidebar.title("🚌 City Bus System")
    if st.session_state.user:
        st.sidebar.success(f"Signed in: {st.session_state.user['name']}")
        pages = ["Home", "Bus Routes", "Apply for Pass", "My Bus Passes",
                 "QR Code Validation", "Bus Tracking", "Delay Alerts"]
        if st.session_state.user["role"] == "admin":
            pages += ["Admin Dashboard"]
        selected = st.sidebar.radio("Navigation", pages)
        if st.sidebar.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
        return selected
    return "Login / Register"

def auth_page():
    st.title("🚌 City Bus Pass & Tracking System")
    login_tab, register_tab = st.tabs(["Login", "Register"])
    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                user = authenticate_user(email.strip().lower(), password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
    with register_tab:
        with st.form("register_form"):
            name = st.text_input("Full name")
            email = st.text_input("Email address")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            if st.form_submit_button("Create account", use_container_width=True):
                if not name.strip() or not email.strip() or "@" not in email:
                    st.error("Enter a valid name and email.")
                elif len(password) < 6:
                    st.error("Password must contain at least 6 characters.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif register_user(name.strip(), email.strip().lower(), password):
                    st.success("Account created. Please log in.")
                else:
                    st.error("This email is already registered.")

def home():
    st.title("Welcome to City Bus Pass & Tracking")
    st.write("A student-friendly demo for digital bus passes, QR-based digital passes and bus tracking.")
    a,b,c = st.columns(3)
    a.metric("Available routes", len(ROUTES))
    b.metric("Pass validity options", "7 / 30 / 90 days")
    c.metric("Tracking mode", "Simulated GPS")
    st.info("Tracking coordinates and delay alerts in this version are simulated for demonstration. No real bus GPS is connected.")

def routes_page():
    st.title("🗺️ Bus Routes")
    q = st.text_input("Search routes", placeholder="Enter route, stop or destination")
    matches = {n:v for n,v in ROUTES.items() if q.lower() in n.lower()}
    if not matches:
        st.warning("No matching routes found.")
    for name, info in matches.items():
        with st.expander(name, expanded=True):
            st.write(f"Estimated route distance: **{info['duration_km']} km**")
            st.write(f"Base one-day fare: **₹{info['fare']}**")
            st.caption("Stops are illustrative for the academic demonstration.")

def apply_pass():
    st.title("🎫 Apply for Digital Bus Pass")
    with st.form("pass_form"):
        route = st.selectbox("Select route", list(ROUTES.keys()))
        days = st.selectbox("Pass validity", VALIDITIES, format_func=lambda x: f"{x} days")
        start = st.date_input("Pass start date", min_value=date.today(), value=date.today())
        price = calculate_pass_price(ROUTES[route]["fare"], days)
        st.info(f"Estimated pass price: ₹{price:.2f}  |  Base fare ₹{ROUTES[route]['fare']}/day")
        if days == 30:
            st.caption("Includes a suggested 20% long-duration discount.")
        elif days == 90:
            st.caption("Includes a suggested 40% long-duration discount.")
        else:
            st.caption("7-day pass: standard route fare × validity.")
        submitted = st.form_submit_button("Generate Bus Pass", use_container_width=True)
    if submitted:
        pass_id = create_pass(st.session_state.user["id"], route, days, start.isoformat(), price)
        st.success(f"Pass generated successfully! Pass ID: {pass_id}")
        st.write(f"**Amount saved:** ₹{price:.2f}")
        st.caption("Your QR code is available under My Bus Passes. Show it at the validation counter.")

def my_passes():
    st.title("🎫 My Bus Passes")
    rows = get_user_passes(st.session_state.user["id"])
    if not rows:
        st.info("You have not generated a bus pass yet.")
        return
    for p in rows:
        with st.container(border=True):
            col1,col2,col3 = st.columns([3,1,1])
            col1.subheader(p["pass_id"])
            col1.write(p["route"])
            col1.write(f"Validity: {p['start_date']} to {p['end_date']}")
            col2.metric("Price", f"₹{p['price']:.2f}")
            col3.metric("Status", p["status"])
            qr = qrcode.QRCode(version=1, box_size=8, border=4)
            qr.add_data(p["qr_token"])
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_buffer = io.BytesIO()
            qr_image.save(qr_buffer, format="PNG")
            col1.image(qr_buffer.getvalue(), caption="Scan this QR code to validate your bus pass", width=220)

def qr_code_validation():
    st.title("📷 QR Code Validation")
    st.write("Scan the QR code using your camera or upload a QR-code image to verify the bus pass.")
    camera_image = st.camera_input("Scan bus pass QR code with camera")
    uploaded_image = st.file_uploader("Or upload a QR code image", type=["png", "jpg", "jpeg"])
    image_file = camera_image if camera_image is not None else uploaded_image
    if image_file is not None:
        image_bytes = np.frombuffer(image_file.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        detector = cv2.QRCodeDetector()
        token, points, _ = detector.detectAndDecode(image)
        if token:
            from database import validate_pass_token
            result = validate_pass_token(token.strip())
            if result:
                st.success(f"Valid pass: {result['pass_id']} — {result['route']}")
                st.write(f"Passenger: {result['pass_id']} | Status: {result['status']} | Valid until: {result['end_date']}")
            else:
                st.error("QR code detected, but the pass is invalid, expired, or inactive.")
        else:
            st.error("Could not read a QR code. Please try again with a clear, well-lit image.")

def tracking_page():
    st.title("📍 Bus Tracking — Simulated GPS")
    st.caption("Demonstration mode: bus coordinates move automatically along sample Pune routes. These are not real GPS readings.")
    interval = st.slider("Refresh interval (seconds)", 5, 30, 10, 5)
    st.write(f"Auto-refresh is enabled every {interval} seconds.")
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=interval * 1000, key="bus_tracking_refresh")
    except Exception:
        st.warning("Optional auto-refresh package is unavailable. Use the Refresh button to update positions.")
    if st.button("🔄 Refresh bus positions"):
        st.rerun()
    buses = get_bus_positions()
    df = pd.DataFrame([{
        "Bus": b["bus_id"], "Route": b["route"], "Status": b["status"],
        "Latitude": b["lat"], "Longitude": b["lon"], "ETA": b["eta"],
        "Last updated": b["updated"]
    } for b in buses])
    for b in buses:
        status_color = {"Running":"🟢","Stopped":"🟠","Offline":"🔴"}[b["status"]]
        st.write(f"{status_color} **{b['bus_id']} — {b['status']}** | ETA: {b['eta']} | {b['route']}")
    st.map(df.rename(columns={"Latitude":"lat","Longitude":"lon"})[["lat","lon"]], latitude="lat", longitude="lon", size=80)
    st.dataframe(df, use_container_width=True, hide_index=True)

def delay_alerts():
    st.title("🔔 Delay Alerts")
    st.caption("Sample alerts are simulated for the jury demonstration.")
    alerts = [
        ("BUS-101", "Hadapsar – Magarpatta – Shivajinagar", 8, "Traffic near Magarpatta"),
        ("BUS-202", "Katraj – Swargate – Deccan", 5, "Heavy traffic near Swargate"),
        ("BUS-303", "Wakad – Aundh – University", 0, "Running on schedule"),
    ]
    for bus, route, delay, reason in alerts:
        if delay:
            st.warning(f"**{bus}** — {route}: approximately {delay} minutes delayed. {reason}.")
        else:
            st.success(f"**{bus}** — {route}: running on schedule.")

def admin_page():
    st.title("🛠️ Admin Dashboard")
    stats = get_stats()
    c1,c2,c3 = st.columns(3)
    c1.metric("Registered users", stats["users"])
    c2.metric("Total passes", stats["passes"])
    c3.metric("Active passes", stats["active"])
    rows = get_all_passes()
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Download pass report (CSV)", df.to_csv(index=False), "bus_pass_report.csv", "text/csv")
        pass_id = st.text_input("Pass ID to update")
        action = st.selectbox("Action", ["Active", "Revoked"])
        if st.button("Update pass status"):
            if update_pass_status(pass_id.strip(), action):
                st.success("Pass status updated.")
                st.rerun()
            else:
                st.error("Pass ID not found.")

page = sidebar()
if not st.session_state.user:
    auth_page()
elif page == "Home": home()
elif page == "Bus Routes": routes_page()
elif page == "Apply for Pass": apply_pass()
elif page == "My Bus Passes": my_passes()
elif page == "QR Code Validation": qr_code_validation()
elif page == "Bus Tracking": tracking_page()
elif page == "Delay Alerts": delay_alerts()
elif page == "Admin Dashboard": admin_page()
