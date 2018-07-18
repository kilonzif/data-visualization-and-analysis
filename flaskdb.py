
from io import BytesIO
from flask import Flask, render_template, send_file, make_response,json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('ggplot')
 
 
app = Flask(__name__)
 
c = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='pythondata')
 
@app.route('/')
def index(): 
    df = pd.read_sql("SELECT * FROM train", con=c)
    return render_template("index.html",  data=df.head(10).to_html())
 

@app.route('/analysis')
def passenger_class_dist():
	df = pd.read_sql("SELECT * FROM train", con=c)
	#gender
	# gender_results=df.groupby(['Sex'])['Sex'].count()
	gender_results=df.groupby('Sex').size()
	gender_new_df=pd.DataFrame(gender_results)
	#Passenger class distribution
	class_results=df.groupby(['Pclass'])['Pclass'].count()
	class_new_df=pd.DataFrame(class_results)
	#Passenger class and gender distribution
	pass_class_gender_group_df=df.groupby(['Pclass','Sex'])['Sex'].count()
	unstacked_df=pass_class_gender_group_df.unstack('Pclass').T # Unstack the results then transpouse
	pass_class_gender_new_df=pd.DataFrame(unstacked_df,columns=['female','male']) #create new dataframe
	return render_template("analysis.html", gender_data=gender_new_df.to_html(),  passengers_data=class_new_df.to_html(),  passengers_gender_data=pass_class_gender_new_df.to_html())
 
@app.route('/gender_pie_chart/')
def gender_pie_chart():
    df = pd.read_sql("SELECT * FROM train", con=c)
    data=df.groupby(['Sex'])['Sex'].count()
    gender_labels=['Female','Male']
    fig,ax=plt.subplots()
    gender_color = ['r','g']
    ax.pie(data, labels=gender_labels, colors=gender_color,autopct='%1.1f%%', startangle=90, shadow= False)
    plt.axis('equal')
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/class_bar_graph/')
def class_bar_graph():
    df = pd.read_sql("SELECT * FROM train", con=c)
    new_df=df.groupby(['Pclass'])['Pclass'].count()
    pclass=new_df[0:]
    new_df=df.groupby(['Pclass'])['Pclass'].count()
    fig, ax = plt.subplots()
    ax = pclass.plot(kind='bar', color = ['r','g','y'], fontsize=12)
    ax.set_xlabel("Passenger Class (Pclass)", fontsize=12)
    ax.set_ylabel("Population", fontsize=12)
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')
 
@app.route('/class_gender_bar_graph/')
def class_gender_bar_graph():
    df = pd.read_sql("SELECT * FROM train", con=c)
    group_df=df.groupby(['Pclass','Sex'])['Sex'].count()
    unstacked_df=group_df.unstack('Pclass').T 
    new_df=pd.DataFrame(unstacked_df,columns=['female','male']) 
    fig, ax = plt.subplots()
    ax = new_df[['female','male']].plot(kind='bar',color = ['r','g'], legend=True, fontsize=12)
    ax.set_xlabel("Passenger Class (Pclass)", fontsize=12)
    ax.set_ylabel("Population", fontsize=12)
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')
     
@app.route('/visualization')
def visualization():
    return render_template('visualization.html')
 




if __name__ == '__main__':
    app.run(debug=True)