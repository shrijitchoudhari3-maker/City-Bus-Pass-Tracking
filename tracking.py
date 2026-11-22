"""Deterministic simulated GPS positions for jury demonstration."""
from datetime import datetime
import math, time

# Each route is a short illustrative polyline around Pune. Coordinates are sample data.
BUSES = [
    {"bus_id":"BUS-101","route":"Hadapsar – Magarpatta – Shivajinagar",
     "path":[(18.5018,73.9270),(18.5080,73.9250),(18.5160,73.9200),(18.5250,73.9050),(18.5300,73.8500)],
     "speed":1.0,"status":"Running","eta":12},
    {"bus_id":"BUS-202","route":"Katraj – Swargate – Deccan",
     "path":[(18.4520,73.8580),(18.4660,73.8610),(18.4800,73.8560),(18.5010,73.8580)],
     "speed":0.65,"status":"Running","eta":8},
    {"bus_id":"BUS-303","route":"Wakad – Aundh – University",
     "path":[(18.5980,73.7650),(18.5700,73.7780),(18.5600,73.8070),(18.5520,73.8250)],
     "speed":0.0,"status":"Stopped","eta":18},
    {"bus_id":"BUS-404","route":"Pune Station – Shivajinagar – Hinjawadi",
     "path":[(18.5280,73.8740),(18.5350,73.8500),(18.5500,73.8200),(18.5900,73.7900)],
     "speed":0.0,"status":"Offline","eta":None},
]

def get_bus_positions(now=None):
    """Return moving positions; time-based interpolation makes refreshes visibly move."""
    t = time.time() if now is None else float(now)
    output = []
    for idx, bus in enumerate(BUSES):
        path = bus["path"]
        if bus["status"] == "Offline":
            lat, lon = path[0]
        elif bus["status"] == "Stopped":
            lat, lon = path[min(1, len(path)-1)]
        else:
            segment_count = len(path)-1
            phase = (t / (22.0 / bus["speed"]) + idx * 0.37) % segment_count
            seg = int(phase)
            frac = phase - seg
            lat = path[seg][0] + (path[seg+1][0]-path[seg][0])*frac
            lon = path[seg][1] + (path[seg+1][1]-path[seg][1])*frac
        output.append({
            "bus_id":bus["bus_id"],"route":bus["route"],"lat":round(lat,6),
            "lon":round(lon,6),"status":bus["status"],
            "eta":f"{bus['eta']} min" if bus["eta"] is not None else "Unavailable",
            "updated":datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })
    return output

def get_route_options():
    return [b["route"] for b in BUSES]
