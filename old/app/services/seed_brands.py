from app import create_app, db
from app.models import CanonBrand

BRAND_NAMES = [
"Ducky",
"Evoworks",
"Realforce",
"Keychron",
"WOBKEY",
"Leopold",
"Filco",
"Varmilo",
"Wooting",
"Ticktype",
"Vortex",
"HHKB",
"WLMOUSE",
"Chilkey",
"Tex",
"Neo",
"MK",
"Qwertykeys",
"LUMINKEY",
"Shortcut Studio",
"Womier",
"Nuxroskb",
"KBDFans",
"Obinslab",
"Meko",
"Shurikey",
"KBParadise",
"80Retros",
"Hexgears",
"Mistel",
"Meletrix",
"DOIO",
"Pulsar",
"Lemokey",
"ONEofZERO",
"MelGeek",
"Odin Gaming",
"Glorious PC",
"Endgame Gear",
"Binepad",
"Ace Pad Tech",
"IKBC",
"Matias",
"Keycool",
"KBtalking",
"Typone",
"Yunzii",
"Click Inc",
"Moon KBD",
"Akko",
"MonsGeek",
"Keebwerk",
"GDK Lab Keyboards",
"Lofree",
"NuPhy",
"Epomaker",
"Royal Kludge",
"AJAZZ",
"FL·ESPORTS",
"Dareu",
"Feker",
"CIDOO",
"Skyloong",
"MCHOSE",
"DrunkDeer",
"Razer",
"Corsair",
"SteelSeries",
"Logitech",
"ASUS ROG",
"HyperX",
"Mode Designs",
"CannonKeys",
"NovelKeys",
"Vertex",
"Geon",
"Owlab",
"TGR",
"Matrix Lab",
"Percent Studio",
"SingaKBD"
]

def seed_brands():
    app = create_app()

    with app.app_context():
        added = 0

        for name in BRAND_NAMES:
            exists = CanonBrand.query.filter_by(name=name).first()
            if exists:
                continue

            db.session.add(CanonBrand(name=name))
            added += 1

        db.session.commit()
        print(f"Inserted {added} brand names.")

if __name__ == "__main__":
    seed_brands()