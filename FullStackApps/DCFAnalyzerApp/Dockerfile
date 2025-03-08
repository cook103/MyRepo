FROM python:3.9-slim

WORKDIR /app

COPY stock_analyzer.py /app/

COPY ../../MyApps/StockAnalysis/DCFAnalyzer/dcf_analyzer.py /app/

COPY requirements.txt /app/

COPY static/ /app/static
COPY templates/ /app/templates

RUN chmod +x /app/stock_analyzer.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

ENTRYPOINT ["python3", "/app/stock_analyzer.py"]
