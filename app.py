from flask import Flask, render_template
from models import initialize_database, Character, Weapon, Quest
from routes import blueprints
from peewee import fn, JOIN
from models import Weapon

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
    weapon_attribute_query = (
        Weapon
        .select(Weapon.attribute, fn.COUNT(Weapon.id).alias('attribute_count'))
        .group_by(Weapon.attribute)
    )

    weapon_counts = {
    result.attribute: result.attribute_count
    for result in weapon_attribute_query
    }

    sword_count = weapon_counts.get("剣", 0)
    tue_count = weapon_counts.get("杖", 0)


    return render_template('index.html', ranking=ranking,weapon_counts=weapon_counts,sword_count=sword_count,tue_count=tue_count)#test中

if __name__ == '__main__':
    app.run(port=8080, debug=True)
