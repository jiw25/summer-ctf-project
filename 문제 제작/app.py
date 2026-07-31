import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)

# 관리자 백업 파일 생성
with open("admin_password_backup.txt", "w", encoding="utf-8") as f:
    f.write("admin:SuperSecret_Hacker_PW_999")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        host = request.form.get('host', '')
        
        # 특수문자 차단 (파일 덮어쓰기, 와일드카드 우회, 파이프라인 방지)
        forbidden_chars = ['>', '<', '|', '*', '?', '`', '$', ';']
        for char in forbidden_chars:
            if char in host:
                return render_template('index.html', data=f'[Security Alert] 해킹 시도 차단: 허용되지 않은 특수문자 ( {char} )', cmd='Blocked')

        # 서버 파괴 및 소스코드 유출 키워드 차단
        blacklist = ['del', 'rm', 'echo', 'mkdir', 'app.py', 'index.html', 'python', 'powershell']
        for word in blacklist:
            if word in host.lower():
                return render_template('index.html', data=f'[Security Alert] 해킹 시도 차단: 허용되지 않은 명령어/파일 ( {word} )', cmd='Blocked')
        
        # 윈도우 핑 명령어(-n)
        cmd = f'ping -n 3 {host}'
        
        try:
            output = subprocess.check_output(cmd, shell=True, timeout=5, stderr=subprocess.STDOUT)
            result_text = output.decode('cp949', errors='ignore')
            return render_template('index.html', data=result_text, cmd=cmd)
            
        except subprocess.TimeoutExpired:
            return render_template('index.html', data='Timeout! 서버 응답 지연.', cmd=cmd)
            
        except subprocess.CalledProcessError as e:
            result_text = e.output.decode('cp949', errors='ignore')
            return render_template('index.html', data=result_text, cmd=cmd)
            
        except Exception as e:
            return render_template('index.html', data=f'System Error: {e}', cmd=cmd)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
