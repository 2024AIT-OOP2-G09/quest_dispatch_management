from flask import Flask, render_template
from models import initialize_database, Character, Weapon, Quest
from routes import blueprints
from peewee import fn, JOIN

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)


# ホームページのルート
@app.route('/')
def index():
    # キャラクターのランキング取得
    ranking_query = (
        Character
        .select(Character, fn.COUNT(Quest.id).alias('quest_count'))
        .join(Quest, JOIN.LEFT_OUTER, on=(Quest.character == Character.id))
        .group_by(Character)
        .order_by(fn.COUNT(Quest.id).desc())
    )
    # ranking_query は既にイテラブルなので、そのまま使用
    ranking = ranking_query  # クエリ結果はそのまま使用

    # 武器属性ごとのカウント取得
    weapon_attribute_query = (
        Weapon
        .select(Weapon.attribute, fn.COUNT(Weapon.id).alias('attribute_count'))
        .group_by(Weapon.attribute)
    )

    weapon_counts = {
        result.attribute: result.attribute_count
        for result in weapon_attribute_query
    }

    # 特定の武器のカウント
    sword_count = weapon_counts.get("剣", 0)
    tue_count = weapon_counts.get("杖", 0)

    # 剣と杖の比率計算（ゼロ除算回避）
    total_weapons = sword_count + tue_count
    sword_ratio = sword_count / total_weapons if total_weapons > 0 else 0
    tue_ratio = tue_count / total_weapons if total_weapons > 0 else 0

    # `ranking` が空の場合はデフォルト値を設定
    if not ranking:
        ranking = [{'name': 'デフォルトキャラクター', 'quest_count': 0}]

    # 女性キャラクター数のカウント（仮定）
    female_count = Character.select().where(Character.gender == '女性').count()

    # 総キャラクター数
    total_count = len(ranking)

    # 男性キャラクター数のカウント（仮定）
    male_count = Character.select().where(Character.gender == '男性').count()

    # その他のキャラクター数の計算
    other_count = Character.select().where(Character.gender == 'その他').count()

    # 男性と女性の割合を計算
    male_percentage = male_count / total_count if total_count > 0 else 0
    female_percentage = female_count / total_count if total_count > 0 else 0

    return render_template(
        'index.html',
        ranking=ranking,
        weapon_counts=weapon_counts,
        sword_count=sword_count,
        tue_count=tue_count,
        sword_ratio=sword_ratio,
        tue_ratio=tue_ratio,
        male_count=male_count, 
        female_count=female_count,
        male_percentage=male_percentage,
        female_percentage=female_percentage,
        other_count=other_count  
    )

if __name__ == '__main__':
    app.run(port=8080, debug=True)