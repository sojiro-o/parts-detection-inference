#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time

from flask import Flask, url_for, redirect
from flask_cors import CORS

# api
from api.status import status
# from api.upload import upload
from api.predict import predict

app = Flask(__name__)

# crossoriginの有効化
CORS(app)

app.register_blueprint(status)
app.register_blueprint(predict)


if __name__ == '__main__':
    print("--------- LOADING GRAPH ---------")
    start = time.time()
    print('loading time:{:.2f}[sec]'.format(time.time() - start))
    print("--------- SERVER ACTIVE ---------")
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
