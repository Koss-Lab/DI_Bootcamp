#air_traffic.py

from datetime import date

# Airline class
class Airline:
    def __init__(self, id_code, name):
        self.id = id_code          # Ex: "AF"
        self.name = name           # Ex: "Air France"
        self.planes = []           # List of Airplane instances

# Airplane class
class Airplane:
    def __init__(self, id_number, current_location, company):
        self.id = id_number                # Ex: 101
        self.current_location = current_location  # Airport instance
        self.company = company            # Airline instance
        self.next_flights = []            # List of Flight instances (future only)

        # Add this plane to its location and company
        self.current_location.planes.append(self)
        self.company.planes.append(self)

    def fly(self, destination):
        # Simulate takeoff/landing for a flight to given destination
        for flight in self.next_flights:
            if flight.destination == destination:
                flight.take_off()
                flight.land()
                # Remove the flight after flying
                self.next_flights = [f for f in self.next_flights if f != flight]
                return
        print(f"No scheduled flight to {destination.city} found for plane {self.id}.")

    def location_on_date(self, target_date):
        # Simulate future location of the plane on a given date
        location = self.current_location
        for flight in self.next_flights:
            if flight.date > target_date:
                break
            location = flight.destination
        return location

    def available_on_date(self, target_date, location):
        # Check if plane can fly from given location on this date
        if self.location_on_date(target_date) != location:
            return False
        for flight in self.next_flights:
            if flight.date == target_date:
                return False
        return True

# Flight class
class Flight:
    def __init__(self, flight_date, origin, destination, plane):
        self.date = flight_date              # datetime.date object
        self.origin = origin                 # Airport instance
        self.destination = destination       # Airport instance
        self.plane = plane                   # Airplane instance

        self.id = f"{destination.city}-{plane.company.id}-{flight_date.strftime('%Y%m%d')}"
        # Automatically add flight to relevant lists
        plane.next_flights = self._insert_sorted(plane.next_flights, self)
        origin.scheduled_departures = self._insert_sorted(origin.scheduled_departures, self)
        destination.scheduled_arrivals = self._insert_sorted(destination.scheduled_arrivals, self)

    def take_off(self):
        if self.plane in self.origin.planes:
            self.origin.planes.remove(self.plane)
        else:
            print(f"Plane {self.plane.id} was not at origin {self.origin.city}.")

    def land(self):
        self.destination.planes.append(self.plane)
        self.plane.current_location = self.destination

    def _insert_sorted(self, lst, flight):
        # Manual insertion by date (no sorted())
        result = []
        inserted = False
        for f in lst:
            if not inserted and flight.date < f.date:
                result.append(flight)
                inserted = True
            result.append(f)
        if not inserted:
            result.append(flight)
        return result

# Airport class
class Airport:
    def __init__(self, city_code):
        self.city = city_code                        # Ex: "TLV"
        self.planes = []                             # List of planes currently here
        self.scheduled_departures = []               # List of future flights from here
        self.scheduled_arrivals = []                 # List of future flights to here

    def schedule_flight(self, destination, flight_date):
        # Find a plane that can fly that day from this airport
        for airline in airlines:
            for plane in airline.planes:
                if plane.available_on_date(flight_date, self):
                    # Schedule the flight
                    Flight(flight_date, self, destination, plane)
                    print(f"✅ Flight scheduled: {self.city} → {destination.city} on {flight_date}")
                    return
        print(f"❌ No available planes for {self.city} → {destination.city} on {flight_date}")

    def info(self, start_date, end_date):
        print(f"\n📅 Scheduled flights from {self.city} between {start_date} and {end_date}:")
        for flight in self.scheduled_departures:
            if start_date <= flight.date <= end_date:
                print(f"→ {flight.date}: to {flight.destination.city} with plane {flight.plane.id}")

# TEST SECTION (demo)
if __name__ == "__main__":
    # Create airlines
    af = Airline("AF", "Air France")
    elal = Airline("LY", "El Al")
    airlines = [af, elal]

    # Create airports
    cdg = Airport("CDG")
    tlv = Airport("TLV")
    jfk = Airport("JFK")

    # Create airplanes
    plane1 = Airplane(101, cdg, af)
    plane2 = Airplane(202, tlv, elal)

    # Schedule flights
    cdg.schedule_flight(tlv, date(2025, 9, 10))
    tlv.schedule_flight(jfk, date(2025, 9, 11))
    cdg.schedule_flight(jfk, date(2025, 9, 12))  # Should fail (plane1 not available)

    # Show info for CDG
    cdg.info(date(2025, 9, 1), date(2025, 9, 30))

    # Simulate a flight
    print("\n🛫 Flying plane from CDG to TLV...")
    plane1.fly(tlv)
    print(f"📍 New location of plane {plane1.id}: {plane1.current_location.city}")
