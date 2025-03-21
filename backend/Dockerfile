FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update system and install dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    build-essential \
    unzip \
    cmake \
    nasm \
    gnupg \
    libfontconfig1 \
    libcairo2 \
    libjpeg-turbo8 \
    software-properties-common \
    wget \
    git \
    pngquant \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# # Install Google Chrome 114
# RUN wget https://chrome-versions.com/google-chrome-stable-114.0.5735.106-1.deb -O /tmp/google-chrome.deb && \
#     apt-get update && \
#     apt-get install -y /tmp/google-chrome.deb && \
#     rm /tmp/google-chrome.deb

# # Install ChromeDriver
# RUN apt-get update && apt-get install -y unzip curl wget && \
#     CHROMEDRIVER_VERSION=114 && \
#     wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.16/chromedriver_linux64.zip && \
#     unzip /tmp/chromedriver.zip -d /usr/bin/ && \
#     chmod +x /usr/bin/chromedriver && \
#     rm /tmp/chromedriver.zip

# Install Python 3.9
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.9 \
    python3.9-distutils \
    python3.9-venv \
    && wget https://bootstrap.pypa.io/get-pip.py \
    && python3.9 get-pip.py \
    && rm get-pip.py

# Set Python 3.9 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1


# Install pdf2htmlEX
RUN wget https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb && \
    mv pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb pdf2htmlEX.deb && \
    apt-get install -y ./pdf2htmlEX.deb && \
    rm pdf2htmlEX.deb

# Test pdf2htmlEX installation
RUN pdf2htmlEX -v

# Set working directory
WORKDIR /code

# Copy requirements and install Python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code
COPY . /code

# Expose port
EXPOSE 80 8998

# Start FastAPI app
# CMD ["fastapi", "run", "/code/main.py", "--port", "80"]
# CMD ["uvicorn", "app.main:app", "--reload" , "--host", "0.0.0.0", "--port", "80"]
# Start FastAPI app with debugpy
CMD ["python3.9", "-m", "debugpy", "--listen", "0.0.0.0:8998", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]