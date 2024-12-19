from flask import Blueprint, render_template, request, redirect, url_for
from models import Character

# Blueprintの作成
character_bp = Blueprint('character', __name__, url_prefix='/characters')

@character_bp.route('/')
def list():
    # データ取得
    characters = Character.select()

    # 性別ごとの人数をカウント
    male_count = characters.where(Character.gender == '男子').count()
    female_count = characters.where(Character.gender == '女子').count()
    other_count = characters.where(Character.gender != '男子', Character.gender != '女子').count()

    # 総数を計算
    total_count = male_count + female_count + other_count

    return render_template('index.html', title='キャラクター一覧', items=characters,
                            male_count=male_count, female_count=female_count, other_count=other_count,
                            total_count=total_count)



@character_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        Character.create(name=name, gender=gender)
        return redirect(url_for('character.list'))
    
    return render_template('character_add.html')


@character_bp.route('/edit/<int:character_id>', methods=['GET', 'POST'])
def edit(character_id):
    character = Character.get_or_none(Character.id == character_id)
    if not character:
        return redirect(url_for('character.list'))

    if request.method == 'POST':
        character.name = request.form['name']
        character.gender = request.form['gender']
        character.save()
        return redirect(url_for('character.list'))

    return render_template('character_edit.html', character=character)