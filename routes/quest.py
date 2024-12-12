from flask import Blueprint, render_template, request, redirect, url_for
from models import  Character, Weapon, Quest
from datetime import datetime

# Blueprintの作成
quest_bp = Blueprint('quest', __name__, url_prefix='/quests')


@quest_bp.route('/')
def list():
    quests = Quest.select()
    return render_template('order_list.html', title='クエスト一覧', items=quests)


@quest_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        character_id = request.form['character_id']
        weapon_id = request.form['weapon_id']
        quest_date = datetime.now()
        Quest.create(name=name, character=character_id, weapon=weapon_id, quest_date=quest_date)
        return redirect(url_for('quest.list'))
    
    characters = Character.select()
    weapons = Weapon.select()
    return render_template('order_add.html', characters=characters, weapons=weapons)


@quest_bp.route('/edit/<int:quest_id>', methods=['GET', 'POST'])
def edit(quest_id):
    quest = Quest.get_or_none(Quest.id == quest_id)
    if not quest:
        return redirect(url_for('quest.list'))

    if request.method == 'POST':

        quest.name = request.form['name']
        quest.character = request.form['character_id']
        quest.weapon = request.form['weapon_id']
        quest.save()
        
        return redirect(url_for('quest.list'))

    characters = Character.select()
    weapons = Weapon.select()
    return render_template('order_edit.html', quest=quest, characters=characters, weapons=weapons)
