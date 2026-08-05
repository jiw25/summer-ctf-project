from flask import Flask, render_template, request, render_template_string, session, redirect, url_for
import subprocess
import re

app = Flask(__name__)
app.secret_key = 'siss_secret_key_for_session_1234'

#  CmdI 방어용 블랙리스트
BLACKLIST = ['>', '<', '|', '*', '?', ';', 'rm', 'echo', 'app.py']
#  Ping 서비스 (Command Injection)

@app.route('/', methods=['GET', 'POST'])
def index():
    result_data = ""
    cmd_text = "" # 화면에 띄워줄 명령어 문자열
    
    if request.method == 'POST':
        host = request.form.get('host', '')
        cmd_text = f'ping -c 3 {host}'
        
        # 1단계: 블랙리스트 필터링
        for word in BLACKLIST:
            if word in host:
                return render_template('index.html', data="[경고] 허용되지 않은 특수문자 또는 명령어가 포함되어 있습니다.", cmd=cmd_text)
                
        # 2단계: Ping 명령어 실행
        try:
            output = subprocess.check_output(cmd_text, shell=True, stderr=subprocess.STDOUT)
            result_data = output.decode('utf-8', errors='ignore')
        except subprocess.CalledProcessError as e:
            result_data = e.output.decode('utf-8', errors='ignore')
    return render_template('index.html', data=result_data, cmd=cmd_text)


#  관리자 로그인

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1주차 CmdI를 통해 알아내야 하는 관리자 비밀번호
        if username == 'admin' and password == 'SuperSecret_Hacker_PW_999':
            session['logged_in'] = True  # 로그인 성공 도장 쾅!
            return redirect(url_for('dashboard')) # 대시보드로 이동
        else:
            return render_template('login.html', error="아이디 또는 비밀번호가 틀렸습니다.")
            
    return render_template('login.html')

# 관리자 대시보드 (SSTI 취약점 발생 구역!)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
   
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('dashboard.html')

    # POST 요청: 닉네임 설정 폼 제출 시
    nickname = request.form.get('nickname', 'Admin')
    template = f'''
    <!DOCTYPE html>
    <html lang="ko">
    <head><title>대시보드 결과</title></head>
    <body>
        <h2>관리자 대시보드</h2>
        <hr>
        <h3>닉네임이 성공적으로 반영되었습니다:</h3>
        <p style="color: blue; font-size: 20px;">{nickname}</p>
        <br>
        <a href="/dashboard">뒤로 가기</a>
    </body>
    </html>
    '''
    return render_template_string(template)

# 테스트용 로그아웃
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
