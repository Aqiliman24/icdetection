FROM python:3.10.2
WORKDIR /icrecognition
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python","icrecognitionapp.py"]

# FROM nginx
# RUN rm /etc/nginx/conf.d/default.conf
# COPY config/nginx.config /etc/nginx/conf.d/default.conf
# COPY dist/McReportGenerator /usr/share/nginx/html