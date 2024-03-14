flask-react
環境構築
python3 -m venv venv
↑仮想環境を作成(venvという名のディレクトリを作成)

source venv/bin/activate
↑アクティブ化

その中で、
pip3 install Flask

サーバー起動
python3 app.py 

クライアントのpackege.jsonにプロキシを追加
"proxy": "http://localhost:5000",

react作成
npx create-react-app client
npm start![image](https://github.com/Yasuda1127/flask-react-blog/assets/116235027/270697c2-dae1-4970-ab51-c802d76aa829)
