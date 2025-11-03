import qrcode
import os
import json
import re
from pathlib import Path

# 현재 스크립트의 디렉토리를 기준으로 경로 설정
SCRIPT_DIR = Path(__file__).parent
PHOTOS_DIR = SCRIPT_DIR / "photos"
QR_DIR = SCRIPT_DIR / "QR"
MANIFEST_FILE = SCRIPT_DIR / "manifest.json"

def rename_photos_to_numbers():
    """photos 폴더의 모든 이미지 파일을 1, 2, 3... 순서로 이름 변경"""
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    
    if not PHOTOS_DIR.exists():
        print(f"경고: {PHOTOS_DIR} 디렉토리가 존재하지 않습니다.")
        return 0
    
    # 모든 이미지 파일 수집
    image_files = []
    for file in PHOTOS_DIR.iterdir():
        if file.is_file() and file.suffix.lower() in supported_formats:
            image_files.append(file)
    
    if not image_files:
        print("경고: photos 폴더에 이미지 파일이 없습니다.")
        return 0
    
    # 파일 이름으로 정렬 (기존 순서 유지)
    image_files.sort(key=lambda f: f.name.lower())
    
    # 임시 이름으로 먼저 변경 (충돌 방지)
    temp_files = []
    for i, old_file in enumerate(image_files, 1):
        temp_name = f"temp_{i}{old_file.suffix}"
        temp_path = PHOTOS_DIR / temp_name
        old_file.rename(temp_path)
        temp_files.append((temp_path, i, old_file.suffix))
    
    # 최종 이름으로 변경
    renamed_count = 0
    for temp_path, num, ext in temp_files:
        new_name = f"{num}{ext}"
        new_path = PHOTOS_DIR / new_name
        temp_path.rename(new_path)
        renamed_count += 1
    
    print(f"✓ 파일 이름 변경 완료 ({renamed_count}개 파일 → 1, 2, 3...)")
    return renamed_count

def get_image_files(directory):
    """photos 디렉토리에서 이미지 파일 목록을 가져옴"""
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    image_files = []
    
    if not directory.exists():
        print(f"경고: {directory} 디렉토리가 존재하지 않습니다.")
        return image_files
    
    for file in directory.iterdir():
        if file.is_file() and file.suffix.lower() in supported_formats:
            image_files.append(file.name)
    
    # 숫자 파일명 자연스럽게 정렬 (1.jpg, 2.jpg, 10.jpg 순서로)
    def natural_sort_key(filename):
        # 파일명에서 숫자 부분 추출하여 정수로 변환
        stem = Path(filename).stem
        numbers = re.findall(r'\d+', stem)
        if numbers:
            return int(numbers[0])
        return float('inf')  # 숫자가 없으면 맨 뒤로
    
    image_files.sort(key=natural_sort_key)
    return image_files

def update_manifest():
    """manifest.json 파일을 photos 디렉토리의 실제 이미지로 업데이트"""
    images = get_image_files(PHOTOS_DIR)
    
    manifest_data = {
        "title": "My Photos",
        "images": []
    }
    
    for img in images:
        # 파일명에서 확장자를 제거하여 ID로 사용 (숫자 그대로)
        img_id = Path(img).stem
        manifest_data["images"].append({
            "id": img_id,
            "src": f"photos/{img}",
            "alt": f"Photo {img_id}"
        })
    
    # manifest.json 저장 (UTF-8 인코딩)
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ manifest.json 업데이트 완료 ({len(images)}개 이미지)")
    return len(images)

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
    
    # 0. 파일 이름을 1, 2, 3... 으로 변경
    print("\n[1/3] 파일 이름 정리 중...")
    rename_photos_to_numbers()
    
    # 1. manifest.json 업데이트
    print("\n[2/3] manifest.json 업데이트 중...")
    img_count = update_manifest()
    
    # 2. QR 코드 생성 (이미 있으면 건너뜀)
    print("\n[3/3] QR 코드 확인 중...")
    qr_created = generate_qr()
    
    print("\n" + "=" * 50)
    print("✓ 모든 작업 완료!")
    print(f"  - 이미지 수: {img_count}개")
    print(f"  - QR 코드: {'새로 생성됨' if qr_created else '기존 사용'}")
    print("  - URL: https://AToD7918.github.io/picture/")
    print("\n💡 페이지는 항상 강제 새로고침으로 최신 이미지를 표시합니다.")
    print("=" * 50)

if __name__ == "__main__":
    main()