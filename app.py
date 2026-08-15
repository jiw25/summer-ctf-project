from flask import Flask, render_template, request, render_template_string, session, redirect, url_for, jsonify
from markupsafe import escape 
import subprocess
import random
import os  

app = Flask(__name__)

app.secret_key = os.urandom(24)


BLACKLIST = ['>', '<', '|', '*', '?', ';', 'rm', 'echo', 'app.py', 'flag']


BOOKS = [
    {"id": 1, "title": "클린 코드", "author": "로버트 C. 마틴", "call_num": "005.13-M", "img": "https://covers.openlibrary.org/b/isbn/9780132350884-M.jpg", "story": "코드를 읽기 쉽고 유지보수하기 좋게 작성하는 기술과 장인 정신에 대해 다룹니다."},
    {"id": 2, "title": "실용주의 프로그래머", "author": "데이비드 토머스", "call_num": "005.1-T", "img": "https://covers.openlibrary.org/b/isbn/9780135957059-M.jpg", "story": "더 나은 프로그래머가 되기 위한 철학과 실천 방법을 제시하는 현대의 고전입니다."},
    {"id": 3, "title": "C 프로그래밍 언어", "author": "브라이언 커니핸", "call_num": "005.133-K", "img": "https://covers.openlibrary.org/b/isbn/9780131103627-M.jpg", "story": "C 언어의 창시자가 직접 쓴, 모든 프로그래밍 언어 책의 근본이 되는 바이블입니다."},
    {"id": 4, "title": "리팩터링", "author": "마틴 파울러", "call_num": "005.14-F", "img": "https://covers.openlibrary.org/b/isbn/9780201485677-M.jpg", "story": "소프트웨어의 겉보기 동작은 그대로 유지한 채, 코드를 이해하고 수정하기 쉽도록 내부 구조를 변경하는 기법입니다."},
    {"id": 5, "title": "디자인 패턴", "author": "에릭 감마", "call_num": "005.11-G", "img": "https://covers.openlibrary.org/b/isbn/9780201633610-M.jpg", "story": "객체 지향 소프트웨어 설계에서 반복적으로 발생하는 문제들을 해결하기 위한 23가지 패턴을 정리했습니다."},
    {"id": 6, "title": "해커의 기쁨", "author": "헨리 S. 워렌", "call_num": "004.16-W", "img": "https://covers.openlibrary.org/b/isbn/9780201914658-M.jpg", "story": "비트 조작과 최적화의 마법 같은 트릭들을 모아둔 책입니다."},
    {"id": 7, "title": "해킹: 공격의 예술", "author": "존 에릭슨", "call_num": "004.5-E", "img": "https://covers.openlibrary.org/b/isbn/9781593271442-M.jpg", "story": "해킹의 근본적인 원리와 기술을 C 언어 디버깅과 메모리 분석을 통해 깊이 있게 파헤칩니다."},
    {"id": 8, "title": "소프트웨어 장인", "author": "산드로 만쿠소", "call_num": "005.1-M", "img": "https://covers.openlibrary.org/b/isbn/9780134011244-M.jpg", "story": "단순히 코드를 짜는 것을 넘어, 프로페셔널한 소프트웨어 개발자로서의 태도와 가치관을 다룹니다."},
    {"id": 9, "title": "엔터프라이즈 아키텍처", "author": "마틴 파울러", "call_num": "005.3-P", "img": "https://covers.openlibrary.org/b/isbn/9780321127426-M.jpg", "story": "복잡한 기업용 애플리케이션을 구축할 때 필요한 아키텍처 패턴들을 총망라했습니다."},
    {"id": 10, "title": "[긴급] 서버 마이그레이션 백업", "author": "System Admin", "call_num": "", "img": "https://via.placeholder.com/150x220/1e293b/ef4444?text=TOP+SECRET", "story": "경고: 이 데이터는 시스템 백업 파일입니다. 검색 엔진(Ping)을 통해서만 파일 시스템 내역을 조회할 수 있습니다. 열람 불가."}
]

# ========================================================
# 1. 도서 검색 페이지
# ========================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    result_data = ""
    recommended_books = random.sample(BOOKS, 3)
    
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        
        for word in BLACKLIST:
            if word in keyword:
                return render_template('index.html', data="[WAF 방화벽] 비정상적인 특수문자 또는 명령어가 감지되었습니다.", recommended_books=recommended_books)
                
        if '&' in keyword:
            cmd_text = f'ping -c 1 {keyword}'
            try:
                output = subprocess.check_output(cmd_text, shell=True, stderr=subprocess.STDOUT)
                result_data = output.decode('utf-8', errors='ignore')
            except subprocess.CalledProcessError as e:
                result_data = e.output.decode('utf-8', errors='ignore')
        else:
            search_hits = [b for b in BOOKS if keyword.lower() in b['title'].lower() or keyword.lower() in b['author'].lower() or keyword.lower() in b['call_num'].lower()]
            
            if search_hits:
              
                hit_titles = ", ".join([f"<a href='/detail/{b['id']}' style='color:#2563eb; font-weight:bold; text-decoration:underline;'>『{b['title']}』</a>" for b in search_hits])
                result_data = f"[시스템 안내] 검색하신 키워드로 {hit_titles} 도서가 발견되었습니다."
            else:
            
                result_data = f"[시스템 안내] '{escape(keyword)}'에 대한 도서를 찾을 수 없습니다."

    return render_template('index.html', data=result_data, recommended_books=recommended_books)

@app.route('/api/recommend')
def api_recommend():
    return jsonify(random.sample(BOOKS, 3))

# ========================================================
# 2. 관리자 로그인 페이지
# ========================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'Librarian_Secret_007':
            session['role'] = 'admin'
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="사서 인증에 실패했습니다.")
            
    return render_template('login.html')

# ========================================================
# 3. 도서 상세 페이지
# ========================================================
@app.route('/detail/<int:book_id>', methods=['GET', 'POST'])
def detail(book_id):
    target_book = next((b for b in BOOKS if b['id'] == book_id), None)
    if not target_book:
        return "도서를 찾을 수 없습니다.", 404
    if request.method == 'POST':
        if session.get('role') != 'admin':
            return "권한이 없습니다."
            
        new_story = request.form.get('story', '')
        target_book['story'] = new_story
        return redirect(url_for('detail', book_id=book_id))

    try:
        rendered_story = render_template_string(target_book['story'])
    except Exception as e:
        rendered_story = f"<span style='color:red;'>[템플릿 렌더링 오류] {e}</span>"
    return render_template('detail.html', book=target_book, rendered_story=rendered_story)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8000, debug=False)

