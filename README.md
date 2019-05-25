# flask-demo-app

Just a simple Flask application.

## Getting Started

Clone the project, and choose whether you want to run the application from a virtualenv or via Docker.

### Installing via virtualenv

```bash
cd flask-demo-app
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Installing via Docker

```bash
cd flask-demo-app
docker build -t flask-custom-app .
docker run --rm --name flask-custom-app -p 5000:5000 flask-custom-app
```
