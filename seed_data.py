# seed_data.py
from datetime import datetime, timedelta, time, date
import random
from peewee import fn
from database import (
    db, create_tables,
    LineChannel, User, UserChannelLink, LiffSession,
    Address, Salon, SalonStaff, SalonImage,
    WorkingHour, BlackoutDate, Service,
    Reservation, ReservationChangeLog,
    Coupon, CouponRedemption,
    Notification, Review, SearchKeyword
)

random.seed(42)

def reset_and_create_tables():
    with db:
        db.drop_tables([
            LineChannel, User, UserChannelLink, LiffSession,
            Address, Salon, SalonStaff, SalonImage,
            WorkingHour, BlackoutDate, Service,
            Reservation, ReservationChangeLog,
            Coupon, CouponRedemption,
            Notification, Review, SearchKeyword
        ], safe=True)
    create_tables()

def seed_line_channels():
    channels = []
    for i in range(1, 3):  # 2チャネル
        ch = LineChannel.create(
            name=f"MainChannel{i}",
            channel_id=f"2000{i}",
            channel_secret=f"secret_{i}",
            channel_access_token=f"access_token_{i}",
            liff_id=f"liff_id_{i}"
        )
        channels.append(ch)
    return channels

def seed_users(channels):
    users = []
    # 顧客 8名
    for i in range(1, 9):
        u = User.create(
            line_user_id=f"U_customer_{i:02d}",
            line_display_name=f"顧客{i}",
            line_picture_url=f"https://example.com/p{i}.png",
            email=f"customer{i}@example.com",
            phone=f"090-0000-{1000+i}",
            role=0,  # customer
            is_active=True
        )
        users.append(u)
        UserChannelLink.create(user=u, channel=channels[0], channel_user_id=u.line_user_id)

    # スタッフ 4名（のちほどSalonStaffに紐付け）
    staff_users = []
    for i in range(1, 5):
        su = User.create(
            line_user_id=f"U_staff_{i:02d}",
            line_display_name=f"スタッフ{i}",
            line_picture_url=f"https://example.com/s{i}.png",
            email=f"staff{i}@example.com",
            phone=f"080-1111-{2000+i}",
            role=1,  # staff
            is_active=True
        )
        staff_users.append(su)
        UserChannelLink.create(user=su, channel=channels[0], channel_user_id=su.line_user_id)

    # オーナー 2名
    owners = []
    for i in range(1, 3):
        ow = User.create(
            line_user_id=f"U_owner_{i:02d}",
            line_display_name=f"オーナー{i}",
            email=f"owner{i}@example.com",
            role=2,  # owner
            is_active=True
        )
        owners.append(ow)
        UserChannelLink.create(user=ow, channel=channels[0], channel_user_id=ow.line_user_id)

    # 管理者 1名
    admin = User.create(
        line_user_id="U_admin_01",
        line_display_name="管理者",
        email="admin@example.com",
        role=3,
        is_active=True
    )
    UserChannelLink.create(user=admin, channel=channels[0], channel_user_id=admin.line_user_id)

    return users, staff_users, owners, admin

def seed_addresses():
    rows = []
    candidates = [
        ("020-0001", "岩手県", "盛岡市", "本町1-1-1", "第一ビル3F"),
        ("020-0002", "岩手県", "盛岡市", "中央通2-2-2", "第二ビル2F"),
        ("020-0003", "岩手県", "盛岡市", "青山3-3-3", "コーポA-101"),
        ("020-0004", "岩手県", "盛岡市", "南大通4-4-4", None),
        ("020-0005", "岩手県", "盛岡市", "肴町5-5-5", "サカナビル5F"),
        ("020-0006", "岩手県", "盛岡市", "菜園6-6-6", "菜園タワー8F"),
        ("020-0007", "岩手県", "盛岡市", "上田7-7-7", None),
        ("020-0008", "岩手県", "盛岡市", "緑が丘8-8-8", "緑マンション201"),
        ("020-0009", "岩手県", "盛岡市", "松尾町9-9-9", None),
        ("020-0010", "岩手県", "盛岡市", "前九年10-10-10", "メゾン前九年101"),
    ]
    for pc, pref, city, l1, l2 in candidates:
        rows.append(Address.create(
            postal_code=pc, prefecture=pref, city=city, line1=l1, line2=l2
        ))
    return rows

def seed_salons(addresses, owners):
    salons = []
    for i in range(1, 4):  # 3店舗
        s = Salon.create(
            name=f"JoASalon {i}",
            address=addresses[i],
            phone=f"019-600-00{i}{i}",
            description=f"JoASalon {i} の説明テキストです。",
            owner=owners[(i-1) % len(owners)],
            is_active=True
        )
        salons.append(s)
    return salons

def seed_salon_staff(salons, staff_users):
    # 4名のスタッフを2〜3店舗に分散（Userはunique制約あり）
    staff = []
    mapping = [
        (salons[0], staff_users[0]),
        (salons[0], staff_users[1]),
        (salons[1], staff_users[2]),
        (salons[2], staff_users[3]),
    ]
    for salon, su in mapping:
        staff.append(SalonStaff.create(
            salon=salon,
            user=su,
            display_name=su.line_display_name,
            bio=f"{su.line_display_name}のプロフィールです。",
            is_active=True
        ))
    return staff

def seed_salon_images(salons):
    imgs = []
    for i, salon in enumerate(salons, start=1):
        for j in range(1, 3):  # 各店舗2枚 → 6件
            imgs.append(SalonImage.create(
                salon=salon,
                url=f"https://example.com/salon{salon.id}_img{j}.jpg".replace(" ", ""),
                alt=f"Salon {salon.id} Image {j}",
                sort_order=j-1
            ))
    # さらに4枚追加して計10枚程度に調整
    for k in range(4):
        imgs.append(SalonImage.create(
            salon=salons[k % len(salons)],
            url=f"https://example.com/extra_{k}.jpg",
            alt=f"Extra {k}",
            sort_order=10+k
        ))
    return imgs

def seed_working_hours(salons):
    whs = []
    # Salon1: 月〜日 10:00-19:00（7件）
    for w in range(7):
        whs.append(WorkingHour.create(
            salon=salons[0], weekday=w, start=time(10,0), end=time(19,0), is_closed=False
        ))
    # Salon2: 月〜金のみ（5件）
    for w in range(5):
        whs.append(WorkingHour.create(
            salon=salons[1], weekday=w, start=time(9,30), end=time(18,30), is_closed=False
        ))
    # Salon3: 火曜定休（6件＋1件定休）
    for w in range(7):
        closed = (w == 1)  # 火曜
        if closed:
            whs.append(WorkingHour.create(
                salon=salons[2], weekday=w, start=time(0,0), end=time(0,0), is_closed=True
            ))
        else:
            whs.append(WorkingHour.create(
                salon=salons[2], weekday=w, start=time(11,0), end=time(20,0), is_closed=False
            ))
    # 件数は20件超えますが、要件（10前後）よりやや多めでも運用上OK
    return whs

def seed_blackouts(salons):
    today = date.today()
    rows = []
    rows.append(BlackoutDate.create(salon=salons[0], date=today + timedelta(days=7), reason="機器メンテナンス"))
    rows.append(BlackoutDate.create(salon=salons[1], date=today + timedelta(days=14), start=time(14,0), end=time(18,0), reason="社内研修"))
    rows.append(BlackoutDate.create(salon=salons[2], date=today + timedelta(days=21), reason="臨時休業"))
    return rows

def seed_services(salons):
    categories = ["カット", "カラー", "パーマ", "トリートメント", "ヘッドスパ", "脱毛", "鍼灸", "整体", "まつエク", "ネイル"]
    svcs = []
    for i in range(10):
        salon = salons[i % len(salons)]
        duration = random.choice([30, 45, 60, 90])
        price = random.choice([3000, 4500, 6000, 8000, 10000])
        svcs.append(Service.create(
            salon=salon,
            name=categories[i],
            description=f"{categories[i]}の説明です。",
            duration_min=duration,
            price_jpy=price,
            category=categories[i],
            is_active=True
        ))
    return svcs

def seed_coupons(salons, services):
    coupons = []
    # 5件：%/額・スコープ混在
    coupons.append(Coupon.create(code="WELCOME20", name="新規20%OFF", type="percent", value=20.0, scope="global", use_limit=1, is_active=True))
    coupons.append(Coupon.create(code="WEEKDAY500", name="平日500円OFF", type="amount", value=500, scope="global", is_active=True))
    coupons.append(Coupon.create(code="SALON1_10", name="サロン1限定10%OFF", type="percent", value=10.0, scope="salon", salon=salons[0], is_active=True))
    coupons.append(Coupon.create(code="COLOR1000", name="カラー1000円OFF", type="amount", value=1000, scope="service", service=services[1], is_active=True))
    coupons.append(Coupon.create(code="HEADSPA15", name="ヘッドスパ15%OFF", type="percent", value=15.0, scope="service", service=services[4], is_active=True))
    # さらに5件追加して計10件前後
    for i in range(5):
        coupons.append(Coupon.create(
            code=f"PROMO{i+1}",
            name=f"プロモ{i+1}",
            type=random.choice(["percent","amount"]),
            value=random.choice([5.0, 8.0, 1000, 1500]),
            scope=random.choice(["global","salon","service"]),
            salon=random.choice([None, salons[0], salons[1], salons[2]]),
            service=random.choice([None] + services[:3]),
            use_limit=random.choice([None, 1, 2]),
            is_active=True
        ))
    return coupons

def seed_notifications(users, salons):
    notes = []
    titles = ["キャンペーン", "予約確認", "誕生日クーポン", "メンテ通知", "新メニュー追加", "混雑注意", "レビュー依頼", "システムお知らせ", "アンケート"]
    for i, t in enumerate(titles):
        u = users[i % len(users)]
        notes.append(Notification.create(
            user=u,
            salon=random.choice([None] + salons),
            title=t,
            body=f"{t} の本文です。",
            type=random.choice(["campaign","reminder","system"]),
            is_read=(i % 3 == 0)
        ))
    return notes

def seed_search_keywords():
    kws = []
    words = ["カット", "カラー", "ヘッドスパ", "整体", "脱毛", "盛岡", "学割", "早朝", "メンズ", "レディース"]
    for w in words:
        kws.append(SearchKeyword.create(keyword=w, count=random.randint(1, 50), meta={"type": "service"}))
    return kws

def seed_reservations(users, salons, services, staff):
    # 予約10件：開始時刻の重複を避ける
    base = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    reservations = []
    for i in range(10):
        user = users[i % len(users)]
        svc = services[i % len(services)]
        salon = svc.salon
        staff_candidate = [st for st in staff if st.salon_id == salon.id]
        assigned_staff = random.choice(staff_candidate) if staff_candidate else None

        start_at = base + timedelta(days=i, hours=10 + (i % 5))
        end_at = start_at + timedelta(minutes=svc.duration_min)

        r = Reservation.create(
            user=user,
            salon=salon,
            service=svc,
            staff=assigned_staff,
            start_at=start_at,
            end_at=end_at,
            status=random.choice([1,1,1,0,2]),  # 確定多め
            payment_status=random.choice([0,1]),
            amount_jpy=svc.price_jpy - random.choice([0, 500, 1000]),
            note=None
        )
        reservations.append(r)

        ReservationChangeLog.create(
            reservation=r, actor=user, action="create", detail="初回作成"
        )
        if r.status == 3:  # キャンセルされていればログ
            ReservationChangeLog.create(
                reservation=r, actor=user, action="cancel", detail="ユーザー都合"
            )
    return reservations

def seed_coupon_redemptions(reservations, coupons, users):
    red = []
    # 予約の半分くらいにクーポンを紐づけ
    targets = reservations[:len(reservations)//2]
    for i, r in enumerate(targets):
        c = coupons[(i+1) % len(coupons)]
        red.append(CouponRedemption.create(
            coupon=c, user=r.user, reservation=r
        ))
    return red

def seed_reviews(reservations):
    revs = []
    # 完了した予約に対してレビュー（8件前後）
    completed = [r for r in reservations if r.status in (2,)]
    if not completed:
        completed = reservations[2:10:1]  # 代替
    for i, r in enumerate(completed[:8]):
        revs.append(Review.create(
            reservation=r,
            salon=r.salon,
            user=r.user,
            rating=random.choice([4,5,5,3]),
            comment=f"{r.service.name} とても良かったです（{i}）"
        ))
    return revs

def seed_sessions(users):
    sess = []
    now = datetime.utcnow()
    for u in users[:5]:  # 5ユーザー分
        sess.append(LiffSession.create(
            user=u,
            issued_at=now,
            expires_at=now + timedelta(days=7),
            device_info="iOS Safari",
            revoked=False
        ))
    return sess

def main():
    reset_and_create_tables()

    with db.atomic():
        channels = seed_line_channels()
        customers, staff_users, owners, admin = seed_users(channels)
        addresses = seed_addresses()
        salons = seed_salons(addresses, owners)
        staff = seed_salon_staff(salons, staff_users)
        images = seed_salon_images(salons)
        whs = seed_working_hours(salons)
        blackouts = seed_blackouts(salons)
        services = seed_services(salons)
        coupons = seed_coupons(salons, services)
        notifications = seed_notifications(customers, salons)
        keywords = seed_search_keywords()
        reservations = seed_reservations(customers, salons, services, staff)
        redemptions = seed_coupon_redemptions(reservations, coupons, customers)
        reviews = seed_reviews(reservations)
        sessions = seed_sessions(customers)

    print("=== Seed Completed ===")
    print("Users:", User.select().count())
    print("Salons:", Salon.select().count())
    print("Services:", Service.select().count())
    print("Reservations:", Reservation.select().count())
    print("Coupons:", Coupon.select().count())
    print("Reviews:", Review.select().count())

if __name__ == "__main__":
    main()
