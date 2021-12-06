FROM python:3
LABEL description="pavelpetrcz/saunaCbOccupancy"
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install df2gspread
CMD python ./main.py