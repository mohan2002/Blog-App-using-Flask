from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(20), nullable=False,default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self) -> str:
        return 'Blog post' + str(self.id)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts',methods=['GET','POST'])
def posts():
    all_post = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html',posts=all_post)



@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('Edit.html',post=post)



@app.route('/addpost',methods=['GET','POST'])
def addpost():
    if request.method == 'POST':
        post_title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_post = BlogPost(title=post_title,content=content,author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('Newpost.html')

# @app.route('/')
@app.route('/home/<string:name>/<int:id>')
def hello(name,id):
    return "Hello " + name + " " + str(id)


#limiting:

@app.route('/onlyget',methods=['GET'])
def get_req():
    return "You can only get this webpage"


if __name__ == "__main__":
    app.run(debug=True)

