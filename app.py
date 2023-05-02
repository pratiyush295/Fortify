from flask import Flask,render_template,redirect,request,url_for,jsonify,json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc,asc
from flask_login import UserMixin,login_user,login_required,current_user,logout_user
from datetime import datetime
import os
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import LoginManager
import smtplib as s
import random
import urwid
# from app import app


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'key'
db=SQLAlchemy(app)
app.app_context().push()


class Reply(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    reply=db.Column(db.String(1000),nullable=True)
    commentid=db.Column(db.Integer,db.ForeignKey('comment.id'))
    date=db.Column(db.DateTime,default=datetime.utcnow)
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))


class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String(1000),nullable=True)
    noteid=db.Column(db.Integer,db.ForeignKey('note.id'))
    date=db.Column(db.DateTime,default=datetime.utcnow)
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))
    username=db.Column(db.String(1000),nullable=False)
    reply=db.relationship('Reply')

class Note(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    data=db.Column(db.String(10000),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    like=db.Column(db.Integer,default=0)
    user_liked=db.Column(db.Boolean,default=False)
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))
    comment=db.relationship('Comment')

class Frnd(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    frnd_username=db.Column(db.String(1000),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    source_username=db.Column(db.String(1000),db.ForeignKey('user.username'))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(500),nullable=False)
    gender=db.Column(db.String(500),default="Male")
    email=db.Column(db.String(500),nullable=False)
    email_verified=db.Column(db.Boolean,default=False)
    otp=db.Column(db.Integer,nullable=True)
    phone=db.Column(db.String(20),nullable=False)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    bio=db.Column(db.String(1000),nullable=True)
    total_likes=db.Column(db.Integer,default=0)
    notes=db.relationship('Note')
    frnd=db.relationship('Frnd')


def create_db():
    if not os.path.exists('database.db'):
        db.create_all()
        # print('database created')




login_manager=LoginManager()
login_manager.login_view='home'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


def send_mail():

    otp=random.randint(1001,9999)
    ob=s.SMTP("smtp.gmail.com",587)
    ob.starttls()

    ob.login("fortify.achoix@gmail.com","pttidoswwoyteaoz")

    subject="Account Verification Otp"
    body=f'Heyy Blogger,\nYour otp for you account verification is {otp}'

    message="Subject:{}\n\n{}".format(subject,body)
    listOfAddress=[]
    listOfAddress.append(str(current_user.email))
    ob.sendmail("fortify.achoix@gmail.com",listOfAddress,message)
    # print("Mail Sent Successfully")
    ob.quit()
    account=User.query.filter_by(id=current_user.id).first()
    account.otp=otp
    db.session.add(account)
    db.session.commit()
    




@app.route('/login',methods=['POST','GET'])
@app.route('/',methods=['POST','GET'])
def home():
    return render_template('home.html')








@app.route('/login_validation',methods=['GET','POST'])
def login_validation():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get("password")
        credential=User.query.filter_by(email=email).first()
        check=User.query.filter_by(username=email).first()
        # backup=User.query.filter_by(password=password).first()
        # notes=Note.query.filter_by(userid=credential.id)

        if credential:
            if check_password_hash(credential.password,password):
                login_user(credential,remember=True)
                # return render_template('profile.html',user=current_user,note=current_user.notes)
                return redirect(url_for('profile'))
            elif not check_password_hash(credential.password,password):
                message='Incorrect Password' 
                return render_template('home.html',message=message)
            else:
                message="Account Doesn't Exist" 
                return render_template('home.html',message=message)


        if check:
            if check_password_hash(check.password,password):
                login_user(check,remember=True)
                return render_template('profile.html',user=current_user)
            elif not check_password_hash(check.password,password):
                message='Incorrect Password' 
                return render_template('home.html',message=message)
            else:
                message="Account Doesn't Exist" 
                return render_template('home.html',message=message)

    message="Account Doesn't Exist" 
    return render_template('home.html',message=message)

@app.route('/profile')
def profile():
    return render_template('profile.html',user=current_user,note=current_user.notes,frnd=current_user.frnd)


@app.route('/getprofile',methods=['POST','GET'])
def getprofile():
    if request.method=='POST':
        queryusername=request.form.get('queryusername')
        account_user=User.query.filter_by(username=queryusername).first()
        account_user_name=User.query.filter_by(name=queryusername).all()
        account_frnd=Frnd.query.filter_by(source_username=current_user.username,frnd_username=queryusername).first()
        if account_user:
            return render_template('getprofile.html',user=account_user,cur=current_user,note=account_user.notes,frnd=account_user.frnd,already_frnd=account_frnd)
        elif account_user_name:
            return render_template('results.html',user=account_user_name,cur=current_user,search="yes")
        else:
            return render_template('profile.html',user=current_user,note=current_user.notes,frnd=current_user.frnd,message="User doesn't exist")
 
    return render_template('profile.html',user=current_user,note=current_user.notes,frnd=current_user.frnd)

@app.route('/getprofile_parameter/<username>',methods=['POST','GET'])
def getprofile_parameter(username):
    account_user=User.query.filter_by(username=username).first()
    account_frnd=Frnd.query.filter_by(source_username=current_user.username,frnd_username=username).first()
    return render_template('getprofile.html',user=account_user,note=account_user.notes,frnd=account_user.frnd,already_frnd=account_frnd,cur=current_user)

@app.route('/addfrnd/<username>',methods=['POST','GET'])
def addfrnd(username):
    account_frnd=Frnd(frnd_username=username,source_username=current_user.username)
    db.session.add(account_frnd)
    db.session.commit()
    account_user=User.query.filter_by(username=username).first()
    return render_template('getprofile.html',user=account_user,note=account_user.notes,frnd=account_user.frnd,already_frnd='Yes',cur=current_user)


@app.route('/frndresult/<username>')
def frndresult(username):
    account_user=User.query.filter_by(username=username).first()
    if account_user.frnd:
        return render_template('results.html',frnd=account_user.frnd,frnd_list='Yes')
    else:
        return render_template('results.html',frnd=account_user.frnd,frnd_list='no')

@app.route('/elite',methods=['POST','GET'])
def elite():
    
    user=User.query.all()
    # account_elite=User.query.order_by(user.total_likes).all()
    # account_elite=session.query(User).order_by(desc(User.total_likes)).all()
    return render_template('results.html',user=user,elite="yes")
    


@app.route('/otpfirst')
def otpfirst():
    send_mail()
    return render_template('otp.html',user=current_user)

@app.route('/otp',methods=['POST','GET'])
def otp():
    if request.method=="POST":
        ot=request.form.get('otp')
        # print(ot)
        if(len(ot)<4 or len(ot)>4):
            return render_template('otp.html',user=current_user,message="Please Enter Otp of lentgh 4 only")
        if (len(ot)==0):
            return render_template('otp.html',user=current_user,message="Please Enter Your Otp")
        if(len(ot)==4):
            
            # (ot)
            if str(ot)==str(current_user.otp):
                account=User.query.filter_by(id=current_user.id).first()
                account.email_verified=True
                db.session.add(account)
                db.session.commit()
                return render_template('profile.html',user=current_user,note=current_user.notes)
            else:
                return render_template('otp.html',user=current_user,message="Invalid Otp")
        else:
            pass
            
    # print(request.get_json['o1'])
    return render_template('otp.html',user=current_user)
    



@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=="POST":
       
        name=request.form.get('name')
        email=request.form.get('email')
        gender=request.form.get('gender')
        phone=request.form.get('phone')
        username=request.form.get('username')
        pass1=request.form.get('pass1')
        pass2=request.form.get('pass2')
        
        credential=User.query.filter_by(email=email).first()
        check=User.query.filter_by(username=username).first()

        # otp()
        

        if credential:
            message="Email Already Exists"
            return render_template('register.html',message=message)
        elif check:
            message="Username Already Exists"
            return render_template('register.html',message=message)
        elif (len(username)<5):
            message="Username should be of minimun size 5"
            return render_template('register.html',message=message)
        elif(pass1!=pass2):
            message="Both password doesn't match"
            return render_template('register.html',message=message)
        elif(len(name)==0 or len(email)==0 or len(pass1)==0 or len(pass2)==0 or len(username)==0):
            message="Please fill all the fields"
            return render_template('register.html',message=message)
        elif(len(pass1)<6 and len(pass2)<6):
            message="Passwords should be a minimum of six characters"
            return render_template('register.html',message=message)

        else:
            new_account=User(name=name,email=email,gender=gender,phone=phone,username=username,password=generate_password_hash(pass1,method='sha256'))
            # login_user(new_account,remember=True)
            db.session.add(new_account)
            db.session.commit()
            
            message='Account created successfully'
            return render_template('home.html',message=message)

    return render_template('register.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')





@app.route('/addblog',methods=['POST','GET'])
def addblog():

    if request.method=='POST':
        title=request.form.get('title')
        data=request.form.get('blogdata')
        if len(title)==0 or len(data)==0:
            message="You Need to Write something before uploading"
            return render_template('addblog.html',message=message,heading="Write",button="Add",user=current_user)
        else:
            new_note=Note(title=title,data=data,userid=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            message="Blog Added!!!"
            return render_template('addblog.html',message=message,user=current_user)
        


    return render_template('addblog.html',heading="Write",button="Add",user=current_user)


@app.route('/showblog')
def showblog():


    return render_template('showblog.html',all="goa",user=current_user)

@app.route('/blog_index')
def blog_index():
    account_note=Note.query.all()
    return render_template('showblog.html',open='yes',note=account_note)

@app.route('/singleblog/<int:noteid>',methods=['POST','GET'])
def singleblog(noteid):
    account_note=Note.query.filter_by(id=noteid).first()
    account_user=User.query.filter_by(id=account_note.userid).first()
    print(account_user.name)
    return render_template('singleblog.html',note=account_note,user=account_user)

@app.route('/comment/<int:noteid>',methods=['POST','GET'])
def comment(noteid):
    account_note=Note.query.filter_by(id=noteid).first()
    account_user=User.query.filter_by(id=account_note.userid).first()
    return render_template('singleblog.html',note=account_note,user=account_user,com=account_note.comment,comment='yes')

@app.route('/addcomment/<int:noteid>',methods=['POST','GET'])
def addcomment(noteid):
    note_account=Note.query.filter_by(id=noteid).first()
    user_account=User.query.filter_by(id=note_account.userid)

    com=request.form.get('comment')
    if request.method=='POST':
        print(com)
        comment_account=Comment(comment=com,noteid=noteid,userid=note_account.userid,username=current_user.username)
        db.session.add(comment_account)
        db.session.commit()
        return redirect(url_for('comment',noteid=noteid))
    return redirect(url_for('profile'))


@app.route('/addlike/<int:id>',methods=['POST','GET'])
def addlike(id):
    account=Note.query.filter_by(id=id).first()
    account_user=User.query.filter_by(id=account.userid).first()


    if (account.user_liked==True and account_user.username==current_user.username):
        account.like=account.like-1
        account_user.total_likes=account_user.total_likes-1
        account.user_liked=False
        # print('hit if')
   
    elif(account.user_liked and account_user.username==current_user.username and account.like==0):
        # print('hit elif1')
        pass
    elif(account.user_liked==False and account_user.username==current_user.username):
        # print('hit elif2')
        # print(account.user_liked)
        account.like=account.like+1
        account_user.total_likes=account_user.total_likes+1
        account.user_liked=True
        
    else:
        print('hit else')
        account.like=account.like+1
        account_user.total_likes=account_user.total_likes+1

    
    

    # account_user.total_likes=account_user.total_likes+1
    db.session.add(account)
    db.session.add(account_user)
    db.session.commit()
    return render_template('singleblog.html',note=account,user=account_user,com=account.comment,comment='yes')
    # return render_template('showblog.html',all="goa",user=current_user)



@app.route('/addbio',methods=["POST"])
def addbio():
    if request.method=='POST':
        bio=request.form.get('bio')
        account=User.query.filter_by(id=current_user.id).first()
        account.bio=bio
        db.session.add(account)
        db.session.commit()
        return render_template('profile.html',user=current_user,note=current_user.notes)
    # return render_template('home.html')
    return render_template('profile.html',user=current_user,note=current_user.notes)




if __name__=='__main__':
    # print("Command is here")
    create_db()
    app.run(debug=True,host='0.0.0.0')
    
    









    # pip install flask
    # pip install flask-sqlalchemy
    # pip install flask-login
    # Fatal error in launcher freeze