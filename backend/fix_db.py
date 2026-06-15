from models.database import SessionLocal
from models.order import Order
from models.listing import Listing

db = SessionLocal()

custom_names = [
    'Apple AirPods Pro (2nd Gen) with MagSafe Case',
    'Apple iPad mini',
    'Zebronics Jet PRO Premium Wired Gaming On Ear Headphone with LED for Headband + earcups, 40mm Neodymium Drivers, 2 Meter Braided Cable, with mic, Suspension Design, 3.5mm + USB Connector (Black, Blue)',
    'AGARO COSMIC PLUS Sonic Electric Tooth Brush For Adults With 5 Modes, 5 Brush Heads, 1 Interdental Head, Carry Case & Rechargeable With 4 Hours Charge Lasting Up To 25 Days, Power Toothbrush, (Black)',
    'Boat Rockerz 113, 40H Battery, Dual Pair, Fast Charge, ENx Tech, Stream Ad Free Music via App Support, Magnetic Buds, Bluetooth Neckband, Wireless with Mic in Ear Earphones (Active-Black)',
    'JBL Wireless On-Ear Headphones',
    'Apple iPhone 13 Pink',
    'Set of 3 Premium Posters (Anime, Harry Potter & Rock Band)',
    'Apple MacBook Air M4 (Sky Blue)',
    'Lifelong 55 LTR Travel Backpack Rucksack Bags For Men & Women-Trekking Bag With Laptop Compartment For Travel, Hiking, Camping & Trekking-Rucksack Bag Accessories For Outdoor Travel, Orange',
    'RENESMEE Orthotic Arch Support Shoe Insoles, Children Pu Cushioning Inserts, Shock Absorption Velvet Surfaces Deep Heel Cup Inner Sole for Flat Feet, Feet Heel Pain Relief (43-45 EU MEN)'
]

for o in db.query(Order).all():
    if o.product_name not in custom_names and o.user_role == 'seller':
        o.user_role = 'other'

for l in db.query(Listing).all():
    if l.product_name in custom_names:
        o = db.query(Order).filter(Order.listing_id == l.id).first()
        if not o:
            new_order = Order(
                listing_id=l.id,
                product_name=l.product_name,
                image_url=l.image_url,
                grade=l.grade,
                original_price=l.suggested_price_inr,
                user_role='seller',
                events_json='[{"status": "pending", "label": "Analysis Pending", "note": "Received your submission. Waiting for a human agent to review your return.", "ts": "2026-06-15T10:00:00Z"}]'
            )
            db.add(new_order)

db.commit()
db.close()
print("Database updated successfully!")
