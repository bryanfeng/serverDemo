# -*- coding:utf-8 -*-
from flask import Flask, request
 
# 引入bleu计算
from Bleu import Bleu


app = Flask(__name__)
 
@app.route('/')
def hello_world():
	return 'hello_word'

@app.route('/bleu')
def bleu():
	source = request.args.get('source')
	ref = request.args.get('ref')
	my_dog = Bleu(source, ref)
	return my_dog.getBleu()
 
if __name__ == '__main__':
	app.run()
