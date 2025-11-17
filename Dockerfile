# 1. 베이스 이미지
FROM python:3.12-slim

# 2. 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리
WORKDIR /app

# 4. 프로젝트 파일 복사
COPY . /app

# 5. pip 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. 포트 설정
EXPOSE 8000

# 7. 컨테이너 시작 명령
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]