FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app.py extraalearn_lead_conversion.joblib ./

EXPOSE 5000

CMD ["python", "app.py"]
