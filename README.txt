# Bienvenue dans le projet 8INF349_projet_web

## Setup Instructions

## Using Docker
1. **Build the image**
```bash
    docker build -t flask-app .
```
2. **run the container**
```bash
    docker run -p 5000:5000 flask-app
```

## Without Docker
1. **Clone the repository**
ssh:
```bash
    git clone git@github.com:Ludovic-Potvin/8INF349_projet_web.git
```
https:
```bash
    git clone https://github.com/Ludovic-Potvin/8INF349_projet_web.git
```

2. **Run the setup script**

> **_NOTE:_**  Write that code in pycharm terminal (alt+f12)

```bash
    .\setup.bat
```

3. **Activate the virtual environment**

```bash
    venv\Scripts\activate
```

4. **Launch the app**
```bash
    python app.py
```