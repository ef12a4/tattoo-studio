# React Native Mobile App

Dövmeci Stüdyosu için React Native mobil uygulama şablonu.

## 📱 Özellikler

- **Sanatçı Profili:** Sanatçı bilgileri ve portfolyo
- **Online Randevu:** Mobil randevu sistemi
- **Galeri:** Fotoğraf galeri ve 3D önizleme
- **Bildirimler:** Push bildirimler
- **Ödeme:** Mobil ödeme entegrasyonu
- **Harita:** Stüdyo konumu ve navigasyon

## 🚀 Kurulum

```bash
# Node.js ve React Native CLI kurulumu
npm install -g react-native-cli

# Proje klonlama
git clone <repository-url>
cd tattoo-studio-mobile

# Bağımlılıklar
npm install

# iOS
cd ios && pod install

# Çalıştırma
npm run android  # Android için
npm run ios     # iOS için
```

## 📂 Proje Yapısı

```
src/
├── components/          # UI bileşenleri
├── screens/            # Ekranlar
├── navigation/         # Navigasyon
├── services/           # API servisleri
├── utils/              # Yardımcı fonksiyonlar
├── assets/             # Resim ve fontlar
└── styles/             # Stil dosyaları
```

## 🔗 API Entegrasyonu

```javascript
// API konfigürasyonu
const API_BASE_URL = 'http://localhost:5000/api/v1';

// API anahtarı
const API_KEY = 'tattoo_studio_api_key_2024';
```

## 📱 Ekranlar

- **Home:** Ana sayfa ve sanatçılar
- **ArtistDetail:** Sanatçı detayı
- **Booking:** Randevu oluşturma
- **Gallery:** Galeri
- **Profile:** Kullanıcı profili
- **Settings:** Ayarlar

## 🎨 UI/UX

- Material Design
- Responsive tasarım
- Dark/Light tema
- Animasyonlar ve geçişler

## 🔔 Bildirimler

- Randevu hatırlatmaları
- Promosyon bildirimleri
- Sanatçı güncellemeleri

## 💳 Ödeme

- Stripe entegrasyonu
- Iyzico desteği
- Apple Pay / Google Pay

## 🗺️ Harita

- Google Maps entegrasyonu
- Stüdyo konumu
- Navigasyon

## 📊 Analytics

- Kullanıcı takibi
- Performans metrikleri
- Crash raporlama
