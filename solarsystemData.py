class PlanetData:
    planet: str
    mass_10_e24_kg: str
    radius_km: str
    diameter_km: str
    density_kg_m3: int
    gravity_m_s2: str
    escape_velocity_km_s: str
    rotation_period_hours: str
    length_of_day_hours: str
    distance_from_sun_10_e6_km: str
    perihelion_10_e6_km: str
    aphelion_10_e6_km: str
    orbital_period_days: str
    orbital_velocity_km_s: str
    orbital_inclination_degrees: str
    orbital_eccentricity: str
    obliquity_to_orbit_degrees: str
    mean_temperature_c: int
    number_of_moons: int
    ring_system: str
    global_magnetic_field: str

    def __init__(self, planet: str, mass_10_e24_kg: str, radius_km: str, diameter_km: str, density_kg_m3: int, gravity_m_s2: str, escape_velocity_km_s: str, rotation_period_hours: str, length_of_day_hours: str, distance_from_sun_10_e6_km: str, perihelion_10_e6_km: str, aphelion_10_e6_km: str, orbital_period_days: str, orbital_velocity_km_s: str, orbital_inclination_degrees: str, orbital_eccentricity: str, obliquity_to_orbit_degrees: str, mean_temperature_c: int, number_of_moons: int, ring_system: str, global_magnetic_field: str) -> None:
        self.planet = planet
        self.mass_10_e24_kg = mass_10_e24_kg
        self.radius_km = radius_km
        self.diameter_km = diameter_km
        self.density_kg_m3 = density_kg_m3
        self.gravity_m_s2 = gravity_m_s2
        self.escape_velocity_km_s = escape_velocity_km_s
        self.rotation_period_hours = rotation_period_hours
        self.length_of_day_hours = length_of_day_hours
        self.distance_from_sun_10_e6_km = distance_from_sun_10_e6_km
        self.perihelion_10_e6_km = perihelion_10_e6_km
        self.aphelion_10_e6_km = aphelion_10_e6_km
        self.orbital_period_days = orbital_period_days
        self.orbital_velocity_km_s = orbital_velocity_km_s
        self.orbital_inclination_degrees = orbital_inclination_degrees
        self.orbital_eccentricity = orbital_eccentricity
        self.obliquity_to_orbit_degrees = obliquity_to_orbit_degrees
        self.mean_temperature_c = mean_temperature_c
        self.number_of_moons = number_of_moons
        self.ring_system = ring_system
        self.global_magnetic_field = global_magnetic_field
