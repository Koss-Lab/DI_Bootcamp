# weather_cli.py
import os
from dotenv import load_dotenv
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons import exceptions as owm_exc

# ------------------ OFFLINE SAMPLES (pour démo/backup) ------------------
SAMPLES = {
    "Tel Aviv,IL": {
        "current": {
            "status": "clear sky", "temp_c": 29.0, "humidity": 62,
            "wind_speed": 2.6, "wind_deg": 40,
            "sunrise_iso": "2025-08-11 06:02:40+03:00",
            "sunset_iso":  "2025-08-11 19:29:38+03:00",
        }
    },
    "Brussels,BE": {
        "current": {
            "status": "clear sky", "temp_c": 19.2, "humidity": 70,
            "wind_speed": 3.1, "wind_deg": 20,
            "sunrise_iso": "2025-08-10 06:22:26+02:00",
            "sunset_iso":  "2025-08-10 21:13:36+02:00",
        },
        "forecast3h": [
            ("2025-08-11 00:00:00+00:00", "clear sky", 18.1, 68),
            ("2025-08-11 03:00:00+00:00", "clear sky", 15.3, 67),
            ("2025-08-11 06:00:00+00:00", "clear sky", 16.0, 60),
            ("2025-08-11 09:00:00+00:00", "clear sky", 24.8, 39),
            ("2025-08-11 12:00:00+00:00", "clear sky", 27.3, 26),
            ("2025-08-11 15:00:00+00:00", "clear sky", 30.6, 22),
            ("2025-08-11 18:00:00+00:00", "clear sky", 27.7, 30),
            ("2025-08-11 21:00:00+00:00", "clear sky", 21.9, 36),
        ],
        "air": {"aqi": 2, "components": {"pm2_5": 7.4, "pm10": 12.1, "o3": 91.2, "no2": 14.5, "so2": 2.0, "co": 220.0}}
    }
}
# ------------------------------------------------------------------------

load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")
if not API_KEY and not os.getenv("OWM_OFFLINE"):
    raise SystemExit("❌ OWM_API_KEY missing. Put it in .env  (or set OWM_OFFLINE=1)")

OFFLINE = os.getenv("OWM_OFFLINE") == "1"

# ---- OWM config (timeout boost + SSL toggle) ----
cfg = get_default_config()
cfg["language"] = "en"
cfg["connection"]["timeout_secs"] = 20  # + costaud vs défaut
if os.getenv("OWM_DISABLE_SSL_VERIFY") == "1":
    cfg["connection"]["verify_ssl_certs"] = False  # ⚠️ uniquement si nécessaire

owm = OWM(API_KEY or "DUMMY", cfg)
weather_mgr = owm.weather_manager()
geo_mgr = owm.geocoding_manager()
city_reg = owm.city_id_registry()
air_mgr = owm.airpollution_manager()

def net_ok():
    return not OFFLINE

# ---------- Helpers ----------
def resolve_city_id_from_registry(name, country=None, state=None):
    kwargs = {"matching": "exact"}
    if country: kwargs["country"] = country
    if state: kwargs["state"] = state
    matches = city_reg.ids_for(name, **kwargs) or city_reg.ids_for(name, country=country, matching="like")
    return matches[0][0] if matches else None

def resolve_city_id_for_location(loc):
    return resolve_city_id_from_registry(loc.name, getattr(loc, "country", None), getattr(loc, "state", None))

def choose_city():
    query = input("\nEnter a city (e.g., 'Los Angeles, US'): ").strip()
    if not query: return None, None, None
    key = None  # ex: "Brussels,BE" pour samples

    # Online geocoding
    if net_ok():
        try:
            results = geo_mgr.geocode(query, limit=5)
            if results:
                print("\nPossible matches:")
                for i, loc in enumerate(results, 1):
                    st = f", {getattr(loc, 'state', '')}" if getattr(loc, "state", None) else ""
                    print(f"[{i}] {loc.name}, {loc.country}{st} (ID: {getattr(loc, 'id', None)}, {loc.lat:.3f},{loc.lon:.3f})")
                raw = input("Choose a number: ").strip()
                digits = "".join(ch for ch in raw if ch.isdigit())
                if digits.isdigit():
                    idx = int(digits)
                    if 1 <= idx <= len(results):
                        loc = results[idx - 1]
                        city_id = resolve_city_id_for_location(loc)
                        key = f"{loc.name},{loc.country}"
                        return loc, city_id, key
                print("❌ Invalid choice.")
                return None, None, None
        except Exception as e:
            print(f"\n(Info) Online geocoding failed → using offline registry. Reason: {e}")

    # Offline registry fallback
    name, country = query, None
    if "," in query:
        parts = [p.strip() for p in query.split(",", 1)]
        name = parts[0]
        if len(parts) > 1 and len(parts[1]) >= 2:
            country = parts[1][:2].upper()

    cands = city_reg.ids_for(name, country=country, matching="exact") or city_reg.ids_for(name, country=country, matching="like")
    if not cands:
        print("❌ No offline matches found in city registry.")
        return None, None, None

    print("\nOffline matches (city registry):")
    for i, t in enumerate(cands[:5], 1):
        cid, nm, cc, st, lat, lon = t
        st_label = f", {st}" if st else ""
        print(f"[{i}] {nm}, {cc}{st_label} (ID: {cid}, {lat:.3f},{lon:.3f})")
    raw = input("Choose a number: ").strip()
    digits = "".join(ch for ch in raw if ch.isdigit())
    if digits.isdigit():
        idx = int(digits)
        if 1 <= idx <= min(5, len(cands)):
            cid, nm, cc, st, lat, lon = cands[idx - 1]
            class LocLike:
                def __init__(self, name, country, state, lat, lon, cid):
                    self.name = name; self.country = country; self.state = state
                    self.lat = lat; self.lon = lon; self.id = cid
            key = f"{nm},{cc}"
            return LocLike(nm, cc, st, lat, lon, cid), cid, key

    print("❌ Invalid choice.")
    return None, None, None

# ---------- Weather sections ----------
def print_tel_aviv_weather():
    title = "\n=== Tel Aviv, IL — Current Weather ==="
    # online
    if net_ok():
        try:
            obs = weather_mgr.weather_at_place("Tel Aviv,IL")
            w = obs.weather
            print(title)
            print(f"Status      : {w.detailed_status}")
            print(f"Temperature : {w.temperature('celsius')['temp']}°C")
            print(f"Humidity    : {w.humidity}%")
            wind = w.wind()
            print(f"Wind        : {wind.get('speed')} m/s, dir {wind.get('deg')}°")
            print(f"Sunrise     : {w.sunrise_time('iso')}")
            print(f"Sunset      : {w.sunset_time('iso')}")
            return
        except (owm_exc.PyOWMError, Exception) as e:
            print(f"\n(Info) Tel Aviv current failed: {e}\n(Continuing with offline sample if available)")

    # offline sample
    sample = SAMPLES.get("Tel Aviv,IL", {}).get("current")
    if sample:
        print(title)
        print(f"Status      : {sample['status']}")
        print(f"Temperature : {sample['temp_c']}°C")
        print(f"Humidity    : {sample['humidity']}%")
        print(f"Wind        : {sample['wind_speed']} m/s, dir {sample['wind_deg']}°")
        print(f"Sunrise     : {sample['sunrise_iso']}")
        print(f"Sunset      : {sample['sunset_iso']}")
    else:
        print(title)
        print("(offline) No sample available.")

def show_current_weather(loc, city_id, sample_key=None):
    title = f"\n=== {loc.name}, {loc.country} — Current Weather ==="
    # online
    if net_ok():
        try:
            if isinstance(city_id, int):
                obs = weather_mgr.weather_at_id(city_id)
                id_label = city_id
            else:
                obs = weather_mgr.weather_at_coords(loc.lat, loc.lon)
                id_label = "N/A"
            w = obs.weather
            print(title)
            print(f"(City ID: {id_label})")
            print(f"Status      : {w.detailed_status}")
            print(f"Temperature : {w.temperature('celsius').get('temp')}°C")
            print(f"Humidity    : {w.humidity}%")
            wind = w.wind()
            print(f"Wind        : {wind.get('speed','?')} m/s, dir {wind.get('deg','?')}°")
            print(f"Sunrise     : {w.sunrise_time('iso')}")
            print(f"Sunset      : {w.sunset_time('iso')}")
            return
        except (owm_exc.PyOWMError, Exception) as e:
            print(f"\n❌ Current weather failed: {e}\n(Showing offline sample if available)")

    # offline
    s = SAMPLES.get(sample_key or "", {}).get("current")
    print(title)
    if s:
        print(f"(City ID: {city_id if city_id else 'N/A'})")
        print(f"Status      : {s['status']}")
        print(f"Temperature : {s['temp_c']}°C")
        print(f"Humidity    : {s['humidity']}%")
        print(f"Wind        : {s['wind_speed']} m/s, dir {s['wind_deg']}°")
        print(f"Sunrise     : {s['sunrise_iso']}")
        print(f"Sunset      : {s['sunset_iso']}")
    else:
        print("(offline) No sample available.")

def show_forecast_3h(loc, city_id, sample_key=None):
    print("\n--- Next 24h (3-hour steps) ---")
    # online
    if net_ok():
        try:
            if isinstance(city_id, int):
                forecaster = weather_mgr.forecast_at_id(city_id, '3h')
            else:
                forecaster = weather_mgr.forecast_at_coords(loc.lat, loc.lon, '3h')
            forecast = forecaster.forecast
            weathers = getattr(forecast, "weathers", list(forecast))
            for w in weathers[:8]:
                print(f"{w.reference_time('iso')} → {w.detailed_status}, "
                      f"{w.temperature('celsius')['temp']}°C, hum {w.humidity}%")
            return
        except owm_exc.UnauthorizedError:
            print("Your plan does not allow this endpoint. Ask to enable '5 day / 3 hour' API or upgrade.")
            return
        except (owm_exc.PyOWMError, Exception) as e:
            print(f"Error: {e}\n(Showing offline sample if available)")

    # offline
    rows = SAMPLES.get(sample_key or "", {}).get("forecast3h")
    if rows:
        for ts, status, temp, hum in rows:
            print(f"{ts} → {status}, {temp}°C, hum {hum}%")
    else:
        print("(offline) No sample available.")

def show_air_pollution(loc, sample_key=None):
    print("\n--- Air Pollution ---")
    # online
    if net_ok():
        try:
            aq = air_mgr.air_quality_at_coords(loc.lat, loc.lon)
            data = aq.to_dict()
            aqi = data.get("aqi")
            comps = data.get("components", {}) or {}
            print(f"AQI (1=Good … 5=Very Poor): {aqi if aqi is not None else '?'}")
            for k in sorted(comps.keys()):
                print(f"{k.upper():<6}: {comps[k]} μg/m³")
            return
        except owm_exc.UnauthorizedError:
            print("This endpoint is not enabled on your API plan.")
            return
        except (owm_exc.PyOWMError, Exception) as e:
            print(f"Error: {e}\n(Showing offline sample if available)")

    # offline
    s = SAMPLES.get(sample_key or "", {}).get("air")
    if s:
        print(f"AQI (1=Good … 5=Very Poor): {s.get('aqi','?')}")
        for k, v in s.get("components", {}).items():
            print(f"{k.upper():<6}: {v} μg/m³")
    else:
        print("(offline) No sample available.")

# ---------- Main ----------
def main():
    print_tel_aviv_weather()

    loc, city_id, sample_key = choose_city()
    if loc:
        show_current_weather(loc, city_id, sample_key)
        show_forecast_3h(loc, city_id, sample_key)
        show_air_pollution(loc, sample_key)

    print("\n✅ Done.")

if __name__ == "__main__":
    main()
