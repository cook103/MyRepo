FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get purge -y --auto-remove && \
    rm -rf /var/lib/apt/lists/

RUN git clone https://github.com/cook103/MyRepo.git

RUN chmod +x MyRepo/FullStackApps/StockAnalyzerApp/run_app.py

WORKDIR MyRepo/FullStackApps/StockAnalyzerApp

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["./run_app.py"]
