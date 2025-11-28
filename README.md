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

---------------------------------------------------------------------------

#  URL Shortener – Week 3 Progress
**Author:** mohamed adel mohamed kaoud  
**Team Role:** (Advanced Visualization with Grafana)  
---
<div dir="rtl">

# Grafana Monitoring Project

This project sets up **Grafana** using Docker with full **Provisioning Automation**, including:

* Automatic Prometheus datasource creation
* Automatic dashboard import using a JSON file
* Support for fixed UID to keep dashboards persistent across redeployments

---

## Overview

The project uses Grafana’s provisioning system to automatically configure everything at startup without needing to import dashboards manually from the UI.
All datasource and dashboard configurations are stored inside the `provisioning` directory.

---

## Features

### 1. Automated Prometheus Datasource Provisioning

A configuration file is placed inside:

```
provisioning/datasources/datasource.yaml
```

This file automatically:

* Creates a Prometheus datasource when Grafana starts
* Sets `http://prometheus:9091` as the datasource URL
* Marks it as the default datasource
* Prevents manual changes for stability

**Example (datasource.yaml):**

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
```

---

### 2. Automated Dashboard Import (Provisioning)

A dashboard provider configuration is stored in:

```
provisioning/dashboards/dashboard.yaml
```

This file:

* Automatically imports all dashboards inside a specified folder
* Assigns them to a custom Grafana folder
* Reloads dashboards if the files change
* Works with fixed UIDs

**Example (dashboard.yaml):**

```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'Imported Dashboards'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards/json
```

---

### 3. Automatically Imported Dashboard JSON (with fixed UID)

Dashboard files are placed inside:

```
provisioning/dashboards/json/
```

Example dashboard JSON (`my-dashboard.json`):

```json
{
  "uid": "my-dashboard-001",
  "title": "System Monitoring Dashboard",
  "schemaVersion": 36,
  "version": 1,
  "panels": [
    {
      "id": 1,
      "type": "graph",
      "title": "CPU Usage",
      "datasource": "Prometheus",
      "targets": [
        { "expr": "node_cpu_seconds_total" }
      ]
    }
  ]
}
```

The fixed UID ensures:

* No duplicate dashboards on restart
* Same dashboard can be updated automatically
* Stable API references

---

## Docker Compose Setup

```yaml
services:
  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - ./provisioning:/etc/grafana/provisioning
```

This automatically loads:

* Datasources
* Dashboards
* UID configuration

---

## What This Project Provides

* Fully automated Grafana setup
* Zero manual importing required
* Preconfigured Prometheus datasource
* Dashboard auto-loading with persistent UID
* Clean provisioning folder structure
* Production-ready configuration

---

-------------------------------------------------------------------------------------------------------

### URL Shortener – Week 4 Progress

### Monitoring & Alerting (Prometheus + Alertmanager)

## Overview

* During Week 4, I implemented the complete alerting pipeline for the project using:

* Prometheus alert rules

* Alertmanager with Telegram + Gmail notifications

* Updated Prometheus configuration

* A full monitoring → alerting workflow

This adds production-grade observability to the system built in Weeks 1–3.

## Features Added This Week
## 1. Prometheus Alert Rules

A full alert rules file (alerts.rules.yml) was created with conditions that automatically detect failures and performance issues.

| Alert Name               | Purpose                     | Trigger                                  |
| ------------------------ | --------------------------- | ---------------------------------------- |
| **WebServiceDown**       | Detect service outage       | `up == 0` for 1m                         |
| **TooManyFailedLookups** | Detect excessive 404 errors | `increase(url_not_found_total[5m]) > 10` |
| **HighShortenLatency**   | Slow `/shorten` requests    | 95th percentile > 1s                     |
| **HighRedirectLatency**  | Slow redirects              | 95th percentile > 1s                     |
| **NoRedirects**          | Service idle but running    | redirect rate < 0.001                    |


# These alerts protect availability & performance.

## 2. Alertmanager Configuration

* File: alertmanager.yml

* Two notification channels were added:

# Telegram Alerts

* Sends instant messages to Telegram chat

* Markdown formatting

* Uses bot token + chat ID

# Adding Telegram Alerts (Steps)

* Create a Telegram Bot

* Get Chat ID

* Add Telegram Settings to Alertmanager :
```yaml
telegram_configs:
  - bot_token: "<bot_token>"
    api_url: "https://api.telegram.org"
    chat_id: <chat_id>
    message: "*Alert:* {{ .CommonLabels.alertname }}\n*Severity:* {{ .CommonLabels.severity }}\n{{ .CommonAnnotations.description }}"
    parse_mode: "Markdown"
```

# Gmail Email Alerts

* HTML formatted alerts

* Uses Gmail SMTP (App Password)

# Adding Gmail Email Alerts (Steps)

* Enable 2-Step Verification

* Create a Gmail App Password

* Add Email Settings to Alertmanager :
```yaml
email_configs:
  - to: "your_email@gmail.com"
    from: "your_email@gmail.com"
    smarthost: "smtp.gmail.com:587"
    auth_username: "your_email@gmail.com"
    auth_identity: "your_email@gmail.com"
    auth_password: "<app_password>"
    require_tls: true
```

All alerts are routed through a receiver named notifications.

## 3. Alert Routing & Suppression

* Key Alertmanager features configured:

* group_by: alertname → avoids spam

* group_wait: 30s

* group_interval: 15s

* repeat_interval: 1h

Inhibition rules: suppress warnings if a critical alert for same service is firing

This ensures professional-level signal-to-noise control.

# Configuration Files Added This Week
prometheus/
│── alerts.rules.yml     # All alert definitions
│── alertmanager.yml     # Notification routing (Telegram + Gmail)
└── prometheus.yml       # Updated to load rules + alertmanager
## 4. Prometheus Configuration Updates

* File: prometheus.yml

* The following additions were made:

```yaml
rule_files:
  - ./prometheus/alerts.rules.yml

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

```
## Docker Compose Integration

# Alertmanager service added:

```yaml
alertmanager:
  image: prom/alertmanager:latest
  container_name: alertmanager
  volumes:
    - ./prometheus/alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
  command:
    - '--config.file=/etc/alertmanager/alertmanager.yml'
  ports:
    - "9093:9093"
```


# Prometheus now loads alerts:

volumes:
  - ./prometheus/alerts.rules.yml:/etc/prometheus/alerts.rules.yml:ro

## How Alerts Flow (Monitoring → Alerting)

* Flask app exposes /metrics

* Prometheus scrapes data every 5 seconds

* Alert rules evaluate conditions

* If triggered → alert sent to Alertmanager

* Alertmanager:

* Groups alerts

* Applies inhibition

* Sends notifications to Telegram + Email

* Alerts reach:

📱 Telegram instantly

📧 Gmail with full HTML details

## 📊 Useful PromQL Queries
# Check service uptime
``` up{job="flask_app"} ```

# URL 404 spike
``` increase(url_not_found_total[5m]) > 10 ```

# 95th percentile latency
``` histogram_quantile(0.95, sum(rate(shorten_request_latency_seconds_bucket[5m])) by (le)) > 1 ```

# Redirect traffic rate
``` rate(url_redirects_total[5m]) < .01 ```

## Week 4 Summary

* Week 4 introduces the full alerting system for the project:

* Advanced Prometheus alerting

* Full Alertmanager pipeline

* Dual-channel notifications (Telegram + Gmail)

* Intelligent alert grouping & suppression

---
# URL Shortener – Week 5 Progress

**Author:** _Mahmoud Elsayed Hussein_  
**Team Role:** _CI/CD Pipeline – Jenkins_  
**Branch:** `pipeline`

---

## Overview

During Week 5, I implemented the complete **CI/CD pipeline** for the project using **Jenkins**, fully integrated with **AWS ECR** and **AWS ECS**.  
This pipeline automates the entire flow: **code push → Docker build → push to ECR → automatic ECS deployment**.

All pipeline-related work is located in the GitHub branch:  
➡️ **`pipeline`**

---

## 🚀 Key Deliverables

### ✔ 1. Jenkinsfile

A full declarative pipeline that automates:

- Loading shared functions from `script.groovy`
- AWS authentication using Jenkins credentials
- Building Docker images for:
  - Web App (Flask)
  - Prometheus
  - Alertmanager
  - Grafana
- Pushing all images to Amazon ECR
- Deploying all services to Amazon ECS using rolling updates

---

### ✔ 2. script.groovy

A helper script that provides reusable functions:

| Function | Description |
|---------|-------------|
| `buildImage(repo, tag)` | Builds Docker images |
| `awsLogin(repo, region)` | Logs Jenkins into AWS ECR |
| `pushImage(repo, tag)` | Pushes images to ECR |
| `deployToEcs(cluster, service, region)` | Triggers ECS rolling deployments |

This approach keeps the Jenkinsfile clean and modular.

---

## 🔁 CI/CD Pipeline Workflow

### **1. Developer Pushes to GitHub (`pipeline` branch)**  
Jenkins automatically triggers the pipeline.

### **2. AWS ECR Login**  
Jenkins authenticates using stored AWS credentials (`aws-creds`).

### **3. Build Docker Images**  
All four services (Web, Prometheus, Alertmanager, Grafana) are built from source.

### **4. Push Images to AWS ECR**  
Each image is pushed to its corresponding ECR repository.

### **5. Deploy to AWS ECS**


---

## 🏗️ AWS Services Used

| AWS Service | Purpose |
|-------------|---------|
| **ECR** | Stores Docker images |
| **ECS (Fargate)** | Runs the containers in production |
| **IAM** | Secures Jenkins → AWS access |
| **Jenkins** | Automates CI/CD pipeline |

---

## 🎯 Benefits of the Pipeline

- Fully automated build → push → deploy process
- Zero manual AWS command execution
- Ensures all services are always up-to-date
- Production-grade CI/CD workflow
- Clean and scalable deployment architecture

---

## ⭐ Summary of Week 5

In Week 5, I delivered the **CI/CD automation pipeline**:

- Implemented Jenkinsfile
- Created modular `script.groovy`
- Automated Docker builds for all services
- Automated pushes to AWS ECR
- Automated deployments to AWS ECS
- Completed the production-level DevOps workflow

This final component completes the full lifecycle of the project from development → monitoring → alerting → CI/CD deployment.


* Production-ready monitoring workflow

* This completes the full observability layer for the URL Shortener system.

---
# AWS

## 🚀 AWS Deployment Overview

This project is fully deployed on **AWS** using a container-based architecture.  
The backend service (Flask URL Shortener), Prometheus, Grafana, and Alertmanager are all deployed as **independent ECS services**, each using Docker images stored in **Amazon ECR**.

---

## 🧱 AWS Architecture Components

### 1. **Amazon ECR (Elastic Container Registry)**
Four repositories were created to store Docker images:

- `depi-devops-project` — Flask web application  
- `depi-prometheus`  
- `depi-grafana`  
- `depi-alertmanager`

Images are built and pushed automatically through a Jenkins pipeline using AWS CLI authentication.

---

### 2. **Amazon ECS (Elastic Container Service)**
The system runs using **ECS EC2 mode**, where each component is deployed as a separate ECS service.

Created ECS services:

- **Web Service** (Flask app)
- **Prometheus Service**
- **Grafana Service**
- **Alertmanager Service**

Each service pulls its Docker image from the corresponding ECR repository.

---

### 3. **ECS Task Definitions**
Each service has its own task definition containing:

- ECR image reference  
- Exposed ports  
- CPU & memory limits  
- Logging via CloudWatch  
- Environment variables (for web app)

This ensures independent and scalable microservice-style deployment.

---

### 4. **Networking (VPC + Security Groups)**

Internal communication includes:

- Prometheus → Web App (metrics scraping)  
- Prometheus → Alertmanager (alert delivery)  
- Grafana → Prometheus (dashboard queries)

Security groups allow specific ports:

- **5000** – Web App  
- **9090** – Prometheus  
- **9093** – Alertmanager  
- **3000** – Grafana

Only internal traffic between services is allowed.

---

### 5. **AWS CloudWatch Logs**
All ECS containers send logs to **CloudWatch** using:

```json
"awslogs-group": "/ecs/<service-name>",
"awslogs-region": "eu-north-1",
"awslogs-stream-prefix": "ecs"
```

---

### 6. **Jenkins CI/CD Pipeline**

The Jenkins pipeline automates the deployment process for all services (Web, Prometheus, Alertmanager, Grafana).  
The pipeline performs the following steps:

1. **Authenticate to AWS ECR** using:
   ```bash
   aws ecr get-login-password
   ```
2. **Build Docker images** for each service.
3. **Push images** to the AWS ECR repositories.
4. **Trigger ECS rolling updates** using:
   ```bash
   aws ecs update-service --force-new-deployment
   ```
This ensures that any new code change is automatically built, pushed, and deployed to ECS.


---

### 7. **Monitoring & Alerting on AWS**

- **Prometheus** scrapes metrics from the Flask application and evaluates alert rules.
- **Alertmanager** sends notifications through:
  - **Telegram Bot**
  - **Email (SMTP Gmail)**
- **Grafana** loads:
  - Pre-provisioned datasources  
  - Pre-provisioned dashboards  
- All services run in separate ECS tasks, each pulling its latest image from ECR.


---

### **AWS Summary**

This project uses AWS services to create a fully automated, scalable, and observable deployment environment:

- **Amazon ECR** stores all Docker images for Web, Prometheus, Alertmanager, and Grafana.
- **Amazon ECS (EC2 Launch Type)** runs each service in an isolated task.
- **Jenkins** automatically builds, pushes, and deploys updates to ECS through a CI/CD pipeline.
- **Prometheus, Alertmanager, and Grafana** are deployed on AWS and connected together to provide:
  - Real-time metrics  
  - Custom dashboards  
  - Automated Telegram & Email alerts  
- The system is fully integrated and continuously updated with every code change.

This AWS setup ensures reliability, automation, and complete visibility over application performance.
