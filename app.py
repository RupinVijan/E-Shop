from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail



app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME="rupinvijan@gmail.com",
    MAIL_PASSWORD="mummypapas"

)
mail=Mail(app)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///order.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class order(db.Model):
    sno = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50) , nullable=False)
    email = db.Column(db.String(50) , nullable=False)
    address = db.Column(db.String(500) , nullable=False)
    phone = db.Column(db.String(50) , nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

@app.route("/")
def hello_world():
    return render_template("front.html")

@app.route("/front")
def home():
    return render_template("front.html")

@app.route("/contactus")
def about_us():
    return render_template("contactus.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/buy", methods=['GET','POST'])
def buy():
    if request.method=='POST':
        email=request.form.get('email')
        mail.send_message('This message is for verification of your email ' ,sender=email, recipients=[email],
        body="\n Thank You for shopping here \n\n your Verrification code is :: r48.\n\tRegards,\nRupin." )
        return redirect("/verify")
    return render_template("buy.html")

@app.route("/verify" , methods=['GET', 'POST'])
def verification():
    if request.method=='POST':
        verifyid=request.form.get("verifyid")
        if verifyid=="r48":
            return redirect("/confirm")
    return render_template("verify.html")
            
@app.route("/confirm" , methods=['GET', 'POST'])
def confirm():
    if request.method=='POST':

        name=request.form.get('name')
        email=request.form.get('email')
        address=request.form.get('address')
        phone=request.form.get('phone')
        entry=order(name=name,email=email,address=address,phone=phone)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('This message is from ' + name,
        sender=email, recipients=["rupinvijan@gmail.com",email],
        body="\n we are pleased to inform you that your order is confirmed.\n\nExpext your delivery within 7-8 working days please give reviews about it too.\n\nscontact number" + phone + "\n\n At delivery address" + address
        )
    
    return render_template("confirm.html")

@app.route("/admin",methods=['GET','POST'])
def admin():
    if request.method=='POST':
        user=request.form.get('user')
        password=request.form.get('password')
        if user=="Rupin" and password=="password":
            return redirect("/info")
            
    return render_template("admin.html")

@app.route("/info",methods=['GET','POST'])
def info():
    dets=order.query.all()
    return render_template("info.html",dets=dets)

@app.route("/logout")
def logout():
    
    return redirect("/admin")

@app.route("/delete/<string:sno>" , methods=['GET','POST'])
def delete(sno):
    dets=order.query.filter_by(sno=sno).first()
    db.session.delete(dets)
    db.session.commit()
    return redirect("/admin")


if __name__=="__main__":
    app.run(debug=True)