
# 🍸 BarBuddy

[![Web App CI](https://github.com/software-students-spring2025/5-final-machine-not-learning/actions/workflows/webci.yml/badge.svg)](https://github.com/software-students-spring2025/5-final-machine-not-learning/actions/workflows/webci.yml)

BarBuddy is your ultimate personal cocktail companion, crafted to enhance your at-home mixology adventures. Whether you're a seasoned pro or just starting to explore the world of cocktails, BarBuddy provides the ideal mix of inspiration and convenience. The app makes it simple to manage your home bar inventory by tracking the spirits, mixers, and garnishes you have on hand. Using your current ingredients, BarBuddy recommends a diverse selection of cocktail recipes tailored to your preferences and supplies.

Beyond just suggestions, BarBuddy monitors items nearing expiration, helping you make the most of your inventory while reducing waste. You can easily save your favorite drinks, create a custom cocktail library, and explore exciting new recipes. With a sleek interface and intelligent features, BarBuddy transforms every night into a chance to discover, craft, and enjoy amazing cocktails—all from the comfort of your home.

---
## 📦 Docker Images
- [Web Application](https://hub.docker.com/repository/docker/williamma205/webapp/general)

---

## 👥 Team Members

- 1: [Xiaowei Ma](https://github.com/maxiaowei)
- 2: [Mandy Mao](https://github.com/WillliamMa)
- 3: [Rishi Rana](https://github.com/Rishi-Rana1)
- 4: [Max Luetke Meyring](https://github.com/maxlmeyring)

---

## Digital Ocean Deployed URL

Please access the application via the following link:

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