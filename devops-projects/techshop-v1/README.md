# TechShop - E-commerce Platform

**Level 1: Beginner** - Static website with Docker containerization

## 📋 Description

TechShop is an e-commerce platform for electronics, built as part of a DevOps learning curriculum. This is Level 1 (Beginner) focusing on fundamental DevOps technologies: static HTML/CSS, Nginx web server, and Docker containerization.

## 🖼️ Demo

![TechShop Homepage](https://github.com/DavyRoy/TechShop-E-commerce/blob/main/devops-projects/techshop-v1/Снимок%20экрана%202026-02-18%20в%2020.46.32.png)

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3
- **Web Server**: Nginx (Alpine Linux)
- **Containerization**: Docker
- **Automation**: Bash scripts
- **Version Control**: Git & GitHub

## 📦 Project Structure
```
techshop-v1/
├── src/                  # HTML/CSS files
│   ├── index.html
│   ├── catalog.html
│   ├── about.html
│   ├── styles.css
│   └── images/
├── nginx/                # Nginx configuration
│   └── nginx.conf
├── scripts/              # Automation scripts
│   ├── build.sh
│   └── run.sh
├── Dockerfile            # Docker image definition
├── .dockerignore         # Docker ignore file
└── README.md
```

## ⚙️ Requirements

- Docker (version 20.x or higher)
- Git
- 100MB free disk space

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/DavyRoy/TechShop-E-commerce.git
cd TechShop-E-commerce
```

### 2. Build Docker image
```bash
./scripts/build.sh
```

### 3. Run container
```bash
./scripts/run.sh
```

### 4. Access the website
Open your browser and navigate to: `http://localhost:8081`

## 📖 Detailed Instructions

### Manual Build and Run

If you prefer not to use scripts:

**Build image:**
```bash
docker build -t techshop:v1 .
```

**Run container:**
```bash
docker run -d -p 8081:80 --name techshop-container techshop:v1
```

**Stop container:**
```bash
docker stop techshop-container
docker rm techshop-container
```

## 🏗️ Architecture
```
[Browser] --HTTP--> [Docker Container]
                         |
                    [Nginx :80]
                         |
                    [Static Files]
                    (HTML/CSS/JS)
```

## 📝 Features

- ✅ Responsive design
- ✅ Three pages (Home, Catalog, About)
- ✅ Product catalog with 6 items
- ✅ Containerized deployment
- ✅ Automated build and run scripts

## 🎓 Learning Objectives

This project demonstrates:
- Writing Nginx configuration
- Creating Dockerfiles
- Container build process
- Bash script automation
- Git version control
- Professional documentation

## 👨‍💻 Author

Sergey - DevOps Learning Journey

## 📄 License

This is a learning project - not for production use.

## 🔗 Links

- [GitHub Repository](https://github.com/DavyRoy/TechShop-E-commerce.git)
- [Learning Curriculum](https://github.com/DavyRoy/TechShop-E-commerce/blob/main/README.md)

## 🚀 Next Steps

- Level 2: Add PostgreSQL database
- Level 2: Implement CI/CD with GitHub Actions
- Level 2: Add monitoring with Prometheus

---

**Project Status**: ✅ Level 1 Complete (February 2026)