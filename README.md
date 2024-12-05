# クエスト派遣管理アプリケーション
第10回 講義内資料サンプルコード

## 内容（メモ）
- データ(models)
  - キャラクタ
    - 名前（入力）
    - 性別（選択）
  - 武器
    - 名前（入力）
    - 攻撃力（入力）
    - 武器タイプ（選択）
  - クエスト？
    - 名前（入力）
    - 報酬（入力）

- 画面(routesとtemplates) 
  - キャラクタ一覧 
    - キャラクタ制作画面
    - キャラクタ編集
  - 武器リスト
    - 武器制作画面
    - 武器編集画面
  - クエスト画面
    - クエスト追加画面
    - クエスト編集画面

（派遣

　派遣一覧
　派遣先選択）

## require

```bash
python 3.12 or higher

# python lib
Flask==3.0.3
peewee==3.17.7
```

## usage

```bash
$ python app.py
```
