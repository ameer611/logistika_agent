import time
import random
import requests
from datetime import datetime, timedelta

BACKEND_URL = "http://backend:8000/api/zaproslar"

# Seeder bilan bir xil markaziy GPS koordinatalar
VILOYAT_GPS = {
    "Toshkent": (41.2995, 69.2401),
    "Samarqand": (39.6542, 66.9597),
    "Buxoro": (39.7747, 64.4286),
    "Andijon": (40.7821, 72.3442),
    "Farg'ona": (40.3842, 71.7843),
    "Namangan": (40.9983, 71.6726),
    "Navoiy": (40.0844, 65.3792),
    "Xorazm": (41.5568, 60.6307),
    "Jizzax": (40.1158, 67.8422),
    "Sirdaryo": (40.8389, 68.6617),
    "Qashqadaryo": (38.8610, 65.7847),
    "Surxondaryo": (37.9409, 67.2617)
}

def get_random_gps_in_region(viloyat: str) -> str:
    """Seeder bilan bir xil algoritm: viloyat atrofida tasodifiy GPS yaratadi"""
    center_lat, center_lon = VILOYAT_GPS[viloyat]
    lat = center_lat + random.uniform(-0.15, 0.15)
    lon = center_lon + random.uniform(-0.15, 0.15)
    return f"{lat:.4f},{lon:.4f}"

def generate_mock_data():
    viloyatlar_list = list(VILOYAT_GPS.keys())
    
    # Yuk ortish joyi formati: "Viloyat (LAT,LON)"
    yuk_ortish_viloyat = random.choice(viloyatlar_list)
    yuk_ortish_joyi = f"{yuk_ortish_viloyat} ({get_random_gps_in_region(yuk_ortish_viloyat)})"
    
    # Yuk tushirish joyi yuk ortish joyi bilan bir xil bo'lmasligi kerak
    yuk_tushirish_viloyat = random.choice([v for v in viloyatlar_list if v != yuk_ortish_viloyat])
    yuk_tushirish_joyi = f"{yuk_tushirish_viloyat} ({get_random_gps_in_region(yuk_tushirish_viloyat)})"
    
    return {
        "yuk_ortish_joyi": yuk_ortish_joyi,
        "yuk_tushirish_joyi": yuk_tushirish_joyi,
        "yuklash_sanasi": (datetime.now() + timedelta(days=random.randint(1, 5))).isoformat()
    }

if __name__ == "__main__":
    print("Streamer simulator seeder formatiga mos ravishda ishga tushdi...")
    # Backend to'liq yonib, seed qilib bo'lishini kutamiz
    time.sleep(15) 
    
    while True:
        try:
            payload = generate_mock_data()
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 201:
                print(f"Zapros yuborildi! Ortish: {payload['yuk_ortish_joyi']} -> Tushirish: {payload['yuk_tushirish_joyi']}. ID: {response.json().get('id')}")
            else:
                print(f"Xatolik yuz berdi. Status: {response.status_code}")
        except Exception as e:
            print(f"Streamer xatoligi (Backend ulanmadi): {e}")
            
        # 1 dan 10 daqiqagacha tasodifiy kutish
        sleep_interval = random.randint(60, 100)
        time.sleep(sleep_interval)