# Car parts classification (inference api)

## クイックスタート
```bash
git clone https://github.com/sojiro-otsubo/parts-classify-inference
cd parts-classify-inference
docker-compose up

👉 http://localhost:8080
```
コンテナ内では5000番ポートで開いているが, 実機からは8080ポートにアクセスする

### 入力: 車の画像
### 出力: bbox, label, score (座標は416, 416にリサイズされたもの)
```bash
{"result":{"bbox":[[306,201,375,299],[36,201,105,302],[195,170,308,287],[394,158,412,198],[344,112,385,175],[10,191,43,231],[118,169,247,290],[118,171,242,283]],"label":[2,2,5,4,0,0,5,6],"score":[0.95,0.938,0.468,0.457,0.426,0.407,0.366,0.274]},"status":"ok"}
```

## 動作チェック
### イメージのビルド
```bash
docker build -it parts-classify -f docker/Dockerfile .
```
### コンテナ作成
```bash
docker run -p 8080:5000 -it parts-classify
```
コンテナに入る
### テストの実行
```bash
python -m unittest tests.test_api
```
### APIの起動
```bash
python api_server.py
```
### 死活チェック
```bash
curl http://localhost:8080/status
```

## 学習コード
https://github.com/sojiro-otsubo/parts-classify-learn