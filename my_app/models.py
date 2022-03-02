from my_app import db
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
import enum
from flask_login import UserMixin

class MyRole(enum.Enum):
    BAN_GIAM_HIEU = 1
    GIAO_VU = 2
    GIAO_VIEN = 3
    HOC_SINH = 4

class Person(db.Model, UserMixin):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50), nullable=False)
    gioiTinh = Column(String(5), nullable=False)
    ngaySinh = Column(DateTime, nullable=False)
    diaChi = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    chucVu = Column(Enum(MyRole), default=MyRole.HOC_SINH)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    def __str__(self):
        return self.hoTen

class HocSinh(Person):
    __tablename__ = 'hocsinh'
    id = Column(Integer, ForeignKey(Person.id), primary_key=True)
    lop_id = Column(Integer, ForeignKey('lop.maLop'))
    dsThongTinMon = relationship('ThongTinMon', backref='hocSinh', lazy=True)
    dsHocPhi = relationship('HocPhi', backref='hocSinh', lazy=True)


nv_lop = db.Table('nv_lop',
                  Column('nv_id', Integer, ForeignKey('nhanvien.id'), primary_key=True),
                  Column('lop_id', Integer, ForeignKey('lop.maLop'), primary_key=True))

nv_mon = db.Table('nv_mon',
                        Column('nv_id', Integer,
                               ForeignKey('nhanvien.id'),
                               primary_key=True),
                        Column('m_id', Integer,
                               ForeignKey('mon.maMon'),
                               primary_key=True))

class NhanVien(Person):
    __tablename__ = 'nhanvien'
    id = Column(Integer, ForeignKey(Person.id), primary_key=True)
    dsLop = relationship('Lop', secondary='nv_lop', lazy='subquery', backref=backref('dsNhanVien', lazy=True))
    dsMon = relationship('Mon', secondary='nv_mon', lazy='subquery', backref=backref('dsnhanvien', lazy=True))

class KhoiLop(db.Model):
    __tablename__ = 'khoilop'
    maKhoi = Column(Integer, primary_key=True, autoincrement=True)
    tenKhoi = Column(String(10), nullable=False, unique=True)
    dsLop = relationship('Lop', backref='khoiLop', lazy=True)
    def __str__(self):
        return self.tenKhoi

class Lop(db.Model):
    __tablename__ = 'lop'
    maLop = Column(Integer, primary_key=True, autoincrement=True)
    tenLop = Column(String(50), nullable=False, unique=True)
    siSo = Column(Integer, nullable=False, default=0)
    khoiLop_id = Column(Integer, ForeignKey(KhoiLop.maKhoi), nullable=False)
    dsHocSinh = relationship('HocSinh', backref='lop', lazy=True)
    def __str__(self):
        return self.tenLop

class Mon(db.Model):
    __tablename__ = 'mon'
    maMon = Column(Integer, primary_key=True, autoincrement=True)
    tenMon = Column(String(50), nullable=False, unique=True)
    dsThongTinMon = relationship('ThongTinMon', backref='mon', lazy=True)
    def __str__(self):
        return self.tenMon

class HocKy(db.Model):
    __tablename__ = 'hocky'
    maHK = Column(Integer, primary_key=True, autoincrement=True)
    tenHK = Column(String(20), nullable=False)
    namHoc = Column(Integer, nullable=False)
    dsThongTinMon = relationship('ThongTinMon', backref='hocky', lazy=True)
    dsHocPhi = relationship('HocPhi', backref='hocky', lazy=True)
    def __str__(self):
        return self.tenHK

class ThongTinMon(db.Model):
    __tablename__ = 'thongtinmon'
    hocSinh_id = Column(Integer, ForeignKey(HocSinh.id), primary_key=True)
    mon_id = Column(Integer, ForeignKey(Mon.maMon), primary_key=True)
    hocKy_id = Column(Integer, ForeignKey(HocKy.maHK), primary_key=True)
    dsThongTinDiem = relationship('ThongTinDiem',
                                  primaryjoin="and_(ThongTinMon.hocSinh_id == ThongTinDiem.hocSinh_id, "
                                              "ThongTinMon.mon_id == ThongTinDiem.mon_id, "
                                              "ThongTinMon.hocKy_id == ThongTinDiem.hocKy_id)",
                                  backref='thongTinMon', lazy=True)

class Diem(db.Model):
    __tablename__ = 'diem'
    maDiem = Column(Integer, primary_key=True, autoincrement=True)
    loaiDiem = Column(String(50), nullable=False)
    dsThongTinDiem = relationship('ThongTinDiem', backref='loaiDiem', lazy=True)
    def __str__(self):
        return self.loaiDiem

class ThongTinDiem(db.Model):
    __tablename__ = 'thongtindiem'
    maTTD = Column(Integer, primary_key=True, autoincrement=True)
    diem_id = Column(Integer, ForeignKey(Diem.maDiem), nullable=False)
    CTDiem = Column(Float, nullable=False)
    hocSinh_id = Column(Integer, ForeignKey(ThongTinMon.hocSinh_id), nullable=False)
    mon_id = Column(Integer, ForeignKey(ThongTinMon.mon_id), nullable=False)
    hocKy_id = Column(Integer, ForeignKey(ThongTinMon.hocKy_id), nullable=False)

class QuiDinh(db.Model):
    __tablename__ = 'quidinh'
    maQD = Column(Integer, primary_key=True, autoincrement=True)
    noiDungQD = Column(String(200), nullable=False)
    chiTietQuiDinh = relationship('CTQuiDinh', backref='quidinh', lazy=True, uselist=False)
    def __str__(self):
        return self.noiDungQD

class CTQuiDinh(db.Model):
    __tablename__ = 'ctquidinh'
    noiDung = Column(Integer, nullable=False)
    quiDinh_id = Column(Integer, ForeignKey(QuiDinh.maQD), primary_key=True)

class HocPhi(db.Model):
    __tablename__ = 'hocphi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tongHocPhi = Column(Integer, nullable=False)
    tinhTrang = Column(Boolean, default=0)
    hocSinh_id = Column(Integer, ForeignKey(HocSinh.id))
    hocKy_id = Column(Integer, ForeignKey(HocKy.maHK))

if __name__ == '__main__':
    db.create_all()