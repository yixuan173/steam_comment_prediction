from flask import Flask, request, Response, render_template
from flask_cors import CORS
import json
import pandas as pd
import os
import jieba
from os import path
from collections import Counter
from wordcloud import WordCloud
from simpletransformers.classification import ClassificationModel
import pymysql
from flask_paginate import Pagination


app = Flask(__name__)
CORS(app)

# 連接資料庫
conn = pymysql.connect(
    host="127.0.0.1", port=3306, user='root', passwd='', db='steamdb', charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)


# 讀取本地圖片
def return_img_stream(img_local_path):
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream


# 建立文字雲圖片
def create_word_cloud(excel_path):
    df = pd.read_excel(excel_path)
    df = df.to_csv('./uploads/wordcloud.txt', sep='\t', index=False)

    # 載入停用詞、中文、自訂義字典
    STOPWORDS = [line.strip() for line in open(
        "./jieba_dict/stopword.txt", encoding="utf-8").readlines()]
    jieba.set_dictionary('./jieba_dict/dict.txt')
    jieba.load_userdict('./jieba_dict/mydict.txt')

    text = open('./uploads/wordcloud.txt', encoding='utf8')
    word_list = list(filter(lambda x: x not in STOPWORDS and len(x)
                            != 1, jieba.cut(text.read())))
    text.close()
    
    word_freq = Counter(word_list) # 統計詞彙出現頻率
    # 文字雲呈現樣式設定
    wc = WordCloud(width=800,
                   height=400,
                   background_color='white',
                   max_words=500,
                   max_font_size=130,
                   random_state=42,
                   min_font_size=5,
                   colormap='tab20',
                   font_path='./wordcloud_data/SourceHanSansTW-Regular.otf')

    wc.generate_from_frequencies(word_freq) #生成文字雲
    wc.to_file('./uploads/pic/wordcloud.jpg')
    img_stream = return_img_stream('./uploads/pic/wordcloud.jpg')

    return img_stream
    

#########路由#########
# 首頁
@app.route('/')
def index():
    return render_template('index.html')


# 預測評論正負評
@app.route('/predictComment', methods=['POST', 'GET'])
def predictComment():
    if request.method == 'POST':
        model = ClassificationModel(
            'bert', './model/model_086_2', use_cuda=False) # './model/model_086_2'為載入事前訓練好的模型
        predictions, _ = model.predict([request.values['comment']])
        if predictions[0] == 1:
            ans = '推薦'
        else:
            ans = '不推薦'
        return render_template('predict.html', comment=request.values['comment'], predictions=ans)
    return render_template('predict.html', comment="")


# 讀取不同遊戲類別頁面
@app.route('/category/<name>')
def action(name, limit=9):
    if name == 'action':
        category = "動作"
    if name == 'rpg':
        category = "角色扮演"
    if name == 'strategy':
        category = "策略"
    if name == 'adventure_and_casual':
        category = "冒險和休閒"
    if name == 'simulation':
        category = "模擬"
    if name == 'sports_and_racing':
        category = "運動和競速"

    cursor.execute(f"SELECT * FROM `game` WHERE 類別 = '"+category+"' ")
    items = cursor.fetchall()
    # 實現分頁功能
    page = int(request.args.get("page", 1))
    start = str((page-1) * limit)
    paginate = Pagination(page=page, total=len(items))
    # 顯示每頁9筆資料
    cursor.execute(f"SELECT * FROM `game` WHERE 類別 = '" +
                   category + "' limit "+start+",9")
    items = cursor.fetchall()

    return render_template('category.html', category=category, items=items, paginate=paginate)


# 搜尋遊戲
@app.route('/search', methods=['POST'])
def search():
    search = request.values['searchText']
    cursor.execute(
        f"SELECT DISTINCT * FROM `game` WHERE 名稱 like '%"+search+"%'  GROUP By 名稱")
    items = cursor.fetchall()
    return render_template('search.html', items=items, search=search, count=len(items))


# 產生各個遊戲的文字雲
@app.route('/game', methods=['GET'])
def model():
    name = request.args.get('name')
    excel_path = "./wordcloud_data/all/"+name+".xlsx"
    img_stream = create_word_cloud(excel_path)

    cursor.execute(
        f"SELECT DISTINCT * FROM `game` WHERE 名稱 like '"+name+"'  GROUP By 名稱")
    items = cursor.fetchall()

    return render_template('gamedetail.html', img_stream=img_stream, items=items)


# 顯示本地上傳文件的文字雲
@app.route("/wordcloud", methods=['POST', 'GET'])
def wordcloud():
    if request.method == 'POST':
        img_path = './uploads/pic/wordcloud.jpg'
        img_stream = return_img_stream(img_path)
        return render_template('wordcloud.html', img_stream=img_stream)
    return render_template('wordcloud.html', img_stream="")


# 接收前端傳送的檔案，轉文字雲圖片儲存
@app.route('/upload_file', methods=['POST'])
def upload():
    f = request.files['file']
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'uploads/')
    if not os.path.exists(upload_path):
        os.mkdir(upload_path)

    file_path = str(f.filename)
    f.save(upload_path+"/wordcloud.xlsx")

    # 轉文字雲
    create_word_cloud("./uploads/wordcloud.xlsx")

    return Response(json.dumps(file_path))


if __name__ == '__main__':
    app.run(debug=False)
