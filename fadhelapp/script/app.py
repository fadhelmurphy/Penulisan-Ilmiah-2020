from flask import Flask,render_template,request
from scraping import scrap
from classify import massive,predicts

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def predict():
	if request.method == 'GET':
		return render_template('layout.html',title="Home",page='result.html')
	else:
		result = predicts(request.form['message'])
		return render_template('layout.html',msg=result,title="Home",page='result.html')

@app.route('/scraping',methods=['GET','POST'])
def scraping():
	if request.method == 'GET':
		return render_template('layout.html',title="Scraping",page='scraping.html')
	else:
		df = scrap(request.form['query'],request.form['awal'],request.form['akhir'],request.form['limit'])
		df=massive(df)	
		return render_template('layout.html',data=df.to_html(classes="table table-striped table-bordered table-hover",escape=False),title="Scraping",page='scraping.html')

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')