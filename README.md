

```markdown
# 중앙 도서관 시스템 (CTF Web Challenge)

평범한 도서 검색 시스템처럼 보이지만, 백엔드에서 쉘 명령어가 돌아가고 있는 취약한 웹 서비스
Command Injection부터 Stored SSTI까지 단계별로 연계되는 시나리오형 웹 문제

## 🎯 풀이 시나리오 (Intended)
1. **Command Injection**: 메인 페이지 도서 검색(ping) 기능에서 필터링을 우회해 `admin_password.txt` 탈취
2. **Admin Login**: 획득한 사서 비밀번호로 `/login` 에 접속해 세션 획득
3. **Stored SSTI**: 관리자 권한으로 열리는 도서 상세 페이지의 '줄거리 수정' 기능에서 Jinja2 템플릿 인젝션을 트리거하여 서버의 `flag.txt` 읽기

## 🛠 Tech Stack
- Backend: Python, Flask
- Frontend: HTML/CSS (Jinja2)

## 🚀 How to Run (Local Test)
```bash
# 의존성 설치
pip install flask markupsafe

# 서버 실행 ([http://127.0.0.1:8000](http://127.0.0.1:8000))
python app.py

```

*(참고: 최종 배포용 Dockerfile은 리눅스 환경 기준으로 작성 예정)*

## 📝 Dev Log & Patch Notes

**[최근 업데이트: 2026.08.15]**

* **언인텐(Unintended) 숏컷 차단**
* 문제점: 커맨드 인젝션 취약점이 터질 때, 참가자가 관리자 계정을 안 캐고 다이렉트로 `cat flag.txt`를 때려버리는 숏컷 발생.
* 조치: WAF 블랙리스트 룰셋에 `flag` 키워드 추가. 무조건 `admin_password.txt`부터 읽고 정석 루트를 타도록 강제함.


* **SSTI 기믹 고도화 (Stored 방식으로 변경)**
* 기존에는 줄거리를 수정해도 임시 렌더링만 되고 데이터가 날아가서 몰입도가 떨어졌음.
* POST 요청 시 수정된 페이로드가 서버 메모리(`BOOKS` 딕셔너리)에 실제로 반영되도록 로직 수정. 완전한 **Stored SSTI**로 퀄리티 업그레이드.
* 프론트엔드 쪽에 편집 모드 토글 버튼 추가 및 CSS UI 개선.


* **사이드 이펙트 및 기타 취약점 점검**
* SQLi: DB 연동 없이 파이썬 객체로 관리되므로 원천 차단됨.
* XSS / CSS Injection: jinja 템플릿에서 `escape()` 처리 및 로그인 폼 반환 로직 확인 결과 안전함.
* 세션 위조: `os.urandom(24)` 사용으로 강제 세션 생성 불가 확인.



## 📌 TODO

* [ ] 문제 배포용 `Dockerfile` 및 `docker-compose.yml` 작성 (Ubuntu 베이스)
* [ ] 컨테이너 내부에 `flag.txt` 및 `admin_password.txt` 권한 세팅 (www-data)
* [ ] 공식 Write-up 작성

```

```
