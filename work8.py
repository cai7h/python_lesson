# main.py：添加安全初始化，不会破坏现有数据
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from peewee import Model, CharField, IntegerField, ForeignKeyField, MySQLDatabase
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder='work8')
app.secret_key = 'super-secret-key'

db =MySQLDatabase(
    database='python_lesson',
    user='root',
    password='Cqh051213',
    host='localhost',
    port=3306,
    charset='utf8mb4'
)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class BaseModel(Model):
    class Meta:
        database = db

class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    password_hash = CharField()

class DoubanMovie(BaseModel):
    title = CharField()
    year = IntegerField()

    class Meta:
        table_name = 'douban_movie'  # ✅ 显式指定使用已有的表名

class Collection(BaseModel):
    user = ForeignKeyField(User, backref='collections')
    movie = ForeignKeyField(DoubanMovie)

@login_manager.user_loader 
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))

@app.route('/')
@login_required
def home():
    return render_template('welcome.html', username=current_user.username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.get_or_none(User.username == username):
            return render_template('register.html', error='用户名已存在')
        User.create(username=username, password_hash=generate_password_hash(password))
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_or_none(User.username == username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', error='用户名或密码错误')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    movies = []
    query_year = ''
    if request.method == 'POST':
        year = request.form['year']
        query_year = year
        if year.isdigit():
            year_int = int(year)
            print(f"🧪 查询年份：{year_int}")

            all_years = [m.year for m in DoubanMovie.select()]
            print("📅 数据库所有年份：", sorted(set(all_years)))

            movies = DoubanMovie.select().where(DoubanMovie.year == year_int)
            print(f"🔍 查询到电影数量：{len(movies)}")
            for m in movies:
                print(f"👉 {m.title} ({m.year})")

    return render_template('search.html', movies=movies, year=query_year)

@app.route('/collect/<int:movie_id>', methods=['POST'])
@login_required
def collect(movie_id):
    movie = DoubanMovie.get_or_none(DoubanMovie.id == movie_id)
    if movie:
        Collection.get_or_create(user=current_user.id, movie=movie_id)
    return redirect(url_for('my_collection'))

@app.route('/my_collection')
@login_required
def my_collection():
    collections = Collection.select().where(Collection.user == current_user.id)
    return render_template('collection.html', collections=collections)

@app.route('/debug_movies')
def debug_movies():
    all_movies = DoubanMovie.select()
    for m in all_movies:
        print(f"🎬 {m.title} ({m.year})")
    return f"共找到 {len(all_movies)} 部电影"

@app.route('/debug_info')
def debug_info():
    rows = db.execute_sql("SELECT COUNT(*) FROM douban_movie").fetchone()
    return f"✅ 当前连接数据库中共有 {rows[0]} 部电影"

if __name__ == '__main__':
    db.connect()
    db.create_tables([User, DoubanMovie, Collection], safe=True)
    app.run(debug=True)