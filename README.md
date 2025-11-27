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

