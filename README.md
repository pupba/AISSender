# TCPA Sender

이 프로젝트는 AIS 데이터를 기반으로 TCPA(Time to Closest Point of Approach) 값을 계산하고, 입력된 IP 주소로 안전 여부를 반환하는 웹 페이지입니다.

## 사전 요구사항

-   Python 3.11.0
-   Pandas
-   Numpy
-   Flask 라이브러리 (`pip install flask` 명령어로 설치)

## 설치 및 실행

1. 이 저장소를 클론합니다:
   `git clone https://github.com/your/repository.git`
2. 프로젝트 디렉토리로 이동합니다:
   `cd tcpa-calculator`
3. 필요한 종속성을 설치합니다:
   `pip install -r requirements.txt`
4. 서버를 실행합니다:
   `python sender.py`

5. 웹 브라우저에서 `http://localhost:8080`으로 접속하여 TCPA 계산기 페이지에 접속합니다.

## 사용 방법

1. IP Address에 신호를 보낼 IP와 포트를 입력합니다.
2. 시작 버튼을 누르면 신호를 보내기 시작하고 응답으로 TCPA값과 안전한지 위험한지 알려줍니다.
3. 멈춤을 누르면 신호 보내는 것을 멈춥니다.
4. 다시 IP를 넣고 시작을 누르면 멈춘 시점 부터 다시 신호를 보내기 시작합니다.

## 구조 및 파일 설명

-   `sender.py`: Flask 애플리케이션의 진입점입니다.
-   `TCPA.py`: TCPA 모듈 파일입니다.

## 웹 페이지

![image](https://github.com/pupba/MealDemandForecasting/assets/53106728/310e59ba-a317-4de3-bd5f-ebbe271a1bbc)
