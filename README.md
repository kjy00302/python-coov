# Python으로 COOV 증명서 가지고 놀기

## 증명서 발급

fetcher.py를 통해 증명서를 발급받을 수 있다. 웹브라우저를 통해 본인 인증 절차를 완료한 후 수동으로 토큰을 추출해 입력해야 한다.

### 사용 방법

    fetcher.py

처음으로 실행시키면 자동적으로 본인 인증 페이지가 뜬다.

본인 인증을 진행한 후 "본인인증이 완료 되었습니다." 창이 뜬 상태에서 개발자 도구를 켜서 "eyJ"로 시작하는 JWT 토큰을 찾아 입력에 붙여 넣는다.

증명서는 coov.ini 파일에 저장된다.

### 주의할 점

본인 인증 페이지를 불러올 때 쓰는 키가 변경될 수 있다.

## 증명서 인증받기

responder.py를 통해 인증을 위한 QR 코드를 출력할 수 있다. 스크립트가 동작 중일 때만 인증이 가능하다

### 사용 방법

    responder.py <증명서 타입> <쉼표로 이은 증명할 VC 타입들>

### 사용 예

    responder.py user dob,name,isadult

### 주의할 점

VC 순서에 따라서 결과가 제대로 표시되지 않을 수 있다.

## 증명서 인증하기

caller.py를 통해 증명서를 읽을 수 있다. 5초 안으로 응답이 없으면 자동으로 종료된다.

### 사용 방법

    caller.py <상대편 일회용 코드>

### 사용 예

    caller.py did:infra:9dMcKjVz8m2YpXWppmQQ

    caller.py `zbarcam --raw -1`

## 사용한 라이브러리

 - [cryptography](https://github.com/pyca/cryptography)
 - [jwcrypto](https://github.com/latchset/jwcrypto)
 - [python-socketio](https://github.com/miguelgrinberg/python-socketio)
 - [qrcode](https://github.com/lincolnloop/python-qrcode)
