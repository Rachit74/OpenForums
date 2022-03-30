from studyforums import *
from studyforums.models import *

@app.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@app.route('/home')
def home():
    questions = Question.query.all()
    return render_template("home.html", questions=questions)

@app.route('/ask', methods=["POST", "GET"])
def ask():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        author = current_user.username
        question = Question(title=title, content=content, author=author)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("ask.html")

@app.route('/ans/<int:id>', methods=["POST", "GET"])
def answer(id):
    question = Question.query.get_or_404(id)
    ans = request.form['content']
    author = current_user.username
    q_id = question.id
    ans = Answer(ans=ans, author=author, q_id=q_id)
    db.session.add(ans)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/delete_ans/<int:id>')
def delete_ans(id):
    ans = Answer.query.get_or_404(id)
    if ans.author == current_user.username or current_user.username == "admin":
        db.session.delete(ans)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return "You cannot delete this post | <a href='/home'> Home </a>"

@app.route('/post/<int:id>')
def question(id):
    question = Question.query.get_or_404(id)
    answers = Answer.query.all()
    return render_template("question.html", q=question, user=current_user.username, answers=answers)

