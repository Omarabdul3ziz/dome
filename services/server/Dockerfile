FROM python:3

WORKDIR /usr/src/app

COPY requirments.txt ./

RUN python3 -m pip install --user --no-cache-dir -r requirments.txt

COPY . .

CMD ["python", "app.py"]