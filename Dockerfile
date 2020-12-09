FROM python:3

COPY bot/ ./bot/
COPY game/ ./game/
COPY images/ ./images/ 
COPY res/ ./res/ 
COPY util/ ./util/
COPY main.py requirements.txt ./
RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]