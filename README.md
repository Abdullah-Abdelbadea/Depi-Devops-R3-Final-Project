# URL Shortener - Week 1 (Python + Flask)

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open the browser at: `http://localhost:5000`

---

## Run with Docker (recommended)

Build the image:

```bash
docker build -t url-shortener:week1 .
```

Run the container:

```bash
docker run -p 5000:5000 -v $(pwd)/data:/data url-shortener:week1
```

Or using Docker Compose:

```bash
docker-compose up --build
```

---

## Test the API with curl

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://www.example.com"}' http://localhost:5000/shorten
```

Then open the short URL in your browser to be redirected to the original link.

---

## Push the Project to GitHub - Step by Step

Initialize a local repository:

```bash
git init
git add .
git commit -m "Week1: URL shortener (Flask + SQLite)"
git branch -M main
```

(Option A) via GitHub website:

Go to github.com -> New repository -> Set the name (e.g., `url-shortener-week1`) -> Create.

Link the local repo:

```bash
git remote add origin https://github.com/<your-username>/url-shortener-week1.git
git push -u origin main
```

(Option B) via GitHub CLI:

```bash
gh auth login   # if not logged in
gh repo create url-shortener-week1 --public --source=. --remote=origin --push
```

After pushing, you will see the files on your GitHub repository page.

---

## Notes

- The SQLite database is stored in `data/url_shortener.db` (the folder is mounted when running with Docker Compose).
- This week focuses on the core functionality and containerization. Monitoring tools (Prometheus/Grafana) will be added in the following weeks as per the project plan.
>>>>>>> week1







## Prometheus Alert Rules

A dedicated alert rules file (alerts.rules.yml) was added to automatically detect abnormal or unhealthy application behavior.
The implemented alerts include:

WebServiceDown – triggers when the Flask service stops responding.

TooManyFailedLookups – triggers when the number of 404 errors becomes abnormally high.

HighShortenLatency – alerts when the /shorten API becomes slow (95th percentile > 1 second).

HighRedirectLatency – alerts when redirect operations become slow.

NoRedirects – detects when the service is running but no redirect traffic is happening.

These rules allow early detection of issues like downtime, performance degradation, or bad user input trends.

## Alertmanager Integration (Telegram + Gmail)

Alertmanager is fully configured to deliver alerts using two notification channels:

Telegram Bot — Instant alerts are sent to a specified chat using a Telegram bot.

Gmail (SMTP) — Alerts are also delivered via email using a secure Gmail App Password.

Alertmanager routes every alert from Prometheus to both channels, ensuring high reliability and multiple forms of notification.

## Prometheus Configuration

The main prometheus.yml file was updated to:

Load external alert rules from alerts.rules.yml

Define Alertmanager as the alert delivery system

Scrape the Flask web service metrics endpoint

Use a 5-second scrape interval for better resolution

>>>>week 5
