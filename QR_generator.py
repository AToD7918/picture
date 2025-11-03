import qrcode, os

url = "https://AToD7918.github.io/picture/"
os.makedirs("C:\\Users\\tjrgk\\Desktop\\Git\\picture\\QR", exist_ok=True)  # 폴더 자동 생성
qrcode.make(url).save("C:\\Users\\tjrgk\\Desktop\\Git\\picture\\QR\\photo_qr.png")