# je met ma version de python
FROM python:3.12-slim

# je donne le root 
WORKDIR /app

# je met une copy des requirements
COPY requirements.txt .

# on install les pips sans le cache pour plus leger
RUN pip install -r requirements.txt --no-cache-dir

# on copy TOUT le code : SAUF .dockerignore
COPY . .

# commandes a exectuer 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]