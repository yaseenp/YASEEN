from flask import Flask, render_template, request,session

app = Flask(__name__)
app.secret_key ='a'
def showall():
    sql= "SELECT * from USER"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ",  dictionary["CONTACT"])
        print("The Adress is : ",  dictionary["ADDRESS"])
        print("The Role is : ",  dictionary["ROLE"])
        print("The Branch is : ",  dictionary["BRANCH"])
        print("The Password is : ",  dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def getdetails(email,password):
    sql= "select * from USER where email='{}' and password='{}'".format(email,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ", dictionary["CONTACT"])
        print("The Address is : ", dictionary["ADDRESS"])
        print("The Role is : ", dictionary["ROLE"])
        print("The Branch is : ", dictionary["BRANCH"])
        print("The Password is : ", dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def insertdb(conn,name,email,contact,address,role,branch,password):
    sql= "INSERT into USER VALUES('{}','{}','{}','{}','{}','{}','{}')".format(name,email,contact,address,role,branch,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))
    
    
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mwv02817;PWD=BGu2G7vYyF7JGCrq",'','')
print(conn)
print("connection successful...")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        contact = request.form['mobile']
        address = request.form['address']
        role = request.form['role']
        if role =="0":
            role = "Faculty"
        else:
            role = "Student"
        branch = request.form['branch']
        password = request.form['password']
        
        #inp=[name,email,contact,address,role,branch,password]
        insertdb(conn,name,email,contact,address,role,branch,password)
        return render_template('login.html')
        

@app.route("/login",methods=['POST','GET'])
def loginentered():

      global Userid
      global Username
      msg = ''
      if request.method == "POST" :
           email = str(request.form['email'])
           print (email)
           password = request. form['password']

           sql = "SELECT * FROM REGISTER WHERE EMAIL=? AND PASSWORD=?"

           stmt = ibm_db.prepare(conn, sql)

           # this username & password is should be same as db-2 details & order also

           ibm_db.bind_param(stmt, 1, email)
           ibm_db.bind_param(stmt, 2, password)
           ibm_db. execute(stmt)
           account = ibm_db.fetch_assoc (stmt)
           print(account)
           if account:
                session['Loggedin'] = True
                session['id'] = account['EMAIL']
                Userid = account['EMAIL']
                session['email'] = account['EMAIL']
                Username = account['USERNAME']
                Name = account['NAME']
                msg = "logged in successfully !"
                sql ="SELECT ROLE FROM REGISTER where email = ?"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt, 1, email)
                ibm_db.execute (stmt)
                r = ibm_db.fetch_assoc(stmt)
                print(r)
                if r['ROLE'] == 1:
                     print ("STUDENT")
                     return render_template("studentprofile.html", msg=msg, user=email, name=Name,role="STUDENT",username=Username, email=email)

                elif r['ROLE']== 2:
                       print ("FACULTY")
                       return render_template("Facultyprofile.html", msg=msg, user=email, name=Name,role="FACULTY",username=Username, email=email)
                else:
                       return render_template("adminProfile.html", msg=msg, user=email, name=Name,role="ADMIN",username=Username, email=email)
           else:
                       msg = "Incorrect Email/password"

                       return render_template("login.html", msg=msg)
      else:
                return render_template("login.html")


# Rendering Adminprofile.html
@app.route("/adminprofile")
def aprofile():
    return render_template("adminProfile.html")

if __name__ =='__main__':
    app.run( debug = True)
                  