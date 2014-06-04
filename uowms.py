#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from uowmlib import WPConfiguration

app = Flask(__name__)

@app.route("/")
def hello():
    wpconf = WPConfiguration()
    return render_template('index.html', conf=wpconf)

if __name__ == "__main__":
    app.debug = True
    app.run()
