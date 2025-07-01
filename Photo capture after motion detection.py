from gpiozero import LED, MotionSensor
import cv2
import time
from time import sleep
import os
import smtplib
from email.message import EmailMessage

# GPIO 핀 설정
led = LED(17)                  # LED는 GPIO 17번
pir = MotionSensor(4)          # SR505는 GPIO 4번

# 이메일 발신자 및 수신자 정보 설정
EMAIL_ADDRESS = "sebin5736@gmail.com"       # 보내는 이메일 주소
EMAIL_PASSWORD = "mrnt sfau vexx kipm"         # Gmail 앱 비밀번호
TO_EMAIL = "sebin105@naver.com"        # 받는 이메일 주소

# 사진 저장 폴더 생성
photo_folder = "./photos"
os.makedirs(photo_folder, exist_ok=True)

# 이메일 전송 함수 정의
def send_email(image_path):
    msg = EmailMessage()
    msg["Subject"] = "모션 감지됨 - 사진 첨부"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content("움직임이 감지되어 사진을 전송합니다.")

    with open(image_path, 'rb') as img:
        msg.add_attachment(img.read(), maintype="image", subtype="jpeg", filename=os.path.basename(image_path))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("메일 전송 완료:", os.path.basename(image_path))

# USB 웹캠 초기화
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

# 초기 변수 선언
last_motion_time = 0
last_capture_time = 0
img_counter = 0

print("시스템 시작. 화면 표시 중...")

while True:
    ret, frame = cam.read()
    if not ret:
        print("카메라 오류")
        break

    # 항상 카메라 영상 출력
    cv2.imshow("Camera", frame)
    cv2.waitKey(1)

    # 모션 감지되었을 때
    if pir.motion_detected:
        last_motion_time = time.time()

        # LED 깜빡이기
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)

        # 4초 간격으로 사진 촬영 및 메일 전송
        if time.time() - last_capture_time >= 4:
           
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 255), 2, cv2.LINE_AA)
           
            filename = f"{photo_folder}/image_{img_counter}.jpg"
            cv2.imwrite(filename, frame)
            print("사진 촬영:", filename)
            send_email(filename)
            img_counter += 1
            last_capture_time = time.time()

    else:
        # 1분 이상 감지 없을 경우 LED 꺼짐
        if time() - last_motion_time >= 60:
            led.off()
            last_capture_time = 0

    sleep(0.1)

# 종료 시 정리
cam.release()
cv2.destroyAllWindows()
