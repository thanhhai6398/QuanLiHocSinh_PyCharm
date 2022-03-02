from flask import Flask, render_template, request, redirect, jsonify, session
from my_app import app, login_manager, endpoint, partnerCode, accessKey, secretKey, redirectUrl, ipnUrl, requestType, port, password
from admin import *
from flask_login import login_user, logout_user, login_required, current_user
import utils
import datetime
import json
from urllib.request import Request, urlopen
import uuid
import hmac
import hashlib
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@app.route("/")
def home():
    return render_template("home.html")

@login_manager.user_loader
def user_load(id):
    return Person.query.get(id)

@app.route("/login", methods=['post'])
def login_exe():
    err_msg = ""
    username = request.form.get("username")
    password = request.form.get("password")
    password = str(hashlib.md5(password.encode("utf-8")).digest())

    user1 = Person.query.filter(Person.username==username,
                               Person.password==password,
                               Person.chucVu==1).first()
    if user1: #admin dang nhap thanh cong
        login_user(user1)
    return redirect("/admin")

@app.route("/user-login", methods=['get','post'])
def normal_user_login():
    if request.method== 'GET':
        return render_template("login_user.html")
    else:
        err_msg=""
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.encode("utf-8")).digest())

        user2 = Person.query.filter(Person.username == username,
                                    Person.password == password,
                                    Person.chucVu == 2).first()
        user3 = Person.query.filter(Person.username == username,
                                    Person.password == password,
                                    Person.chucVu == 3).first()
        user4 = Person.query.filter(Person.username == username,
                                    Person.password == password,
                                    Person.chucVu == 4).first()
        if user2:  # giaovu dang nhap thanh cong
            login_user(user2)
            return redirect("/giaovu")
        elif user3:
            login_user(user3)
            return redirect("/giaovien")
        elif user4:
            login_user(user4)
            return redirect("/hocsinh")
        else:
            err_msg = "Username hoặc password không chính xác!"
            return render_template("login_user.html", err_msg=err_msg)

@app.route("/giaovu")
def home_giaovu():
    session["pid"] = 2
    return render_template("giaovu/giaovu_home.html")

@app.route("/giaovien")
def home_giaovien():
    session["pid"] = 3
    return render_template("giaovien/giaovien_home.html")

@app.route('/hocsinh')
def home_hocsinh():
    session["pid"] = 1
    return render_template("hocsinh/hocsinh_home.html")

@app.route("/user-logout")
def normal_user_logout():
    logout_user()
    return redirect("/user-login")

@app.route("/register", methods=['get','post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        try:
            password = request.form["password"]
            confirm_password = request.form['confirm-password']
            if password.strip() == confirm_password.strip():
                data = request.form.copy()
                del data['confirm-password']

                if utils.add_user(hoTen=data['hoten'],
                                  gioiTinh=data['gioitinh'],
                                  ngaySinh=datetime(data['ngaysinh']),
                                  diaChi=data['diachi'],
                                  email=data['email'],
                                  username=data['username'],
                                  password=data['password']):
                    return redirect("/user-login")
                else:
                    err_msg = "Đăng ký không thành công! Vui lòng kiểm tra lại thông tin đăng ký!"
            else:
                err_msg = "Mật khẩu không khớp!"
        except:
            err_msg = "Lỗi hệ thống!!!"

    return render_template("register.html", err_msg=err_msg)


    """user2 = Person.query.filter(Person.username == username,
                                Person.password == password,
                                Person.chucVu == 2).first()
    user3 = Person.query.filter(Person.username == username,
                                Person.password == password,
                                Person.chucVu == 3).first()
    user4 = Person.query.filter(Person.username == username,
                                Person.password == password,
                                Person.chucVu == 4).first()

    if user2: #dang nhap thanh cong
        return redirect("/giaovu")
        #return render_template("giaovu/giaovu_home.html")
    if user3: #dang nhap thanh cong
        return redirect("/giaovien")
    if user4: #dang nhap thanh cong
        return redirect("/hocsinh")"""

###########admin = BGH
@app.route('/upload', methods=['post'])
def upload():
    avatar = request.files.get("avatar")
    if avatar:
        avatar.save("%s/static/images/%s" % (app.root_path, avatar.filename))
        return "Successful"
    return "Failed"

#############GVu
@app.route("/receipt")
def bien_lai():
    list = utils.get_tuition_list(tinhTrang=int(0))
    return render_template("giaovu/receipt.html",
                           list=list)

@app.route("/fee/<int:hocky>/<int:student_id>", methods=["get", "post"])
def pay_fee(hocky, student_id):
    if utils.pay_fee(hocky, student_id):
        return redirect("/fee")

@app.route("/fee", methods=["get", "post"])
def hoc_phi():
    list = utils.get_tuition_list(tinhTrang=int(1))
    if request.method == 'POST':
        hoTen = request.form["hoTen"]
        list1 = utils.get_tuition_list(hoTen=hoTen)
        return render_template("giaovu/fee.html", list=list1)
    return render_template("giaovu/fee.html",
                           list=list)

@app.route("/detailClass/<int:student_id>", methods=["get", "post"])
def delete_Student_from_Class(student_id):
    if utils.delete_Student_from_Class(student_id):
        return redirect("/listClass")

@app.route("/detailClass", methods=["get", "post"])
def read_or_create_list_Class():
    newSt = utils.get_student_new()
    lop_id = request.args.get("lop_id")
    lop = utils.get_Class(lop_id=lop_id)
    students = utils.get_student(lop_id=lop_id)
    if request.method == "POST":
        id = request.form["student_id"]
        if utils.add_Student_to_Class(student_id=id, lop_id=lop_id):
            return redirect("/listClass")
    return render_template("giaovu/detailClass.html",
                           students=students,
                           newSt=newSt,
                           lop=lop)

@app.route("/listClass")
def list_Class():
    classes = utils.get_Class()
    return render_template("giaovu/listClass.html",
                           classes=classes)

@app.route("/listClass/<int:lop_id>", methods=["get", "post"])
def delete_Class(lop_id):
    if utils.delete_Class(lop_id=lop_id):
        return redirect("/listClass")

@app.route("/addClass", methods=["get", "post"])
def add_Class():
    err = ""
    khoi = utils.get_Khoi()
    newSt = utils.get_student_new()

    if request.method == 'POST':
        maLop = request.form["maLop"]
        tenLop = request.form["tenLop"]
        khoiLop_id = request.form["khoiLop_id"]
        list = request.form.getlist("student_id")
        if utils.add_Class(maLop=maLop, tenLop=tenLop, khoiLop_id=khoiLop_id):
            for i in list:
                utils.add_Student_to_Class(student_id=i, lop_id=maLop)
            return redirect("/listClass")
        else:
            err = "Du lieu dau vao khong hop le!"
    return render_template("giaovu/addClass.html",
                           khoi=khoi,
                           newSt=newSt)

@app.route("/listStudent")
def list_Student():
    students = utils.get_student()
    return render_template("giaovu/listStudent.html",
                           students=students)

@app.route("/listStudent/<int:student_id>", methods=["get", "post"])
def delete_student(student_id):
    if utils.delete_student(student_id=student_id):
        return redirect("/listStudent")

@app.route("/addStudent", methods=["get", "post"])
def add_or_update_Student():
    err = ""
    student_id = request.args.get("student_id")
    student = None
    if student_id:
        student = utils.get_student_by_id(student_id=int(student_id))
    if request.method == 'POST':
        data = request.form.copy()
        if student_id:  # Cap nhat
            data = dict(request.form.copy())
            data["id"] = student_id
            hoTen = request.form["hoTen"]
            gioiTinh = request.form["gioiTinh"]
            ngaySinh = request.form["ngaySinh"]
            diaChi = request.form["diaChi"]
            email = request.form["email"]
            if utils.update_student(student_id=student_id, hoTen=hoTen, gioiTinh=gioiTinh,
                                    ngaySinh=ngaySinh, diaChi=diaChi, email=email):
                return redirect("/listStudent")
        else:  # Them
            if utils.add_person(**data):
                return redirect("/listStudent")
            else:
                err = "Dữ liệu đầu vào không hợp lệ!"
    return render_template("giaovu/addStudent.html",
                           student=student,
                           err=err)

###################################HS
@app.route('/lapdanhsach')
def lapdanhsach():
    lopList = utils.get_AllLop()
    return render_template("hocsinh/lapdanhsach.html", lopList=lopList)

@app.route('/tracuu')
def tracuu():
    return render_template("hocsinh/tracuu.html")

@app.route('/thanhtoan')
def thanhtoan():
    id = session.get("pid")
    if not id:
        return render_template("hocsinh/hocsinh_home.html")
    hoc_phi_list = utils.get_all_hoc_phi(id)
    tong_hoc_phi = 0
    for i in hoc_phi_list:
        tong_hoc_phi += i.tongHocPhi
    session["tongHocPhi"] = tong_hoc_phi
    return render_template("hocsinh/thanhtoan.html", hocPhiList=hoc_phi_list, tongHocPhi=tong_hoc_phi)

@app.route('/api/thanh-toan-momo', methods=['post'])
def thanh_toan_momo():
    # parameters send to MoMo get get payUrl
    orderInfo = "pay with MoMo"
    amount = str(session["tongHocPhi"])
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    extraData = ""

    raw_signature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData +\
                    "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo \
                    + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl \
                    + "&requestId=" + requestId + "&requestType=" + requestType

    h = hmac.new(secretKey.encode('utf-8'), raw_signature.encode('utf-8'), hashlib.sha256)
    signature = h.hexdigest()

    data = {
        'partnerCode': partnerCode,
        'partnerName': "HCMUTE",
        'storeId': "QuanLyHocSinh",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'ipnUrl': ipnUrl,
        'redirectUrl': redirectUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }

    data = json.dumps(data).encode('utf-8')
    clen = len(data)
    req = Request(endpoint, data, {'Content-Type': 'application/json', 'Content-Length': clen})
    f = urlopen(req).read()
    respone = json.loads(f.decode('utf-8'))
    return respone

@app.route('/ketquathanhtoan')
def ket_qua_thanh_toan():
    amount = request.args.get('amount')
    extraData = request.args.get('extraData')
    message = request.args.get('message')
    orderId = request.args.get('orderId')
    orderInfo = request.args.get('orderInfo')
    orderType = request.args.get('orderType')
    payType = request.args.get('payType')
    requestId = request.args.get('requestId')
    responseTime = request.args.get('responseTime')
    resultCode = request.args.get('resultCode')
    transId = request.args.get('transId')
    raw_signature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + \
                    "&message=" + message + "&orderId=" + orderId + "&orderInfo=" + orderInfo \
                    + "&orderType=" + orderType + "&partnerCode=" + partnerCode \
                    + "&payType=" + payType + "&requestId=" + requestId + "&responseTime=" + responseTime \
                    + "&resultCode=" + resultCode + "&transId=" + transId

    h = hmac.new(secretKey.encode('utf-8'), raw_signature.encode('utf-8'), hashlib.sha256)
    signature = h.hexdigest()
    msignature = request.args.get('signature')
    status = 0
    if signature == msignature:
        if resultCode == '0':
            pid = session['pid']
            utils.update_hoc_phi(pid)
            send_email()
            status = 1
            return render_template("hocsinh/ketquathanhtoan.html", status=status, signature=signature, msignature=msignature)
    return render_template("hocsinh/ketquathanhtoan.html", status=status, signature=signature, msignature=msignature)

def send_email():
    sender_email = 'hcmutenhom11@gmail.com'
    pid = session['pid']
    hoc_sinh = utils.get_hoc_sinh(pid)
    receiver_email = hoc_sinh.email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Thanh Toán Học Phí"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Chào bạn,
    Bạn đã thanh toán học phí thành công
    """
    html = """\
    <html>
      <body>
        <p>Chào bạn,<br>
           Bạn đã thanh toán học phí thành công<br>
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("hcmutenhom11@gmail.com", password)
        server.sendmail(sender_email, receiver_email, message.as_string())

@app.route('/api/xlketquathanhtoan', methods=['post'])
def xl_ket_qua_thanh_toan():
    data = request.json
    amount = data['amount']
    extraData = data['extraData']
    message = data['message']
    orderId = data['orderId']
    orderInfo = data['orderInfo']
    orderType = data['orderType']
    payType = data['payType']
    requestId = data['requestId']
    responseTime = data['responseTime']
    resultCode = data['resultCode']
    transId = data['transId']
    raw_signature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + \
                    "&message=" + message + "&orderId=" + orderId + "&orderInfo=" + orderInfo \
                    + "&orderType=" + orderType + "&partnerCode=" + partnerCode \
                    + "&payType=" + payType + "&requestId=" + requestId + "&responseTime=" + responseTime \
                    + "&resultCode=" + resultCode + "&transId=" + transId

    h = hmac.new(secretKey.encode('utf-8'), raw_signature.encode('utf-8'), hashlib.sha256)
    signature = h.hexdigest()
    msignature = data['signature']
    if signature == msignature:
        if resultCode == '0':
            pid = session['pid']
            utils.update_hoc_phi(pid)

####################
@app.route("/chunhiem", methods=['POST', 'GET'])
def chunhiem():
    id = session.get("pid")
    if id == 3:
        students = utils.load_class(id)
        return render_template('giaovien/chunhiem.html', students=students)
    return render_template('home.html')

@app.route("/listdiem")
def list_diem():
    diems = utils.load_diem()
    return render_template("giaovien/loaddiem.html",
                           diems=diems)

if __name__ == '__main__':
    app.run(debug=True)