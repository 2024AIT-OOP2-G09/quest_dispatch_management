from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from peewee import fn, JOIN
from models import Character, Quest

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    ranking = (
        Character
        .select(Character, fn.COUNT(Quest.id).alias('quest_count'))
        .join(Quest, JOIN.LEFT_OUTER, on=(Quest.character == Character.id))
        .group_by(Character)
        .order_by(fn.COUNT(Quest.id).desc())
    )
    return render_template('index.html', ranking=ranking)#test中

if __name__ == '__main__':
    app.run(port=8080, debug=True)
