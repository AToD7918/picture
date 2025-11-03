# ? Photo Gallery

QR 코드로 공유할 수 있는 간단한 사진 갤러리

## ? 사용 방법

### 1?? 사진 추가하기

`photos/` 폴더에 숫자 이름의 이미지 파일을 넣으세요:

```
photos/
  1.jpg
  2.jpg
  3.jpg
  4.jpg
  ...
```

**지원 형식:** jpg, jpeg, png, gif, webp, bmp

### 2?? 자동 업데이트

```bash
python QR_generator.py
```

이 명령어는:
- ? `photos/` 폴더를 자동으로 스캔
- ? `manifest.json` 자동 생성
- ? QR 코드 생성 (처음 한 번만)

### 3?? GitHub에 배포

```bash
git add .
git commit -m "사진 업데이트"
git push
```

## ? 기능

- **스와이프**: 좌우로 스와이프하여 사진 전환
- **핀치 줌**: 두 손가락으로 확대/축소
- **더블탭**: 빠르게 2번 탭하여 확대/축소
- **팬 이동**: 확대 상태에서 드래그하여 이동
- **키보드**: ← → 화살표로 이동 (PC)

## ? 자동 정렬

파일명의 숫자를 기준으로 자연스럽게 정렬:
- `1.jpg` → `2.jpg` → `3.jpg` → ... → `10.jpg` → `11.jpg`

## ? URL

- **메인**: https://AToD7918.github.io/picture/
- **특정 사진**: https://AToD7918.github.io/picture/?id=3

## ? 팁

- **캐시 문제 없음**: 페이지가 자동으로 최신 버전을 로드
- **QR 코드 고정**: 한 번 생성된 QR 코드는 변경 없이 계속 사용
- **무제한 사진**: 원하는 만큼 사진 추가 가능
