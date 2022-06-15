# Steam評論預測及文字雲呈現
### `搜尋頁面`
![展示](https://github.com/yixuan173/steam_comment_prediction/blob/master/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA01.gif)
### `評論預測`
![展示](https://github.com/yixuan173/steam_comment_prediction/blob/master/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA02.gif)
### `個別遊戲文字雲`
![展示](https://github.com/yixuan173/steam_comment_prediction/blob/master/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA03.gif)
### `自定義文字雲`
![展示](https://github.com/yixuan173/steam_comment_prediction/blob/master/%E5%B1%95%E7%A4%BA/%E5%B1%95%E7%A4%BA04.gif)

## 簡介

Steam遊戲評論預測推薦或不推薦，以及即時顯示某款遊戲評論的文字雲，或產生自定義文字雲

## 使用技術

藉由 beautifulSoup + selenium 爬取 Steam 遊戲評論，使用 xampp 架設後端資料庫，前端採用 flask 框架  
透過 simpletransformers 裡面提供的 bert 模型，由先前爬取的評論共6000多筆（推薦不推薦各占將近50%）進行訓練  
網站利用訓練完成後的模型（F1-Score: 86.2%，Sensitivity: 85.8%，Specificity: 86.5%），來即時預測評論推薦與否  
文字雲部份透過 jieba 進行斷詞，使用 wordcloud 產生文字雲  
  
`python`
`flask`
`xampp`
`jieba`
`wordcloud`
`simpletransformers`
`selenium`
`beautifulSoup`


## 如何開始

[下載](https://drive.google.com/drive/folders/1Go-Do0g3Z790wMwMuBAbw7Jv1hJGalq6?usp=sharing "下載")資料庫檔案以及預先用Steam評論訓練好的模型（或是選擇直接利用simpletransformers提供的模型也可以）  
打開 `xampp` 的Apache及MySQL  
再將下載完的`steamdb.sql`匯入到資料庫  
以及模型資料夾`model/model_086_2`載入  
再運行 `python run.py` 

## `資料夾介紹`

### `jieba-dict`

放置jieba斷詞所需的中文詞典、停用詞詞典、自定義詞典

### `static`

放置靜態文件

### `templates`

放置html

### `uploads`

放置產生文字雲所需的文字檔以及圖片

### `web_crawler`

前置處理，用來爬取Steam評論

### `wordcloud_data`

存放先前從Steam爬取的評論，用來產生文字雲
