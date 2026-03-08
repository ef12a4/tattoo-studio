# 🆓 Free Hosting Deployment Guide

## 1. Railway (En Kolay)
**URL**: tattoo-studio.up.railway.app
**Limit**: 500 saat/ay ücretsiz

```bash
# 1. Railway CLI kurulum
npm install -g @railway/cli

# 2. Login
railway login

# 3. Proje oluştur
railway init

# 4. Deploy
railway up

# 5. Environment variables ekle
railway variables set SECRET_KEY=your_secret_key
railway variables set DATABASE_URL=sqlite:///tattoo_studio.db
```

## 2. Render (Popüler)
**URL**: tattoo-studio.onrender.com
**Limit**: 750 saat/ay ücretsiz

```bash
# 1. GitHub'a push et
git add .
git commit -m "Ready for Render deployment"
git push origin main

# 2. Render.com'a git
# 3. "New Web Service" seç
# 4. GitHub reposunu bağla
# 5. Build Command: pip install -r requirements.txt
# 6. Start Command: gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

## 3. Vercel (En Hızlı)
**URL**: tattoo-studio.vercel.app
**Limit**: Sınırsız (kullanım bazlı)

```bash
# 1. Vercel CLI kurulum
npm install -g vercel

# 2. Deploy
vercel

# 3. Environment variables ekle
vercel env add SECRET_KEY
vercel env add DATABASE_URL
```

## 4. Fly.io (Gelişmiş)
**URL**: tattoo-studio.fly.dev
**Limit**: 160 saat/ay ücretsiz

```bash
# 1. Fly CLI kurulum
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Deploy
fly launch
fly deploy
```

## 5. Glitch (Anında)
**URL**: random-words.glitch.me
**Limit**: Sınırsız (sleep modunda)

```bash
# 1. glitch.com'a git
# 2. "New Project" > "Import from GitHub"
# 3. Repoyu gir
# 4. Otomatik başlatılır
```

## 6. Replit (Basit)
**URL**: tattoo-studio.username.repl.co
**Limit**: Sınırsız (kullanım limitli)

```bash
# 1. replit.com'a git
# 2. "Import from GitHub"
# 3. Repoyu gir
# 4. Otomatik çalışır
```

## 7. PythonAnywhere (Klasik)
**URL**: username.pythonanywhere.com
**Limit**: Web app ücretsiz

```bash
# 1. pythonanywhere.com'a git
# 2. "Bash" konsol aç
# 3. Clone et:
git clone <your-repo-url>
cd tattoo-studio

# 4. Virtual environment oluştur
mkvirtualenv tattoo-studio
pip install -r requirements.txt

# 5. Web app oluştur
# 6. Path: /home/username/tattoo-studio/wsgi.py
# 7. Start command: gunicorn --bind 0.0.0.0:8000 wsgi:app
```

## 🏆 Tavsiyeler

### En İyi Free Hosting Seçimi:
1. **Yeni başlayanlar**: **Glitch** (anında, en kolay)
2. **Hızlı deploy**: **Vercel** (saniyeler içinde)
3. **Stabil**: **Render** (en güvenilir)
4. **Gelişmiş**: **Railway** (database destekli)

### Domain olmadan URL'ler:
- **Railway**: `tattoo-studio.up.railway.app`
- **Render**: `tattoo-studio.onrender.com`
- **Vercel**: `tattoo-studio.vercel.app`
- **Fly.io**: `tattoo-studio.fly.dev`
- **Glitch**: `tattoo-studio.glitch.me`
- **Replit**: `tattoo-studio.username.repl.co`

### Önemli Notlar:
- ✅ Tüm platformlar SSL sağlar
- ✅ HTTPS otomatik çalışır
- ✅ Environment variables desteklenir
- ⚠️ Free planlarda sleep mode olabilir
- ⚠️ Database limitleri olabilir
- ⚠️ Bandwidth limitleri var

### Hızlı Test İçin:
**Glitch** en hızlısı - 5 dakikada hazır!

### Production İçin:
**Render** veya **Railway** daha stabil.
