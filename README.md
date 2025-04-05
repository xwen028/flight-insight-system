# ✈️ Flight Prediction System – NUS AD Project
This repository contains the source code for **Flight Prediction based on Machine Learning**, developed as part of the NUS Application Development Capstone Project by Team 2.
The system predicts flight delays and future ticket prices using machine learning, and recommends optimal flight combinations — delivered through both web and Android mobile interfaces.  
🔗 **Explore our full team portfolio:** [Team 2 GitHub Organisation](https://github.com/sa58team2)

## 🎯 Key Features
### 🔍 Prediction Functions
- Predict future flight ticket prices (Random Forest)
- Predict flight delay reasons and risk (Neural Network)
- Forecast flight cancellation rates
### ✈️ Flight Optimisation
- Recommend cheapest/fastest flights based on user input
- Search by origin, destination, waypoints, and date
### 🌦 Weather Forecast
- View real-time or forecasted weather for destination
### 📲 Platform Support
- Web app (Java Spring Boot)
- Mobile app (Android)
- Backend APIs + ML model integration

## 🧠 Machine Learning Models
| Model           | Purpose                      | Technique       |
|----------------|------------------------------|-----------------|
| Random Forest   | Ticket Price Prediction       | Regression      |
| Neural Network  | Delay Risk & Reason Analysis | Classification  |

## 🛠 Tech Stack
- Java Spring Boot (Web Backend)
- Android (Mobile Frontend)
- Python (Machine Learning API)
- PostgreSQL
- RESTful APIs
- Docker, GitHub Actions, CI/CD
- Cloud Deployment (Docker Compose)

## 🧪 Project Setup Guide
To enable the project locally:
### ✅ Step 1: Start the Backend
#### 1.1 Start the Machine Learning API
```bash
cd code/ml
docker build -t ad-flask-app .
docker run --name ad-flask -p 5001:5001 ad-flask-app
```
#### 1.2 Start the Java Backend
```bash
cd code/backend
# Edit `application.properties` to match your DB config
docker build -t ad-maven-app .
docker run --name ad-maven -p 8080:8080 ad-maven-app
```

### ✅ Step 2: Start the Frontend
```bash
cd code/frontend
docker build -t ad-react-app .
docker run --name ad-react -p 3000:3000 ad-react-app
```
Now, your project is live on:
- Web UI → [http://localhost:3000](http://localhost:3000)  
- Backend API → [http://localhost:8080](http://localhost:8080)  
- ML API → [http://localhost:5001](http://localhost:5001)

## 🐳 One-Click Setup with Docker Compose
To simplify setup, we provide a `docker-compose.yml` for full integration.
### 📦 Project Structure
```
project-root/
├── code/
│   ├── ml/
│   ├── backend/
│   └── frontend/
└── docker-compose.yml
```
### 🚀 Start Everything at Once
```bash
docker-compose up --build
```
To stop all:
```bash
docker-compose down
```
### 💡 Benefits
- Auto-starts all 3 containers in the correct order
- Ideal for development, testing, and cloud deployment

## 📁 Project Artefacts
- 📊 ERD: `adProjERD.png`
- 🏗️ Architecture: `architecturalDiagram.png`
- 🎥 Submission Slides: `Main Submission Slides.pdf`
- 📄 Final Report: `Project Status Report.docx`
- 📝 Project Proposal: `Project Proposal.pdf`

## 📌 About the Capstone
This project was developed as part of the **NUS SA4106 AD Project module**, where students apply system design, full-stack development, ML integration, and DevOps practices to solve a real-world problem.
