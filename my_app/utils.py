from my_app import app, db
from my_app.models import *
from sqlalchemy import and_, func
from flask_login import current_user
import hashlib
import datetime


def add_user(hoTen, gioiTinh, ngaySinh, diaChi, email, username, password):
    password = str(hashlib.md5(password.encode("utf-8")).digest())
    ngaySinh = datetime(ngaySinh)
    user = Person(hoTen=hoTen,
                  gioiTinh=gioiTinh,
                  ngaySinh=ngaySinh,
                  diaChi=diaChi,
                  email=email,
                  username=username,
                  password=password)
    db.session.add(user)
    try:
        db.session.commit()
        return True
    except:
        return False

def stats_slhs_by_semester():
    return db.session.query(HocKy.namHoc, HocKy.maHK, HocKy.tenHK, func.count(HocPhi.id))\
            .join(HocPhi, HocPhi.hocKy_id==HocKy.maHK, isouter=True)\
            .group_by(HocKy.maHK, HocKy.tenHK).all()

def stats_fee_by_semester():
    return db.session.query(HocKy.namHoc, HocKy.maHK, HocKy.tenHK, func.count(HocPhi.id), func.sum(HocPhi.tongHocPhi)) \
        .join(HocPhi, HocPhi.hocKy_id == HocKy.maHK, isouter=True) \
        .where(HocPhi.tinhTrang==1)\
        .group_by(HocKy.maHK, HocKy.tenHK).all()

def stats_fee_by_year():
    return db.session.query(HocKy.namHoc, func.count(HocPhi.id), func.sum(HocPhi.tongHocPhi)) \
        .join(HocPhi, HocPhi.hocKy_id == HocKy.maHK, isouter=True) \
        .where(HocPhi.tinhTrang==1)\
        .group_by(HocKy.namHoc).all()

#######################
def get_student(lop_id=None):
    if lop_id:
        return HocSinh.query.filter(HocSinh.lop_id == int(lop_id))
    return Person.query.filter(Person.chucVu == 'HOC_SINH')

def get_student_new():
    st = db.session.execute("SELECT * FROM Person WHERE id  NOT IN "
                            "( SELECT id FROM HocSinh) AND chucVu = 'HOC_SINH'")
    return st

def get_student_by_id(student_id):
    return Person.query.get(int(student_id))

def add_person(hoTen, gioiTinh, ngaySinh, diaChi, email):
    password = str(hashlib.md5('123'.encode("utf-8")).digest())
    person = Person(
        hoTen=hoTen,
        gioiTinh=gioiTinh,
        ngaySinh=ngaySinh,
        diaChi=diaChi,
        email=email,
        username=hoTen,
        password=password
    )
    db.session.add(person)
    try:
        db.session.commit()
        return True
    except:
        return False

def update_student(student_id, hoTen, gioiTinh, ngaySinh, diaChi, email):
    password = str(hashlib.md5('123'.encode("utf-8")).digest())
    p = get_student_by_id(student_id)
    p.hoTen = hoTen
    p.gioiTinh = gioiTinh
    p.ngaySinh = ngaySinh
    p.diaChi = diaChi
    p.email = email
    p.username = hoTen
    p.password = password
    db.session.add(p)
    try:
        db.session.commit()
        return True
    except:
        return False

def delete_student(student_id):
    delete_Student_from_Class(student_id=student_id)
    db.session.execute('DELETE FROM HocPhi WHERE hocSinh_id = :val1', {'val1': student_id})
    db.session.execute('DELETE FROM Person WHERE id = :val1', {'val1': student_id})
    try:
        db.session.commit()
        return True
    except:
        return False

def get_Class(lop_id=None):
    if lop_id:
        return Lop.query.filter(Lop.maLop == int(lop_id))
    return Lop.query.all()

def get_Khoi():
    return KhoiLop.query.all()

def add_Class(maLop, tenLop, khoiLop_id):
    db.session.execute('INSERT INTO Lop(maLop, tenLop, siSo, khoiLop_id) VALUES (:val0, :val1, :val2, :val3)',
                       {'val0': maLop, 'val1': tenLop, 'val2': '0', 'val3': khoiLop_id})
    try:
        db.session.commit()
        return True
    except:
        return False

def delete_Class(lop_id):
    db.session.execute('DELETE FROM HocSinh WHERE lop_id = :val1', {'val1': lop_id})
    db.session.execute('DELETE FROM Lop WHERE maLop = :val2', {'val2': lop_id})
    try:
        db.session.commit()
        return True
    except:
        return False

def add_Student_to_Class(student_id, lop_id):
    db.session.execute('INSERT INTO HocSinh(id, lop_id) VALUES (:val1, :val2)', {'val1': student_id, 'val2': lop_id})
    db.session.execute('UPDATE Lop SET siSo = siSo + 1 WHERE maLop = :val1', {'val1': lop_id})
    db.session.execute(
        'INSERT INTO HocPhi(tongHocPhi, tinhTrang, hocSinh_id, hocKy_id) VALUES (:val1, :val2, :val3, :val4)',
        {'val1': '2000000', 'val2': '1', 'val3': student_id, 'val4': '1'})
    db.session.execute(
        'INSERT INTO HocPhi(tongHocPhi, tinhTrang, hocSinh_id, hocKy_id) VALUES (:val1, :val2, :val3, :val4)',
        {'val1': '3000000', 'val2': '1', 'val3': student_id, 'val4': '2'})
    try:
        db.session.commit()
        return True
    except:
        return False

def delete_Student_from_Class(student_id):
    db.session.execute('DELETE FROM HocPhi WHERE hocSinh_id = :val1', {'val1': student_id})
    db.session.execute('UPDATE Lop SET siSo = siSo-1 WHERE maLop = (select lop_id from HocSinh where id = :val1)',
                       {'val1': student_id})
    db.session.execute('DELETE FROM HocSinh WHERE id = :val1', {'val1': student_id})

    try:
        db.session.commit()
        return True
    except:
        return False

def pay_fee(hocky, student_id):
    db.session.execute('UPDATE HocPhi SET tinhTrang=0 WHERE hocKy_id= :val1 AND hocSinh_id= :val2',
                       {'val1': hocky,'val2': student_id})
    try:
        db.session.commit()
        return True
    except:
        return False

def get_tuition_list(hoTen=None, tinhTrang=None):
    if hoTen:
        list = db.session.execute("SELECT * FROM HocPhi,Person WHERE tinhTrang=1 "
                                  "AND HocPhi.hocSinh_id = Person.id AND hoTen = :val1", {'val1': hoTen})
    else:
        list = db.session.execute("SELECT * FROM HocPhi,Person WHERE tinhTrang= :val1 "
                                  "AND HocPhi.hocSinh_id = Person.id", {'val1': tinhTrang})
    return list

#################
def get_AllLop():
    return Lop.query.all()

def get_all_hoc_phi(id):
    return HocPhi.query.filter(and_(HocPhi.hocSinh_id == id, HocPhi.tinhTrang == 0)).all()

def update_hoc_phi(id):
    db.session.query(HocPhi).filter(HocPhi.hocSinh_id == id). update({HocPhi.tinhTrang: 1}, synchronize_session=False)
    db.session.commit()

def get_hoc_sinh(id):
    return HocSinh.query.filter(HocPhi.hocSinh_id == id).first()

######################Giao vien

def load_class(teacher_id): #list hs của lớp chủ nhiệm
    teacher = NhanVien.query.filter(NhanVien.id == teacher_id).first()

    listhocsinh = load_lisths(1) #teacher.lop_id
    return listhocsinh

def load_lisths(class_id): #list hs theo lop
    listhocsinh = HocSinh.query.filter(HocSinh.lop_id == class_id).all()
    return listhocsinh

def load_diem():
    st = db.session.execute("select hoTen, loaiDiem, CTDiem, hocKy_id FROM Diem "
                            "inner join thongtindiem on diem.maDiem=thongtindiem.diem_id "
                            "inner join person on thongtindiem.hocSinh_id=person.id")
    return st

