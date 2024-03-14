from flask import Flask, jsonify
from flask_cors import CORS
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash
import os

from datetime import datetime
import pytz


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog2.db'

# 暗号化
app.config['SECRET_KEY'] = os.urandom(24)

# LoginManager()　ログインするのに必要な機能をインスタンス化
login_manager = LoginManager()
# 紐付け
login_manager.init_app(app)

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now(pytz.timezone('Asia/Tokyo')))
    
# UserMixin ログインに必要な機能を持たせたクラス テーブルを作成
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),  unique=True)
    password = db.Column(db.String(12))


# 投稿を取得
@app.route('/posts', methods=['GET'])
@login_required
def index():
    posts = Post.query.all()
    posts_data = [{'id': post.id,'title': post.title, 'body': post.body} for post in posts]
    return jsonify(posts_data)


# 個々の投稿を取得
@app.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id) 
    post_data = {'id': post.id, 'title': post.title, 'body': post.body}
    return jsonify(post_data)


# 投稿を作成
@app.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        body = data.get('body')

        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()

        return jsonify({"message": "成功しました"})
    

# 投稿を修正する
@app.route('/<int:id>/update', methods=['GET','POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        post_data = {'title':post.title, 'body':post.body}
        return jsonify({"message": "成功しました", "post":post_data})
    else:
        data = request.get_json()
        print(data)
        # 上書きしている
        post.title = data.get('title')
        post.body = data.get('body')

        # アップデートする時はコミットすれば良いだけ
        db.session.commit()
        return jsonify({"message": "アップデート成功"}), 200
    

# 投稿を削除する
@app.route('/<int:id>/delete', methods=['DELETE'])
@login_required
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "削除成功"}), 200


# 新規登録
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User(username=username, password=generate_password_hash(
            password, method='pbkdf2:sha256'))

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "新規登録成功"}), 200
    else:
        return jsonify({"message": "新規登録失敗"}), 400

# sessionからユーザー情報読みこむのに書かなければならない
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ログイン
@app.route('/login', methods=['GET', 'POST'])
# getとpostを受け付ける
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # firstは一番最初の値を取ってくる
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"message": "ログイン成功"}), 200
    else:
        return jsonify({"message": "ログイン失敗"}), 400
    
# ログアウト
@app.route('/logout')
# ログインしていないとできない
@login_required
def logout():
    logout_user()
    return jsonify({"message": "ログイン成功"}), 200

# Members API Route
# @app.route("/members")
# def members():
#     return {"members": ["Member1", "Member2", "Member3"]}

# デバックモードを　ONにする 
if __name__ == "__main__":
    app.run(debug=True,port=8888)
