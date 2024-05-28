class MoonData:
    moon: str
    planet: str
    mass_10_e24_kg: float
    eccentricity: float
    periapsis_10_e6_km: float
    apoapsis_10_e6_km: float
    orbital_period_days: float
    orbital_inclination_deg: float

    def __init__(self, moon: str, planet: str, mass_10_e24_kg: float, eccentricity: float, periapsis_10_e6_km: float, apoapsis_10_e6_km: float, orbital_period_days: float, orbital_inclination_deg: float) -> None:
        self.moon = moon
        self.planet = planet
        self.mass_10_e24_kg = mass_10_e24_kg
        self.eccentricity = eccentricity
        self.periapsis_10_e6_km = periapsis_10_e6_km
        self.apoapsis_10_e6_km = apoapsis_10_e6_km
        self.orbital_period_days = orbital_period_days
        self.orbital_inclination_deg = orbital_inclination_deg
