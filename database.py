from datetime import datetime, timedelta
from peewee import (
    Model, AutoField, CharField, IntegerField, FloatField, BooleanField,
    DateTimeField, DateField, TimeField, ForeignKeyField, TextField,
    Check
)
from playhouse.sqlite_ext import JSONField
from peewee import SqliteDatabase

db = SqliteDatabase('many_booking.db')

class Person(Model):
    name = CharField()
    age = IntegerField()

    class Meta:
        database = db # This model uses the "people.db" database.

db.create_tables([Person])

# ---------------- Base ----------------
class BaseModel(Model):
    created_at = DateTimeField(default=datetime.utcnow, index=True)
    updated_at = DateTimeField(default=datetime.utcnow)
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    class Meta:
        database = db

# ========== LIFF / LINE 連携 ==========
class LineChannel(BaseModel):
    """
    （任意）複数テナント運用や将来の拡張用。
    単一チャネル運用なら1行だけ保持しておけばOK。
    """
    id = AutoField()
    name = CharField()
    channel_id = CharField(unique=True)        # Messaging APIのChannel ID
    channel_secret = CharField()
    channel_access_token = TextField()         # 長期アクセストークン
    liff_id = CharField(null=True)             # LIFF ID（1つならここに）

class User(BaseModel):
    """
    LINEベースの会員。LINEのuserIdを必須ユニークキーに。
    - passwordは不要
    - emailは任意（予約連絡用に後で追加してもOK）
    """
    id = AutoField()
    line_user_id = CharField(unique=True, index=True)  # 例: Ua0123456789...
    line_display_name = CharField(null=True)
    line_picture_url = CharField(null=True)
    line_status_message = CharField(null=True)

    email = CharField(null=True, index=True)
    phone = CharField(null=True)
    birthday = DateField(null=True)
    gender = CharField(null=True)                        # 'male'|'female'|'other' など
    role = IntegerField(default=0, constraints=[Check('role in (0,1,2,3)')])  # 0=customer,1=staff,2=owner,3=admin
    is_active = BooleanField(default=True)

class UserChannelLink(BaseModel):
    """
    （重要）LINEの userId は**チャネルごとに異なる**可能性があるため、
    将来複数チャネル運用する場合に備えた対応。
    単一チャネルなら自動的に1行だけ作られる。
    """
    id = AutoField()
    user = ForeignKeyField(User, backref='channel_links', on_delete='CASCADE')
    channel = ForeignKeyField(LineChannel, backref='users', on_delete='CASCADE')
    channel_user_id = CharField(index=True)  # このチャネル内でのuserId
    class Meta:
        indexes = ((('channel', 'channel_user_id'), True),)  # unique

class LiffSession(BaseModel):
    """
    フロントのLIFFで取得したIDトークン検証後に発行するアプリ用セッション/JWTを保存（任意）。
    監査や多端末ログアウトに使える。
    """
    id = AutoField()
    user = ForeignKeyField(User, backref='sessions', on_delete='CASCADE')
    issued_at = DateTimeField(default=datetime.utcnow, index=True)
    expires_at = DateTimeField()
    device_info = CharField(null=True)     # UAなど
    revoked = BooleanField(default=False)

# ========== 店舗・営業時間 ==========
class Address(BaseModel):
    id = AutoField()
    postal_code = CharField(null=True)
    prefecture = CharField(null=True)
    city = CharField(null=True)
    line1 = CharField(null=True)
    line2 = CharField(null=True)

class Salon(BaseModel):
    id = AutoField()
    name = CharField(index=True)
    address = ForeignKeyField(Address, backref='salons', null=True, on_delete='SET NULL')
    phone = CharField(null=True)
    description = TextField(null=True)
    is_active = BooleanField(default=True)
    owner = ForeignKeyField(User, backref='owned_salons', null=True, on_delete='SET NULL')

class SalonStaff(BaseModel):
    id = AutoField()
    salon = ForeignKeyField(Salon, backref='staff', on_delete='CASCADE', index=True)
    user = ForeignKeyField(User, backref='staff_profiles', on_delete='CASCADE', unique=True)
    display_name = CharField(null=True)
    bio = TextField(null=True)
    is_active = BooleanField(default=True)

class SalonImage(BaseModel):
    id = AutoField()
    salon = ForeignKeyField(Salon, backref='images', on_delete='CASCADE', index=True)
    url = CharField()
    alt = CharField(null=True)
    sort_order = IntegerField(default=0)

class WorkingHour(BaseModel):
    id = AutoField()
    salon = ForeignKeyField(Salon, backref='working_hours', on_delete='CASCADE', index=True)
    weekday = IntegerField(constraints=[Check('weekday BETWEEN 0 AND 6')])
    start = TimeField()
    end = TimeField()
    is_closed = BooleanField(default=False)

class BlackoutDate(BaseModel):
    id = AutoField()
    salon = ForeignKeyField(Salon, backref='blackouts', on_delete='CASCADE', index=True)
    date = DateField(index=True)
    start = TimeField(null=True)
    end = TimeField(null=True)
    reason = CharField(null=True)

# ========== メニュー ==========
class Service(BaseModel):
    id = AutoField()
    salon = ForeignKeyField(Salon, backref='services', on_delete='CASCADE', index=True)
    name = CharField(index=True)
    description = TextField(null=True)
    duration_min = IntegerField(constraints=[Check('duration_min > 0')])
    price_jpy = IntegerField(constraints=[Check('price_jpy >= 0')])
    is_active = BooleanField(default=True)
    category = CharField(null=True)  # 'cut'|'color'|'脱毛' etc.

# ========== 予約 ==========
class Reservation(BaseModel):
    """
    status: 0=pending,1=confirmed,2=completed,3=canceled,4=no_show
    payment_status: 0=unpaid,1=paid,2=refunded
    """
    id = AutoField()
    user = ForeignKeyField(User, backref='reservations', on_delete='CASCADE', index=True)
    salon = ForeignKeyField(Salon, backref='reservations', on_delete='CASCADE', index=True)
    service = ForeignKeyField(Service, backref='reservations', on_delete='RESTRICT')
    staff = ForeignKeyField(SalonStaff, backref='reservations', null=True, on_delete='SET NULL')
    start_at = DateTimeField(index=True)
    end_at = DateTimeField(index=True)
    status = IntegerField(default=1, constraints=[Check('status in (0,1,2,3,4)')])
    payment_status = IntegerField(default=0, constraints=[Check('payment_status in (0,1,2)')])
    amount_jpy = IntegerField(null=True)      # クーポン適用後の最終金額
    note = TextField(null=True)
    class Meta:
        indexes = ((( 'staff','start_at','end_at'), True),)  # 同スタッフの重複予約防止

class ReservationChangeLog(BaseModel):
    id = AutoField()
    reservation = ForeignKeyField(Reservation, backref='logs', on_delete='CASCADE', index=True)
    actor = ForeignKeyField(User, backref='reservation_actions', null=True, on_delete='SET NULL')
    action = CharField()  # 'create'|'confirm'|'cancel'|'reschedule' etc.
    detail = TextField(null=True)

# ========== クーポン ==========
class Coupon(BaseModel):
    id = AutoField()
    code = CharField(unique=True, index=True)
    name = CharField()
    description = TextField(null=True)
    type = CharField(constraints=[Check("type in ('percent','amount')")])  # 値引種別
    value = FloatField(constraints=[Check('value >= 0')])
    scope = CharField(default='global', constraints=[Check("scope in ('global','salon','service')")])
    salon = ForeignKeyField(Salon, null=True, backref='coupons', on_delete='CASCADE')
    service = ForeignKeyField(Service, null=True, backref='coupons', on_delete='CASCADE')
    use_limit = IntegerField(null=True)         # 例: 1 = 初回限定
    starts_at = DateTimeField(null=True)
    ends_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)

class CouponRedemption(BaseModel):
    id = AutoField()
    coupon = ForeignKeyField(Coupon, backref='redemptions', on_delete='CASCADE', index=True)
    user = ForeignKeyField(User, backref='coupon_uses', on_delete='CASCADE', index=True)
    reservation = ForeignKeyField(Reservation, backref='coupon_uses', on_delete='CASCADE', unique=True)
    used_at = DateTimeField(default=datetime.utcnow)
    class Meta:
        indexes = ((( 'coupon','user'), False),)

# ========== 通知 / お知らせ ==========
class Notification(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='notifications', null=True, on_delete='CASCADE', index=True)
    salon = ForeignKeyField(Salon, backref='notifications', null=True, on_delete='CASCADE', index=True)
    title = CharField()
    body = TextField(null=True)
    type = CharField(default='system', constraints=[Check("type in ('campaign','reminder','system')")])
    is_read = BooleanField(default=False)
    delivered_at = DateTimeField(default=datetime.utcnow)

# ========== 口コミ ==========
class Review(BaseModel):
    id = AutoField()
    reservation = ForeignKeyField(Reservation, backref='review', on_delete='CASCADE', unique=True)
    salon = ForeignKeyField(Salon, backref='reviews', on_delete='CASCADE', index=True)
    user = ForeignKeyField(User, backref='reviews', on_delete='CASCADE', index=True)
    rating = IntegerField(constraints=[Check('rating BETWEEN 1 AND 5')], index=True)
    comment = TextField(null=True)

# ========== 検索キーワード ==========
class SearchKeyword(BaseModel):
    id = AutoField()
    keyword = CharField(unique=True, index=True)
    count = IntegerField(default=0)
    meta = JSONField(null=True)

# 初期化
def create_tables():
    with db:
        db.create_tables([
            LineChannel, User, UserChannelLink, LiffSession,
            Address, Salon, SalonStaff, SalonImage,
            WorkingHour, BlackoutDate, Service,
            Reservation, ReservationChangeLog,
            Coupon, CouponRedemption,
            Notification, Review, SearchKeyword
        ])

create_tables()