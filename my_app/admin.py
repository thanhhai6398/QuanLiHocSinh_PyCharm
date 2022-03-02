from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request
from my_app.models import Person, HocSinh, NhanVien, KhoiLop, Lop, HocKy, HocPhi, ThongTinMon, ThongTinDiem, QuiDinh, CTQuiDinh, Diem, Mon
from my_app import db, app, utils


class MyAdminIndex(AdminIndexView):
    @expose("/")
    def __index__(self):
        stats = utils.stats_slhs_by_semester()
        return self.render('admin/index.html', stats=stats)

admin = Admin(app=app,
              name="QLHS",
              template_mode="bootstrap4",
              index_view=MyAdminIndex())

class AuthenticatedView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            return current_user.is_authenticated
        return False

class PersonModelView(AuthenticatedView):
    can_export = True
    column_searchable_list = ['hoTen', 'gioiTinh', 'ngaySinh', 'diaChi', 'email', 'chucVu', 'username']
    column_filters = []
    page_size = 50

class HocSinhModelView(AuthenticatedView):
    column_searchable_list = ['hoTen', 'gioiTinh', 'ngaySinh', 'diaChi', 'email', 'chucVu', 'username']
    can_export = True

class NhanVienModelView(AuthenticatedView):
    column_searchable_list = ['hoTen', 'gioiTinh', 'ngaySinh', 'diaChi', 'email', 'chucVu', 'username']
    can_export = True

class LopModelView(AuthenticatedView):
    column_searchable_list = ['tenLop', 'siSo']
    can_export = True

class MonModelView(AuthenticatedView):
    column_searchable_list = ['tenMon']
    can_export = True

class HocKyModelView(AuthenticatedView):
    column_searchable_list = ['tenHK', 'namHoc']
    can_export = True

class ThongTinMonModelView(AuthenticatedView):
    can_export = True

class DiemModelView(AuthenticatedView):
    can_export = True

class ThongTinDiemModelView(AuthenticatedView):
    can_export = True

class QuiDinhModelView(AuthenticatedView):
    column_searchable_list = ['noiDungQD']
    can_export = True

class CTQuiDinhModelView(AuthenticatedView):
    can_export = True

class HocPhiModelView(AuthenticatedView):
    column_searchable_list = ['tongHocPhi', 'tinhTrang']
    can_export = True


class StatsView(BaseView):
    @expose("/")
    def __index__(self):
        stats = utils.stats_fee_by_semester()
        return self.render("admin/thongke.html", stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated

class StatsViewByYear(BaseView):
    @expose("/")
    def __index__(self):
        stats = utils.stats_fee_by_year()
        return self.render("admin/thongketheonam.html", stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(BaseView):
    @expose("/")
    def __index__(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(PersonModelView(Person, db.session, name="Người dùng"))
admin.add_view(HocSinhModelView(HocSinh, db.session, name="Học sinh"))
#admin.add_view(ModelView(nv_lop, db.session))
#admin.add_view(ModelView(nv_mon, db.session))
admin.add_view(NhanVienModelView(NhanVien, db.session, name="Đội ngũ"))
admin.add_view(AuthenticatedView(KhoiLop, db.session, name="Khối lớp"))
admin.add_view(LopModelView(Lop, db.session, name="Lớp"))
admin.add_view(MonModelView(Mon, db.session, name="Môn"))
admin.add_view(HocKyModelView(HocKy, db.session, name="Học kỳ"))
admin.add_view(ThongTinMonModelView(ThongTinMon, db.session, name="Thông tin môn"))
admin.add_view(DiemModelView(Diem, db.session, name="Điểm"))
admin.add_view(ThongTinDiemModelView(ThongTinDiem, db.session, name="Thông tin điểm"))
admin.add_view(QuiDinhModelView(QuiDinh, db.session, name="Quy định"))
admin.add_view(CTQuiDinhModelView(CTQuiDinh, db.session, name="Chi tiết quy định"))
admin.add_view(HocPhiModelView(HocPhi, db.session, name="Học phí"))

admin.add_view(StatsView(name="Thống kê doanh thu học phí"))
admin.add_view(StatsViewByYear(name=""))
admin.add_view(LogoutView(name="Đăng xuất"))