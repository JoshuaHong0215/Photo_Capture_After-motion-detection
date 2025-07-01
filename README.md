# Photo_Capture_After-motion-detection
After motion detect, LED Flicker and e-mail sent 

# Feature
모션 감지 후 LED가 깜빡거리며 사진을 찍고 지정된 이메일로 사진을 전송하며 1분 동안 감지가 이루어지지않을 경우 점등 되는 보안 프로그램

# 보완사항
GPS모듈(NEO-6M, u-blox, VK-172)이 있다면 추후 아래와 같은 절차를 따를것

[1-2] 라즈베리파이에 설치
1. pip install gpsd-py3 설치
2. sudo apt install gpsd gpsd-clients
   sudo systemctl stop gpsd.socket
   sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock


3. 코드 수정_추후

import gpsd

#GPSD에 연결하는 함수

gpsd.connect()

#GPS 좌표 가져오는 함수

def get_gps_location():
    try:
        packet = gpsd.get_current()
        latitude = packet.lat
        longitude = packet.lon
        return f"Lat: {latitude:.6f}, Lon: {longitude:.6f}"
    except:
        return "위치 확인 불가"

3-1 timestamp = time.strftime(.....)아래에 gps_text = get_gps_location()추가
3-2 cv2.puttext(frame.timestamp (10, 30)....코드 줄 아래에 10,60좌표에 gps_text 코드삽입하는 코드 작성


# Image
![Photo_capture_image](https://github.com/user-attachments/assets/c3415a3b-141b-468b-8006-f3e998c4a06e)
