# URL Shortener - Week 1 (Python + Flask)

هذه الملفات تنفذ متطلبات **Week 1** من مشروع "DevOps Engineer" (Web service, SQLite, Docker).  
(تابع المواصفات في ملف المشروع الذي أرسلته.) 

## محتويات المشروع
- `app.py` : تطبيق Flask يحتوي على نقطتي الوصول:
  - `POST /shorten` لقبول رابط طويل وإرجاع كود مختصر ورابط قصير.
  - `GET /<short_code>` لإعادة التوجيه إلى الرابط الطويل.
- `templates/index.html` : واجهة بسيطة للتجربة.
- `static/style.css` : أنماط الواجهة.
- `requirements.txt` : تبعيات المشروع.
- `Dockerfile` و `docker-compose.yml` : لتشغيل الحاوية محليًا.
- `data/` : مجلد مخصص لملف قاعدة البيانات (سينشأ تلقائيًا).

## تشغيل محلي (بدون دوكر)
1. أنشئ virtualenv:
   ```bash
   python -m venv env
   source env/bin/activate   # على Windows: env\Scripts\activate
   ```
2. ثبّت التبعيات:
   ```bash
   pip install -r requirements.txt
   ```
3. شغّل التطبيق:
   ```bash
   python app.py
   ```
4. افتح المتصفح على: `http://localhost:5000`

## تشغيل باستخدام Docker (مستحسن)
- بناء الصورة:
  ```bash
  docker build -t url-shortener:week1 .
  ```
- تشغيل:
  ```bash
  docker run -p 5000:5000 -v $(pwd)/data:/data url-shortener:week1
  ```
- أو باستخدام Docker Compose:
  ```bash
  docker-compose up --build
  ```

## أختبار API عبر curl
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://www.example.com"}' http://localhost:5000/shorten
```
وفتح الرابط المختصر في المتصفح سيعيد التوجيه إلى الرابط الأصلي.

## رفع المشروع على GitHub - أوامر خطوة بخطوة
1. تهيئة مستودع محلي:
   ```bash
   git init
   git add .
   git commit -m "Week1: URL shortener (Flask + SQLite)"
   git branch -M main
   ```
2. (خيار أ) عبر موقع GitHub:
   - ادخل إلى github.com -> New repository -> املأ الاسم (مثلا `url-shortener-week1`) -> Create.
   - ثم ربط المستودع المحلي:
     ```bash
     git remote add origin https://github.com/<your-username>/url-shortener-week1.git
     git push -u origin main
     ```
3. (خيار ب) عبر GitHub CLI:
   ```bash
   gh auth login   # إذا لم تقم بتسجيل الدخول
   gh repo create url-shortener-week1 --public --source=. --remote=origin --push
   ```
4. بعد الرفع، ستشاهد الملفات على صفحة المستودع في GitHub.

## ملاحظات
- قاعدة البيانات SQLite مخزنة في `data/url_shortener.db` (مجلد يتم ربطه عند تشغيل Docker Compose).
- هذا الأسبوع يركز على وظيفة التطبيق والتعبئة (containerization). أدوات المراقبة (Prometheus/Grafana) ستتم إضافتها في الأسابيع التالية وفقًا لمخطط المشروع.

--- 
تمت كتابة هذه الحزمة لتتناسب مع Week 1 من مواصفات المشروع.
