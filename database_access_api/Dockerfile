FROM tiangolo/uvicorn-gunicorn:python3.9

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
ENV MODULE_NAME=app

ADD requirements.txt .
#ADD templates ./templates

RUN pip install --upgrade pip
# RUN pip install wheel
RUN pip3 install -r requirements.txt

# COPY ./templates /app/templates
# COPY app.py /app
# COPY requirements.txt /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
