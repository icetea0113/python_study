from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import subprocess
from subprocess import TimeoutExpired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'dawqlkebfawlhj_1o9i823t78dACFNAWIDB_sdekfjbik'  # Set a secret key for securely signing the session

ALLOWED_NAMES = ['superuser_test', '이상헌', '양동헌', '조철민', '김장우', '서지민']
START_TIME = datetime(2023, 12, 16, 12, 0)  # Submission start time
END_TIME = datetime(2023, 12, 22, 23, 59)   # Submission end time
student_scores = {name: 0 for name in ALLOWED_NAMES}

# Set the path for the uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Flask-Login 설정
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/myapp/mydatabase.db'  # 예시 URI, 실제 경로 설정 필요
db = SQLAlchemy(app)

class StudentScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<StudentScore {self.name}>'



@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# 점수 업데이트 로직
def update_student_score(name, score):
    student_score = StudentScore.query.filter_by(name=name).first()
    if student_score:
        student_score.score += score
    else:
        student_score = StudentScore(name=name, score=score)
        db.session.add(student_score)
    db.session.commit()

# 관리자 페이지에서 점수 보기
@app.route('/admin/scores')
@login_required
def admin_scores():
    scores = StudentScore.query.all()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Student Scores</title>
        </head>
        <body>
            <h2>Student Scores</h2>
            <table>
                <tr>
                    <th>Student Name</th>
                    <th>Score</th>
                </tr>
                {% for student in scores %}
                <tr>
                    <td>{{ student.name }}</td>
                    <td>{{ student.score }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
    ''')

# 최초 실행 시 데이터베이스 테이블 생성
@app.before_first_request
def initialize_database():
    db.create_all()

# 관리자 계정 클래스
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

class StudentScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)

# 관리자 인증
@login_manager.user_loader
def load_user(user_id):
    if user_id == '1':
        return Admin()
    return None

# 관리자 로그인 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '이희근' and password == 'androi3810!':  # 간단한 예시, 실제 사용시 보안 강화 필요
            admin = Admin.query.get(1) or Admin(id=1)
            db.session.add(admin)
            db.session.commit()
            login_user(admin)
            return redirect(url_for('admin_scores'))
    return render_template_string('''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

# 관리자 로그아웃 라우트
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin/scores')
@login_required
def admin_scores():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Student Scores</title>
        </head>
        <body>
            <h2>Student Scores</h2>
            <table>
                <tr>
                    <th>Student Name</th>
                    <th>Score</th>
                </tr>
                {% for name, score in student_scores.items() %}
                <tr>
                    <td>{{ name }}</td>
                    <td>{{ score }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
    ''', student_scores=student_scores)

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'py'}

# Maximum allowed code length
MAX_CODE_LENGTH = 3000  # 3000 bytes
MAX_CODE_LENGTH_SEO_JI_MIN = 1500  # 1500 bytes for 서지민

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Check code length
def check_code_length(code):
    return len(code)

@app.route('/', methods=['GET', 'POST'])
def home():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        if username not in ALLOWED_NAMES:
            error_message = "Invalid name. Please enter a valid name."
        else:
            session['username'] = username
            return redirect(url_for('submit'))
    
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Home - Enter Your Name</title>
            <script>
                function validateForm() {
                    var name = document.forms["nameForm"]["username"].value;
                    if (!["이상헌", "양동헌", "조철민", "김장우", "서지민"].includes(name)) {
                        alert("Invalid name. Please enter a valid name.");
                        return false;
                    }
                    return true;
                }
            </script>
        </head>
        <body>
            <h2>Enter your name to submit a problem</h2>
            <form name="nameForm" method="post" onsubmit="return validateForm()">
                Your Name: <input type="text" name="username"><br>
                <input type="submit" value="Go to Submission">
            </form>
            {% if error_message %}
                <script>alert("{{ error_message }}");</script>
            {% endif %}
        </body>
        </html>
    ''', error_message=error_message)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('home'))

    username = session['username']
    if not (START_TIME <= datetime.now() <= END_TIME):
        return "Submission is closed. Please submit between {} and {}.".format(START_TIME, END_TIME)

    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return "No file selected"
        
        # Read the code content
        code_content = file.read()
        file.seek(0)
        # Check code length based on the user
        max_code_length = MAX_CODE_LENGTH
        if username == '서지민':
            max_code_length = MAX_CODE_LENGTH_SEO_JI_MIN

        if check_code_length(code_content) > max_code_length:
            return f"Code length exceeds the maximum limit of {max_code_length} bytes"

        filename = secure_filename(file.filename)
        script_path = os.path.join(app.config['UPLOAD_FOLDER'], username, filename)

        os.makedirs(os.path.dirname(script_path), exist_ok=True)  # Create user folder if not exists
        file.save(script_path)

        session['script_path'] = script_path
        return redirect(url_for('grading_results'))

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Submit Your Python Script</title>
        </head>
        <body>
            <h2>Submit your Python script</h2>
            <form action="{{ url_for('submit') }}" method="post" enctype="multipart/form-data">
                <input type="file" name="file"><br><br>
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
    ''')

    # GET 요청에 대한 응답
    return '''
        <html>
            <head>
                <title>Submit File</title>
            </head>
            <body>
                <h2>Submit your Python script</h2>
                <form action="" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>
    '''


def run_python_script(script_path, input_path, time_limit=1):
    try:
        start_time = datetime.now()  # 스크립트 실행 전 시간 기록
        with open(input_path, 'r') as input_file:
            process = subprocess.run(
                ['python', script_path],
                stdin=input_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=time_limit
            )
        end_time = datetime.now()  # 스크립트 실행 후 시간 기록
        execution_time = end_time - start_time  # 실행 시간 계산
        return process.stdout.strip(), None, execution_time
    except TimeoutExpired:
        return None, "Time limit exceeded"

@app.route('/grading-results', methods=['GET'])
def grading_results():
    script_path = session.get('script_path')
    if not script_path:
        return redirect(url_for('home'))

    grading_details = []
    total_score = 0

    input_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'input')
    output_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'output')

    for input_file in os.listdir(input_folder):
        if input_file.endswith('.inp'):
            file_number = int(input_file.split('.')[0])
            file_score = 6 if 1 <= file_number <= 10 else 8 if 11 <= file_number <= 15 else 0

            input_path = os.path.join(input_folder, input_file)
            output_path = os.path.join(output_folder, input_file.replace('.inp', '.out'))

            script_output, error, execution_time = run_python_script(script_path, input_path)

            execution_time_seconds = execution_time.total_seconds() if execution_time else None
            execution_time_str = f"{execution_time_seconds:.2f} s" if execution_time_seconds is not None else 'Timeout'
            with open(output_path, 'r') as file:
                expected_output = file.read().strip()

            is_correct = script_output == expected_output
            score = file_score if is_correct else 0
            total_score += score

            grading_details.append({
                'number': file_number,
                'time': execution_time_str,
                'score': score
            })

    # 채점 결과를 표시하는 페이지 렌더링
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Grading Results</title>
        </head>
        <body>
            <h2>Grading Results</h2>
            <table border="1">
                <tr>
                    <th>Problem Number</th>
                    <th>Time Taken</th>
                    <th>Score</th>
                </tr>
                {% for detail in grading_details %}
                    <tr>
                        <td>{{ detail.number }}</td>
                        <td>{{ detail.time }}</td>
                        <td>{{ detail.score }}</td>
                    </tr>
                {% endfor %}
            </table>
            <p><strong>Total Score:</strong> {{ total_score }}</p>
        </body>
        </html>
    ''', grading_details=grading_details, total_score=total_score)

# 기존 함수들...


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
