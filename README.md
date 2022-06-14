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

Steam遊戲評論預測推薦或不推薦，以及即時顯示某款遊戲評論的文字雲，或產生自訂義文字雲

## 使用技術

藉由 beautifulSoup + selenium 爬取 Steam 遊戲評論，透過 xampp 架設後端資料庫，前端採用 flask 框架  
透過 simpletransformers 來去建立 bert 模型，來預測評論推薦與否  
文字雲部份透過 jieba 進行段詞，使用 wordcloud 產生文字雲圖片  
  
`python`
`flask`
`xampp`
`jieba`
`wordcloud`
`simpletransformers`
`selenium`
`beautifulSoup`


## 如何開始

先打開 `xampp` 的Apache及MySQL  
再運行 `python run.py` 

## `資料夾介紹`

### `jieba-dict`

### `static`

### `templates`

### `uploads`

### `web_crawler`

### `wordcloud_data`

