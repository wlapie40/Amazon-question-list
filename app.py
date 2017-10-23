from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
import pyodbc
from wtforms import SelectField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'D0ntT3LLAny0n3!?!?!'

GradTrav = pyodbc.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=FAKE_SERVER_NAME;'
    r'DATABASE=FAKE_DB_NAME;'
    r'Trusted_Connection=True;'
    )

cursor=GradTrav.cursor()

class Form(FlaskForm):
    Lang = SelectField('Select language',choices=[('CZ','CZ'),('EN','EN'),('PL','PL'),('ES','ES')],validators=[InputRequired()])
    Type = SelectField('Select product type', choices=[('Home HPC','Home HPC'),('Video','Video'),('Hardlines-EU','Hardlines-EU'),('PrinterEU','PrinterEU'),('COMMUNICATIONS','COMMUNICATIONS'),('TV 2016','TV 2016'),('Repair TV','Repair TV'),('Repair Tools','Repair Tools'),('Home+Kitchen','Home+Kitchen'),('Major Appliance','Major Appliance'),('AUDIO','AUDIO'),('Repair-EU','Repair-EU'),('Home Non Power','Home Non Power'),('Repair Computer','Repair Computer'),('Jewelery','Jewelery'),('Camera','Camera'),('Watches','Watches'),('VG','VG')],validators=[InputRequired()])

@app.route('/',methods=['GET','POST'])
def hello():
    form=Form()
    if request.method=='POST':
        lang = form.Lang.data,
        type = form.Type.data,

        cursor.execute("""SELECT [Subtype],[value],[Order] FROM [GradTrav].[dbo].[QuestionList] WITH (NOLOCK)WHERE LANG='"""+str(lang[0])+"'"+""" AND TYPE='"""+str(type[0])+"'")
        data = [[i.Subtype,i.value,int(i.Order)] for i in cursor.fetchall()]
        r=0
        for i in data:
            if i[0] == 'Q':
                r += 1
                i.append(r)
            else:
                i.append(r)

        prev_elem=None
        for i in data:
            if i[0] == 'Q' and 'Check' in i[1]:
                i.append('check_box')
                prev_elem = 'check_box'
            elif i[0] == 'A' and prev_elem == 'check_box':
                i.append('check_box')
            else:
                i.append('list_box')
                prev_elem = 'list_box'
        print(data)
        return render_template('header.html',data=data,form=form)
    return render_template('header.html',form=form)

@app.route('/ReadAnswer',methods=['GET','POST'])
def ReadAnswer():
    if request.method == "POST":
        selected_contacts = request.form.getlist("contacts")
        print(selected_contacts)
    return render_template('header.html')

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0',debug=True)