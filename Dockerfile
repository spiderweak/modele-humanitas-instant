FROM python:3.11

WORKDIR /app

COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

CMD [ "python", "modelisation-2d.py" ]