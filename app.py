from flask import Flask, render_template, request
from deepface import DeepFace
import os
from datetime import datetime

# Flask 앱 초기화
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 업로드 폴더 없으면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 홈 페이지 라우트
@app.route('/')
def index():
    return render_template('index.html')

# 이미지 분석 라우트
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "이미지를 업로드하세요.", 400

    file = request.files['file']
    if file.filename == '':
        return "파일이 선택되지 않았습니다.", 400

    # 업로드 파일 저장
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}_{file.filename}")
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
        return f"분석 중 오류가 발생했습니다: {e}"

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
