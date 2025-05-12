FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ai_recipe.py ./
COPY templates/ ./templates/
COPY .env ./

ENV PORT=8000
EXPOSE 8000

CMD ["python", "app.py"]