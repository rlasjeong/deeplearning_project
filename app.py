from flask import Flask, render_template, request, redirect, url_for
from deepface import DeepFace
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 업로드 폴더 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')  # 안전하게 가져오기
    if not file or file.filename == '':
        return redirect(url_for('index'))  # 파일 없으면 홈으로

    # 파일 이름에 공백이나 한글 문제 방지
    filename = file.filename.replace(" ", "_")
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}_{filename}")
    file.save(filepath)

    try:
        # DeepFace 분석
        result = DeepFace.analyze(
            img_path=filepath,
            actions=['emotion', 'age', 'gender'],
            enforce_detection=False
        )

        analysis = {
            'emotion': result[0]['dominant_emotion'],
            'age': result[0]['age'],
            'gender': result[0]['gender']
        }

        return render_template('result.html', result=analysis, image_path=filepath)

    except Exception as e:
        # 에러 발생 시 홈으로 돌아가면서 에러 메시지 출력
        return f"분석 중 오류가 발생했습니다: {e}<br><a href='/'>홈으로 돌아가기</a>"

if __name__ == '__main__':
    # 호스트를 0.0.0.0으로 지정하면 외부 접속도 가능
    app.run(debug=True, host='0.0.0.0', port=5000)
