from flask import Blueprint, render_template, request, redirect, url_for
from models import Weapon

# Blueprintの作成
weapon_bp = Blueprint('weapon', __name__, url_prefix='/weapons')


@weapon_bp.route('/')
def list():
    weapons = Weapon.select()
    return render_template('weapon_list.html', title='武器一覧', title2='武器タイプの割合', items=weapons)


@weapon_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        attribute = request.form['attribute']
        attackpower = request.form['attackpower']
        Weapon.create(name=name, attribute=attribute,attackpower=attackpower)
        return redirect(url_for('weapon.list'))
    
    return render_template('weapon_add.html')


@weapon_bp.route('/edit/<int:weapon_id>', methods=['GET', 'POST'])
def edit(weapon_id):
    weapon = Weapon.get_or_none(Weapon.id == weapon_id)
    if not weapon:
        return redirect(url_for('weapon.list'))

    if request.method == 'POST':
        weapon.name = request.form['name']
        weapon.attribute = request.form['attribute']
        weapon.attackpower = request.form['attackpower']
        weapon.save()
        return redirect(url_for('weapon.list'))

    return render_template('weapon_edit.html', weapon=weapon)