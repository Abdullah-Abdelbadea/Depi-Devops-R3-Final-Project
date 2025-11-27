#  URL Shortener – Week 1 Progress

During Week 1 of the Depi DevOps R3 Final Project, the following core infrastructure was completed:

###  Implemented by me:
- app.py Flask backend API for shortening and redirecting URLs
- index.html frontend interface for submitting URLs
- Dockerfile containerization setup for the Flask service
- First web service configured in docker-compose.yml
- Docker image successfully built and pushed to DockerHub

---

## 🧠Tech Stack Used
| Component | Technology |
|--------|------------|
| Backend API | Flask (Python 3.11) |
| Database | SQLite |
| Containerization | Docker + Gunicorn |
| Deployment Orchestration | Docker Compose |
| Image Registry | DockerHub |

---

## 📦 Project Structure (Week 1)

```
.
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── /data
└── /templates/index.html
```

---

## ▶️ How to Run the Web Service (Local Setup)

1. Clone the repository:
```
git clone git@github.com:Abdullah-Abdelbadea/Depi-Devops-R3-Final-Project.git
cd Depi-Devops-R3-Final-Project
```

2. Build the Docker image:
```
docker build -t url-shortener:web .
```

3. Run the container:
```
docker run -p 5000:5000 -v ./data:/data -e DB_PATH=/data/url_shortener.db url-shortener:web
```

4. Run using Docker Compose:
```
docker-compose up --build
```

The app will run on:
```
http://localhost:5000
```

---

## 🏷️ Push Image to DockerHub

1. Login:
```
docker login
```

2. Tag the image:
```
docker tag url-shortener:web hassankaoud/url-shortener:latest
```

3. Push:
```
docker push hassankaoud/url-shortener:latest
```

---

## ⭐ Summary of Week 1
Week 1 focused on building the main Flask service, containerizing it with Docker, orchestrating it with Docker Compose, and successfully pushing the Docker image to DockerHub.

---



#  URL Shortener – Week 2 Progress
**Author:** Abdullah Mohamed Abdelbadea  
**Team Role:** Backend (URL Shortener Service + Prometheus Instrumentation)  

---

## Overview
This component of the project implements a **Flask-based URL Shortener** that stores URLs in a SQLite database and exposes an endpoint for Prometheus to scrape runtime metrics. The service provides:

- URL shortening (`POST /shorten`)
- Redirection via short codes (`GET /<short_code>`)
- Exported Prometheus metrics (`GET /metrics`)
- SQLite persistent storage
- Dockerized deployment with Prometheus integration

This README documents only **my part** of the system.

---

## Features
- Generate unique short codes using secure random generation.
- Store URLs in a SQLite database with auto-creation on startup.
- Automatic redirection using the generated short code.
- Integrated Prometheus monitoring.
- Fully containerized using Docker Compose.

---

## Application Endpoints

### `POST /shorten`
Shortens a given long URL.

**Request (JSON):**
```json
{
  "url": "https://example.com/long/path"
}
```

**Response:**
```json
{
  "short_code": "Ab12C3",
  "short_url": "http://localhost:5000/Ab12C3",
  "long_url": "https://example.com/long/path"
}
```

### `GET /<short_code>`
Redirects to the original long URL  
- Returns **302 redirect** if found  
- Returns **404 page** if the code does not exist  

### `GET /metrics`
Exposes all Prometheus metrics for scraping.

---

## Prometheus Metrics Included
The application exports the following counters and histograms:

| Metric Name | Type | Description |
|-------------|------|-------------|
| `url_shortened_total` | Counter | Number of successfully shortened URLs |
| `url_redirects_total` | Counter | Successful redirect operations |
| `url_not_found_total` | Counter | Number of 404 lookups due to unknown short codes |
| `shorten_request_latency_seconds` | Histogram | Latency for `/shorten` requests |
| `redirect_request_latency_seconds` | Histogram | Latency for redirect operations |

These metrics are exposed automatically at the `/metrics` endpoint.

---

## Docker Compose Setup
Below is the part relevant to my service:

### `docker-compose.yml`
```yaml
prometheus:
  image: prom/prometheus:latest
  container_name: prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
    - ./prometheus/alerts.rules.yml:/etc/prometheus/alerts.rules.yml:ro
  command:
    - '--config.file=/etc/prometheus/prometheus.yml'
  ports:
    - "9091:9090"
  depends_on:
    - web
```

---

## Prometheus Configuration
### `prometheus.yml`
```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'flask_app'
    static_configs:
      - targets: ['web:5000']
```

Prometheus scrapes the Flask service every **5 seconds** via the Docker network.

---

## Database
- SQLite file path: `data/url_shortener.db`
- Automatically created if missing
- Table schema:
```sql
CREATE TABLE IF NOT EXISTS urls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  short_code TEXT UNIQUE,
  long_url TEXT NOT NULL,
  created_at INTEGER
);
```

---

## Running the Service

### Start using Docker Compose:
```bash
docker compose up --build -d
```

### Access:
- App Homepage → `http://localhost:5000/`
- Metrics → `http://localhost:5000/metrics`
- Prometheus → `http://localhost:9091/` (based on your mapping)

---

## Useful PromQL Queries

### URL Shortening Rate (per minute)
```
rate(url_shortened_total[1m])
```

### Redirects over the last hour
```
increase(url_redirects_total[1h])
```

### 95th Percentile Latency (5-minute window)
```
histogram_quantile(0.95, sum(rate(shorten_request_latency_seconds_bucket[5m])) by (le))
```

### 404 Ratio
```
increase(url_not_found_total[5m]) /
(increase(url_redirects_total[5m]) + increase(url_not_found_total[5m]))
```

---

## Notes & Troubleshooting
- Ensure the Flask service name is **`web`** in Docker Compose to match the Prometheus configuration.
- `/metrics` must be accessible from inside the Prometheus container.
- If the host port for Prometheus is changed, update the team documentation accordingly.
- Increase `SHORT_CODE_LEN` if collisions occur.

---

## ⭐ Summary of Week 2
This part of the system provides a fully functional **URL Shortening API** instrumented with **Prometheus metrics**, running inside Docker, and ready for monitoring dashboards or alerting systems.


