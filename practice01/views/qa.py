from flask import Blueprint, request, render_template, g, redirect

from ORM.forms import QuestionForm, AnswerForm
from practice01.decorators import login_required
from config.extends import db
from ORM.models import Question, Answer

bp = Blueprint('qa', __name__, url_prefix='/qa')


@bp.route('/')
def hello_world():
    return redirect('/')


@bp.route('/publish', methods=['GET', 'POST'])
@login_required
def publish_qa():
    if request.method == 'GET':
        return render_template('publish_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = Question(title=title, content=content, author_id=g.user.id)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            print(form.errors)
            return redirect('/qa/publish')

@bp.route('/qa_detail/<question_id>', methods=['GET', 'POST'])
def qa_detail(question_id):
    question = Question.query.get(question_id)
    return render_template('detail.html', question=question)


@bp.post('/publish_answer')
@login_required
def publish_answer():
    form = AnswerForm(request.form)
    if form.validate():
        question_id = form.question_id.data
        content = form.content.data
        answer = Answer(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(f"/qa/qa_detail/{question_id}")
    else:
        print(form.errors)
        return redirect(f"/qa/qa_detail/{request.form.get('question_id')}")


@bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('q')
    questions = Question.query.filter(Question.title.contains(keyword)).all()
    return render_template("index.html", questions=questions)
