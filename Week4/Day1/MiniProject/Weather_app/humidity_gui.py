# humidity_gui.py
import os
from collections import defaultdict
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons import exceptions as owm_exc

# -------- Offline samples (mêmes données que le CLI) --------
SAMPLES = {
    "Tel Aviv,IL": {
        "forecast3h": [
            ("2025-08-11 00:00:00+03:00", 68),
            ("2025-08-11 03:00:00+03:00", 67),
            ("2025-08-11 06:00:00+03:00", 60),
            ("2025-08-11 09:00:00+03:00", 52),
            ("2025-08-11 12:00:00+03:00", 45),
            ("2025-08-11 15:00:00+03:00", 40),
            ("2025-08-11 18:00:00+03:00", 48),
            ("2025-08-11 21:00:00+03:00", 55),
            # jour 2
            ("2025-08-12 00:00:00+03:00", 60),
            ("2025-08-12 03:00:00+03:00", 58),
            ("2025-08-12 06:00:00+03:00", 54),
            ("2025-08-12 09:00:00+03:00", 42),
            ("2025-08-12 12:00:00+03:00", 35),
            ("2025-08-12 15:00:00+03:00", 33),
            ("2025-08-12 18:00:00+03:00", 45),
            ("2025-08-12 21:00:00+03:00", 52),
            # jour 3
            ("2025-08-13 00:00:00+03:00", 62),
            ("2025-08-13 03:00:00+03:00", 60),
            ("2025-08-13 06:00:00+03:00", 56),
            ("2025-08-13 09:00:00+03:00", 46),
            ("2025-08-13 12:00:00+03:00", 38),
            ("2025-08-13 15:00:00+03:00", 34),
            ("2025-08-13 18:00:00+03:00", 47),
            ("2025-08-13 21:00:00+03:00", 53),
        ]
    },
    "Brussels,BE": {
        "forecast3h": [
            ("2025-08-11 00:00:00+02:00", 68),
            ("2025-08-11 03:00:00+02:00", 67),
            ("2025-08-11 06:00:00+02:00", 60),
            ("2025-08-11 09:00:00+02:00", 39),
            ("2025-08-11 12:00:00+02:00", 26),
            ("2025-08-11 15:00:00+02:00", 22),
            ("2025-08-11 18:00:00+02:00", 30),
            ("2025-08-11 21:00:00+02:00", 36),
            # jour 2 & 3 (exemple)
            ("2025-08-12 00:00:00+02:00", 60),
            ("2025-08-12 03:00:00+02:00", 58),
            ("2025-08-12 06:00:00+02:00", 55),
            ("2025-08-12 09:00:00+02:00", 44),
            ("2025-08-12 12:00:00+02:00", 33),
            ("2025-08-12 15:00:00+02:00", 28),
            ("2025-08-12 18:00:00+02:00", 35),
            ("2025-08-12 21:00:00+02:00", 40),
            ("2025-08-13 00:00:00+02:00", 63),
            ("2025-08-13 03:00:00+02:00", 60),
            ("2025-08-13 06:00:00+02:00", 58),
            ("2025-08-13 09:00:00+02:00", 47),
            ("2025-08-13 12:00:00+02:00", 36),
            ("2025-08-13 15:00:00+02:00", 31),
            ("2025-08-13 18:00:00+02:00", 38),
            ("2025-08-13 21:00:00+02:00", 43),
        ]
    }
}
# ------------------------------------------------------------

def load_mgrs():
    load_dotenv()
    api = os.getenv("OWM_API_KEY")
    offline = os.getenv("OWM_OFFLINE") == "1"
    cfg = get_default_config()
    cfg["language"] = "en"
    cfg["connection"]["timeout_secs"] = 20
    if os.getenv("OWM_DISABLE_SSL_VERIFY") == "1":
        cfg["connection"]["verify_ssl_certs"] = False
    owm = OWM(api or "DUMMY", cfg)
    return offline, owm.weather_manager(), owm.geocoding_manager()

def init_plot(ax, city_label):
    ax.set_title(f"3-Day Humidity Forecast — {city_label}")
    ax.set_ylabel("Humidity (%)")
    ax.set_xlabel("Day")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.25)

def write_humidity_on_bar_chart(ax, bars, humidities):
    for bar, h in zip(bars, humidities):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*0.85,
                f"{int(round(h))}%", ha="center", va="center",
                fontweight="bold", color="white")

def plot_temperatures(ax, labels, humidities):
    # (Nom de fonction demandé par l’énoncé, on trace l’humidité)
    bars = ax.bar(labels, humidities)
    return bars

def fetch_3h_offline(city_key):
    rows = SAMPLES.get(city_key, {}).get("forecast3h", [])
    if not rows:
        return []
    out = []
    for ts, hum in rows:
        # ts déjà ISO avec timezone, on garde
        out.append((datetime.fromisoformat(ts), hum))
    return out

def fetch_3h_online(geo_mgr, weather_mgr, query):
    # Résout un ID via geocode, puis forecast_at_id
    locs = geo_mgr.geocode(query, limit=1)
    if not locs:
        raise RuntimeError("No geocoding results")
    loc = locs[0]
    forecaster = weather_mgr.forecast_at_coords(loc.lat, loc.lon, '3h')
    forecast = forecaster.forecast
    weathers = getattr(forecast, "weathers", list(forecast))
    out = []
    for w in weathers:
        # reference_time('date') → timezone-aware UTC; on convertira juste par label
        out.append((w.reference_time('date'), w.humidity))
    return out

def aggregate_daily_labels(points, tz: str, days=3):
    """
    points: list[(datetime-aware, humidity int)]
    Retourne (labels ['MM/DD', ...], values [avg humidity])
    """
    zone = pytz.timezone(tz)
    bucket = defaultdict(list)
    for dt, hum in points:
        local = dt.astimezone(zone)
        key = local.strftime("%m/%d")
        bucket[key].append(hum)
    labels, values = [], []
    for key in sorted(bucket.keys())[:days]:
        vals = bucket[key]
        values.append(sum(vals)/len(vals))
        labels.append(key)
    while len(labels) < days:
        labels.append("--/--"); values.append(0)
    return labels, values

def main():
    offline, weather_mgr, geo_mgr = load_mgrs()
    query = input("City for GUI (e.g., 'Tel Aviv, IL' or 'Brussels, BE'): ").strip() or "Tel Aviv, IL"
    city_key = query.replace(" ", "").replace(","," ,").replace(" ,",",")  # normalisation light
    # Déterminer un fuseau simple (heuristique cool)
    tz_guess = "Asia/Jerusalem" if "Tel" in query or "IL" in query else "Europe/Brussels"

    # Récup data
    try:
        if not offline:
            points = fetch_3h_online(geo_mgr, weather_mgr, query)
        else:
            raise RuntimeError("forced offline")
    except Exception:
        points = fetch_3h_offline(city_key.replace(" ", "")) or fetch_3h_offline("Tel Aviv,IL")

    labels, humidities = aggregate_daily_labels(points, tz=tz_guess, days=3)

    # Plot
    fig, ax = plt.subplots(figsize=(7,5))
    try:
        fig.canvas.manager.set_window_title("PyOWM Humidity Forecast")
    except Exception:
        pass
    init_plot(ax, city_label=query)
    bars = plot_temperatures(ax, labels, humidities)
    write_humidity_on_bar_chart(ax, bars, humidities)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
