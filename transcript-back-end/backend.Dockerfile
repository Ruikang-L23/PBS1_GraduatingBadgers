FROM python:3.9-slim

WORKDIR /backend

COPY . .

RUN pip install --no-cache-dir beautifulsoup4 pycaption 
RUN pip install --no-cache-dir flask flask-cors openai==0.28

EXPOSE 5000

CMD ["python", "api.py"]
