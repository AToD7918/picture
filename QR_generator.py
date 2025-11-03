import qrcode
import os
import json
import time
from pathlib import Path

# 현재 스크립트의 디렉토리를 기준으로 경로 설정
SCRIPT_DIR = Path(__file__).parent
PHOTOS_DIR = SCRIPT_DIR / "photos"
QR_DIR = SCRIPT_DIR / "QR"
MANIFEST_FILE = SCRIPT_DIR / "manifest.json"
VERSION_FILE = SCRIPT_DIR / "version.txt"

def get_image_files(directory):
    """photos 디렉토리에서 이미지 파일 목록을 가져옴"""
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    image_files = []
    
    if not directory.exists():
        print(f"경고: {directory} 디렉토리가 존재하지 않습니다.")
        return image_files
    
    for file in sorted(directory.iterdir()):
        if file.is_file() and file.suffix.lower() in supported_formats:
            image_files.append(file.name)
    
    return image_files

def update_manifest():
    """manifest.json 파일을 photos 디렉토리의 실제 이미지로 업데이트"""
    images = get_image_files(PHOTOS_DIR)
    
    manifest_data = {
        "title": "My Photos",
        "images": []
    }
    
    for img in images:
        # 파일명에서 확장자를 제거하여 ID로 사용
        img_id = Path(img).stem
        manifest_data["images"].append({
            "id": img_id,
            "src": f"photos/{img}",
            "alt": img_id.upper()
        })
    
    # manifest.json 저장
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ manifest.json 업데이트 완료 ({len(images)}개 이미지)")
    return len(images)

def update_version():
    """version.txt 파일을 현재 타임스탬프로 업데이트"""
    timestamp = str(int(time.time() * 1000))  # 밀리초 단위 타임스탬프
    
    with open(VERSION_FILE, 'w', encoding='utf-8') as f:
        f.write(timestamp)
    
    print(f"✓ version.txt 업데이트 완료 (v{timestamp})")
    return timestamp

def generate_qr():
    """QR 코드 생성 (이미 존재하면 건너뜀)"""
    url = "https://AToD7918.github.io/picture/"
    
    # QR 디렉토리 생성
    QR_DIR.mkdir(exist_ok=True)
    
    # QR 코드 파일 경로
    qr_path = QR_DIR / "photo_qr.png"
    
    # 이미 QR 코드가 있으면 생성하지 않음
    if qr_path.exists():
        print(f"✓ QR 코드 이미 존재함 (건너뜀): {qr_path}")
        return False
    
    # QR 코드 생성 및 저장
    qrcode.make(url).save(str(qr_path))
    print(f"✓ QR 코드 생성 완료: {qr_path}")
    return True

def main():
    print("=" * 50)
    print("Photo Gallery 배포 준비")
    print("=" * 50)
    
    # 1. manifest.json 업데이트
    print("\n[1/3] manifest.json 업데이트 중...")
    img_count = update_manifest()
    
    # 2. version.txt 업데이트
    print("\n[2/3] version.txt 업데이트 중...")
    version = update_version()
    
    # 3. QR 코드 생성 (이미 있으면 건너뜀)
    print("\n[3/3] QR 코드 확인 중...")
    qr_created = generate_qr()
    
    print("\n" + "=" * 50)
    print("✓ 모든 작업 완료!")
    print(f"  - 이미지 수: {img_count}개")
    print(f"  - 버전: {version}")
    print(f"  - QR 코드: {'새로 생성됨' if qr_created else '기존 사용'}")
    print("  - URL: https://AToD7918.github.io/picture/")
    print("\n💡 QR 코드는 한번 생성되면 변경되지 않습니다.")
    print("   웹페이지는 버전 관리로 항상 최신 내용을 보여줍니다.")
    print("=" * 50)

if __name__ == "__main__":
    main()