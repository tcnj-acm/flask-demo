from os.path import abspath, dirname
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextField

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = "secret"
db = SQLAlchemy(app)

#app.root_path = abspath(dirname(__file__))

class TextForm(FlaskForm):
    content = TextField("Content")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return 'Post Content: %r' % self.text

@app.route('/', methods = ['GET', 'POST'])
def main():
    form = TextForm(request.form)
    if request.method == 'POST':
        post = Post(text=form.content.data)
        db.session.add(post)
        db.session.commit()
        return redirect("/")
    return render_template('main.html', form=form, results=Post.query.all())
