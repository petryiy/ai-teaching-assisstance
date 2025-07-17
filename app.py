from flask import Flask, render_template, request
import vertexai
import os
from vertexai.preview.generative_models import GenerativeModel


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"


vertexai.init(project="teaching-466210", location="us-central1")


model = GenerativeModel("gemini-2.0-flash-001")


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    content = request.form['textbook']
    prompt = f"""
你是一位英语老师，以下是学生提交的英语教材内容：
"{content}"
请你完成两个任务：
1. 根据所给内容，提炼总结出语法点和关键词汇；
2. 根据这些要点生成5道多项选择题 （题干+选项+A~D+正确答案）。

请以以下格式输出：
【语法要点】
...
【词汇重点】
...
【题目1】
题干...
A. ...
B. ...
C. ...
D. ...
答案：...
（依此类推生成五题）
"""

    try:
        response = model.generate_content(prompt)
        result = response.text
        return render_template('result.html', output=result)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
