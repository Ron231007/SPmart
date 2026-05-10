# Use Raspberry Pi OS Bullseye base image
FROM arm64v8/debian:bullseye-slim

# Set environment variable to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV SPI_PATH=/app/SPI-Py

# Install core OS tools and add RPi repository
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | apt-key add -
RUN echo "deb http://archive.raspberrypi.org/debian/ bullseye main" > /etc/apt/sources.list.d/raspi.list

# Install Picamera2 and Raspberry Pi-specific packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libzbar0\
    v4l-utils \
    i2c-tools \
    rpi.gpio-common \
    libcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy app files
COPY SPI-Py ./SPI-Py
COPY hal ./hal
COPY newonewithrightID ./website
COPY running_script.sh ./

COPY access_database.py ./
COPY buy_products_process.py ./ 
COPY Buzzer_Switch.py ./
COPY calculatePrice_or_points.py ./
COPY checkout.py ./
COPY credentials.py ./
COPY DCmotor.py ./
COPY Display_menu.py ./
COPY get_keypad_value.py ./
COPY LEDLight.py ./
COPY main.py ./
COPY password.py ./
COPY requirements.txt ./
COPY RFID.py ./
COPY scanbarcode.py ./
COPY Ultrasound.py ./


# Install hardware-specific Python libraries
RUN pip3 install --no-cache-dir rpi-gpio smbus spidev


# Install pip dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install the SPI-Py driver
WORKDIR $SPI_PATH
RUN python3 setup.py install

# Set user to root (required for camera access)
USER root
# Return to root directory
WORKDIR /app

RUN chmod +x running_script.sh
EXPOSE 5000

# Run both hardware and software
CMD ["./running_script.sh"]
