#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from uowmlib import WPConfiguration
import pprint

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def config():
    wpconf = WPConfiguration()
    if request.method == 'POST':
        for x in request.form:
            wpconf.set(x, request.form[x]) 
    return render_template('index.html', conf=wpconf)

@app.route("/collections", methods=['GET', 'POST'])
def collections():
    wpconf = WPConfiguration()
    return render_template('collections.html', collections=wpconf.collections)

def main():
    app.debug = True
    app.run()

if __name__ == "__main__":
    main()
