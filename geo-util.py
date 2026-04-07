from geopy.distance import geodesic
import time

def check_location(user_lat, user_lon, office_lat, office_lon, radius):
    """
    Ishchi ruxsat etilgan radius ichidami yoki yo'qligini tekshiradi.
    """
    user_coords = (user_lat, user_lon)
    office_coords = (office_lat, office_lon)
    
    distance = geodesic(user_coords, office_coords).meters
    return distance <= radius, distance

def is_fake_gps(timestamp):
    """
    Server vaqti bilan solishtirish (oddiy anti-cheat mantiqi).
    """
    server_time = time.time()
    # Agar vaqtlar orasidagi farq juda katta bo'lsa (masalan 5 min), shubha bor
    if abs(server_time - timestamp) > 300:
        return True
    return False