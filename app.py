from flask import *
from flask_sqlalchemy import SQLAlchemy # install flask-sqlalchmy and import before create database
from flask_login import LoginManager,login_user,UserMixin,logout_user # also use *
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///mydb.db"
app.config[ 'SECRET_KEY']= 'thisissecrete'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(100),  nullable=False)
    lname = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(80),  nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username


class Blog(db.Model):        
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),  nullable=False)
    author = db.Column(db.String(100),  nullable=False)
    content = db.Column(db.Text(),  nullable=False)
    pub_date = db.Column(db.DateTime(),  nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return '<Blogfr %r>' % self.title



@login_manager.user_loader # for login user
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    data = Blog.query.all()
    return render_template("index.html",data=data)

@app.route("/main")
def main():
    return render_template ("main.html")
    
@app.route("/register",methods=['GET','POST'])
def register():
    
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        user = User(
            username=username,
            email=email,
            fname=fname,
            lname=lname,
            password=password,
            )
        db.session.add(user)
        db.session.commit()
        flash('User Has Been Registered Successfully','success') # show message
        return redirect ('/login')

    return render_template ("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user=User.query.filter_by(username=username).first()    
        if user and password==user.password:
            login_user(user)
            return redirect('/')

        else:
            flash('Invalid Credentials','danger')
            return redirect('/login')    

    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route("/blogpost",methods=['GET','POST'])
def blogpost():             # create
    if request.method=="POST":
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        
        blog = Blog(
            title = title,
            author = author,
            content = content
        )
        db.session.add(blog)
        db.session.commit()
        flash("Your Post Has Been Submitted Successfully",'success')
        return redirect('/')

    return render_template('blog.html')


@app.route("/blog_detail/<int:id>") # id comes from index.html
def blog_details(id):       # read/retrive
    blog = Blog.query.filter_by(blog_id=id).first()
    return render_template('blog_details.html',blog=blog)

@app.route("/delete/<int:id>",methods=['GET','POST']) # id comes from blog_details.html
def delete_post(id):         # delete
    blog = Blog.query.filter_by(blog_id=id).first()
    db.session.delete(blog)
    db.session.commit()
    flash('Post Has Been Deleted','success')
    return redirect('/')


@app.route("/edit/<int:id>",methods=['GET','POST']) # id comes from blog_details.html
def edit_post(id):         # edit
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        
        blog = Blog.query.filter_by(blog_id=id).first()
       
        blog.title = title
        blog.author = author
        blog.content = content
        db.session.add(blog)
        db.session.commit()

        flash('Post Has Been Updated','success')
        return redirect('/')

    blog = Blog.query.filter_by(blog_id=id).first()    
    return render_template('edit.html',blog=blog)





@app.cli.command("create-db") # use for create mydb.db
def create_db():
    __init_db()

def __init_db():
    db.create_all()
  


if __name__ == "__main__":
    app.run(debug=True)    



#     with app.app_context() as ctx: 
# ...    usr= User.query.all()  