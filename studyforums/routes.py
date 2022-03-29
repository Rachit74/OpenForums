from studyforums import *
from studyforums.models import *
from studyforums.forms import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@app.route('/home')
@login_required
def home():
    questions = Question.query.all()
    return render_template("home.html", questions=questions)

@app.route('/ask', methods=["POST", "GET"])
@login_required
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

@app.route('/question/<int:id>')
@login_required
def question(id):
    question = Question.query.get_or_404(id)
    answers = Answer.query.all()
    return render_template("question.html", q=question, user=current_user.username, answers=answers)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))

        return render_template('login.html', err="Invalid credentials! Please try again.", form=form)
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))