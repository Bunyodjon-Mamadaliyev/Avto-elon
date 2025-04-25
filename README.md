# 🚘 Avto E'lon Platformasi - RESTful API

> 🛠️ Zamonaviy avtomobil e'lonlar platformasi uchun RESTful API

---

## 📖 Loyiha Tavsifi

Ushbu loyiha orqali avtomobil sotuvchilari va xaridorlari:
- 🚙 E'lon joylashtirishi,
- 🔍 Avtomobillarni izlab topishi,
- 🏷️ Narxlarni solishtirishi,
- 💬 Bir-biri bilan muloqot qilishi,
- ⭐ Sharhlar va reytinglar qoldirishi mumkin.

---

## 🧩 Asosiy Funksiyalar

- ✅ Foydalanuvchi autentifikatsiyasi (oddiy yoki diler)
- 🚗 Avtomobil qo'shish, tahrirlash va o‘chirish
- 🔎 Avtomobil va dilerlarni qidirish va filtrlash
- 🖼️ E’lon uchun rasm yuklash
- 🧾 Narxlar tarixini ko’rish
- 🧠 Narx tahlil va baholash tizimi
- ✉️ Xabar almashish va suhbatlar
- 🗂️ Saqlangan va taqqoslangan e'lonlar
- 📑 API hujjatlari (Swagger/OpenAPI)

---

## ⚙️ Texnologiyalar

| Texnologiya | Izoh |
|------------|------|
| Django | Backend web freymvork |
| Django REST Framework | RESTful API yaratish |
| SimpleJWT | Token asosida autentifikatsiya |
| PostgreSQL | Ma'lumotlar ombori |
| drf-yasg | Swagger/OpenAPI hujjatlari |

---

## 🔐 API Endpointlar (Qisqacha)

### 🔑 Autentifikatsiya
- `POST /api/auth/register/` – Ro‘yxatdan o‘tish
- `POST /api/auth/login/` – Login + token olish
- `POST /api/auth/refresh/` – Tokenni yangilash
- `POST /api/auth/logout/` – Logout
- `GET /api/auth/user/` – Joriy foydalanuvchi ma’lumoti

### 🏪 Dilerlar
- `GET/POST /api/dealers/` – Diler ro‘yxati yoki yangi qo‘shish
- `GET/PUT/DELETE /api/dealers/{id}/` – Tafsilotlar, tahrirlash yoki o‘chirish
- `GET/POST /api/dealers/{id}/reviews/` – Diler sharhlari

### 🚘 Avtomobillar
- `GET/POST /api/cars/` – Avtomobillar ro‘yxati yoki yaratish
- `GET /api/makes/` – Avto markalar
- `GET /api/features/` – Xususiyatlar

### 📢 E’lonlar
- `GET/POST /api/listings/` – E’lonlar ro‘yxati yoki yaratish
- `GET /api/listings/{id}/price-history/` – Narx tarixini ko‘rish
- `POST /api/listings/{id}/images/` – Rasm yuklash

### 📬 Xabarlar
- `GET/POST /api/messages/` – Xabarlar
- `GET /api/messages/conversations/` – Suhbatlar ro‘yxati

### ⭐ Sharhlar & Reyting
- `GET/POST /api/reviews/` – Sharhlar
- `GET /api/reviews/users/{user_id}/` – Foydalanuvchi sharhlari

### 📊 Tahlil & Qidiruv
- `GET /api/analytics/price/` – Narx statistikasi
- `POST /api/analytics/price/estimate/` – Narx baholash
- `GET /api/search/listings/` – Keng qamrovli qidiruv

---

## 🛡️ Xavfsizlik

- Token asosidagi autentifikatsiya (JWT)
- Foydalanuvchi huquqlari va ruxsatlar
- CRUD operatsiyalarda egalik tekshiruvi

---

## 🧪 O'rnatish va Ishga tushirish

```bash
git clone https://github.com/Bunyodjon-Mamadaliyev/Avto-elon.git
cd Avto-elon
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```