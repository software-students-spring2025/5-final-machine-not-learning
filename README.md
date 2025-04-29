
# 🍸 BarBuddy

[![Web App CI](https://github.com/software-students-spring2025/5-final-machine-not-learning/actions/workflows/webci.yml/badge.svg)](https://github.com/software-students-spring2025/5-final-machine-not-learning/actions/workflows/webci.yml)

BarBuddy is your ultimate personal cocktail companion, designed to elevate your at-home mixology experience. Whether you're a seasoned bartender or just beginning your journey into the world of cocktails, BarBuddy offers the perfect blend of convenience and inspiration. The app helps you effortlessly manage your home bar inventory by keeping track of the spirits, mixers, and garnishes you have on hand. Based on your current ingredients, BarBuddy suggests a wide variety of cocktail recipes tailored to your personal preferences and available supplies.

In addition to recommendations, BarBuddy tracks items that are nearing expiration, ensuring you get the most out of your stock and reduce waste. You can also save your favorite drinks, build a personalized cocktail library, and explore new recipes with ease. With an intuitive interface and smart features, BarBuddy turns every night into an opportunity to discover, mix, and enjoy delicious cocktails—right from the comfort of your home.

---
## 📦 Docker Images
- [Web Application](https://hub.docker.com/repository/docker/williamma205/webapp/general)

---

## 👥 Team Members

- [Xiaowei Ma](https://github.com/maxiaowei)
- [Mandy Mao](https://github.com/WillliamMa)
- [Rishi Rana](https://github.com/Rishi-Rana1)
- [Max Luetke Meyring](https://github.com/maxlmeyring)

---

## Digital Ocean Deployed URL

You can access the application from:

https://bartender-6r98j.ondigitalocean.app

## 🛠️ Setup Instructions

### Prerequisites

- Docker & Docker Compose
- Python 3.10
- MongoDB Atlas account

### 1. Clone the repo

```bash
git clone https://github.com/software-students-spring2025/5-final-machine-not-learning.git
```

### 2. Environment Setup

Enter the project repository:

```bash
touch .env
```

Edit `.env` and set the following:

```
MONGO_URI=mongodb+srv://youruser:yourpass@yourcluster.mongodb.net/?retryWrites=true&w=majority
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key
```

### 3. Run with Docker

```bash
docker-compose up --build
```

App will be available at `http://127.0.0.1:8080`

---