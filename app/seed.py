import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Malumot

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

HARFLAR = "ABCDEFGHJKLMNOPRSTZ"

def generate_uzb_plate() -> str:
    kod = f"{random.randint(1, 99):02d}"
    harf1 = random.choice(HARFLAR)
    raqam = f"{random.randint(0, 999):03d}"
    harf2 = "".join(random.choices(HARFLAR, k=2))
    return f"{kod}{harf1}{raqam}{harf2}"[:8]

def get_random_gps_in_region(viloyat: str) -> str:
    center_lat, center_lon = VILOYAT_GPS[viloyat]
    lat = center_lat + random.uniform(-0.15, 0.15)
    lon = center_lon + random.uniform(-0.15, 0.15)
    return f"{lat:.4f},{lon:.4f}"

def run_database_seeder():
    """Eski mashinalarni o'chirib, yangi 100 ta mashina qo'shuvchi funksiya"""
    db: Session = SessionLocal()
    try:
        print("Eski ma'lumotlar o'chirilmoqda...")
        db.query(Malumot).delete()
        db.commit()

        print("Yangi 100 ta transport vositasi generatsiya qilinmoqda...")
        generated_plates = set()
        trucks_to_add = []
        viloyatlar_list = list(VILOYAT_GPS.keys())
        
        while len(trucks_to_add) < 100:
            plate = generate_uzb_plate()
            if plate not in generated_plates:
                generated_plates.add(plate)
                
                tanlangan_viloyat = random.choice(viloyatlar_list)
                gps_lokatsiya = get_random_gps_in_region(tanlangan_viloyat)
                loriy_joy = f"{tanlangan_viloyat} ({gps_lokatsiya})"
                
                trucks_to_add.append(
                    Malumot(mashina_raqami=plate, joriy_lokatsiya=loriy_joy)
                )
                
        db.add_all(trucks_to_add)
        db.commit()
        print(f"Seeder muvaffaqiyatli tugadi: {len(trucks_to_add)} ta yangi mashina qo'shildi.")
    except Exception as e:
        print(f"Seederda xatolik: {e}")
        db.rollback()
    finally:
        db.close()