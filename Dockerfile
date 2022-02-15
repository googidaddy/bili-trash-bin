FROM mcr.microsoft.com/playwright:focal
WORKDIR /app
COPY . .
RUN apt-get update -y &&\
    apt-get install -y ca-certificates &&\
    apt-get install -y vim &&\
    apt-get install -y ffmpeg &&\
    pip install -r /app/requirements.txt
CMD ["python", "video.py"]