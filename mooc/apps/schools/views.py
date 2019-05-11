# encoding: utf-8
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from courses.models import Course
from operation.models import UserFavorite
from .models import SchoolName, CityDict, Lecturer
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class SchoolView(View):
    def get(self, request):
        # 查找到所有的所属学校
        all_schools = SchoolName.objects.all()

        # 热门学校,如果不加负号会是有小到大。
        hot_schools = all_schools.order_by("-click_nums")[:3]
        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_schools = all_schools.filter(Q(name__icontains=search_keywords) | Q(
                desc__icontains=search_keywords) | Q(address__icontains=search_keywords))
        # 取出所有的城市
        all_city = CityDict.objects.all()

        # 取出筛选的城市,默认值为空
        city_id = request.GET.get('city', "")
        # 如果选择了某个城市,也就是前端传过来了值
        if city_id:
            # 外键city在数据中叫city_id
            # 我们就在学校中作进一步筛选
            all_schools = all_schools.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            # 我们就在学校中作进一步筛选类别
            all_schools = all_schools.filter(category=category)

        # 进行排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_schools = all_schools.order_by("-students")
            elif sort == "courses":
                all_schools = all_schools.order_by("-course_nums")

        # 总共有多少家学校使用count进行统计
        school_nums = all_schools.count()
        # 对学校进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allschool中取五个出来，每页显示5个
        p = Paginator(all_schools, 4, request=request)
        schools = p.page(page)

        return render(request, "school-list.html", {
            "all_schools": schools,
            "all_city": all_city,
            "school_nums": school_nums,
            "city_id": city_id,
            "category": category,
            "hot_schools": hot_schools,
            "sort": sort,
            "search_keywords": search_keywords,
        })


# class AddUserAskView(View):
#     """
#     用户添加咨询
#     """
#
#     def post(self, request):
#         userask_form = UserAskForm(request.POST)
#         if userask_form.is_valid():
#             user_ask = userask_form.save(commit=True)
#             return HttpResponse(
#                 '{"status":"success"}',
#                 content_type='application/json')
#         else:
#             return HttpResponse(
#                 '{"status":"fail", "msg":"您的字段有错误,请检查"}',
#                 content_type='application/json')


class SchoolHomeView(View):
    """
   学校首页
    """

    def get(self, request, school_id):
        # 向前端传值，表明现在在home页
        current_page = "home"
        # 根据id取到所属院校
        school_name = SchoolName.objects.get(id=int(school_id))
        school_name.click_nums += 1
        school_name.save()
        # 向前端传值说明用户是否收藏
        has_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user,
                    fav_id=school_name.id,
                    fav_type=2):
                has_fav = True
        # 通过所属院校找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = school_name.course_set.all()[:4]
        all_lecturer = school_name.lecturer_set.all()[:2]

        return render(request, 'school-detail-homepage.html', {
            'all_courses': all_courses,
            'all_lecturer': all_lecturer,
            'school_name': school_name,
            "current_page": current_page,
            "has_fav": has_fav
        })


class SchoolCourseView(View):
    """
   院校课程列表页
    """

    def get(self, request, school_id):
        # 向前端传值，表明现在在home页
        current_page = "course"
        # 根据id取到课程所在学校
        school_name = SchoolName.objects.get(id=int(school_id))
        # 通过课程所在学院找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = school_name.course_set.all()
        # 向前端传值说明用户是否收藏
        has_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user,
                    fav_id=school_name.id,
                    fav_type=2):
                has_fav = True
        return render(request, 'school-detail-course.html', {
            'all_courses': all_courses,
            'school_name': school_name,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class SchoolDescView(View):
    """
   学校描述详情页
    """

    def get(self, request, school_id):
        # 向前端传值，表明现在在home页
        current_page = "desc"
        # 根据id取到课程学校
        school_name = SchoolName.objects.get(id=int(school_id))
        # 通过学校找到课程。内建的变量，找到指向这个字段的外键引用
        # 向前端传值说明用户是否收藏
        has_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user,
                    fav_id=school_name.id,
                    fav_type=2):
                has_fav = True
        return render(request, 'school-detail-desc.html', {
            'school_name': school_name,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class SchoolLecturerView(View):
    """
   学校讲师列表页
    """

    def get(self, request, school_id):
        # 向前端传值，表明现在在home页
        current_page = "lecturer"
        # 根据id取到课程学校
        school_name = SchoolName.objects.get(id=int(school_id))
        # 通过课程所在学校找到课程。内建的变量，找到指向这个字段的外键引用
        all_lecturers = school_name.lecturer_set.all()
        # 向前端传值说明用户是否收藏
        has_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(
                    user=request.user,
                    fav_id=school_name.id,
                    fav_type=2):
                has_fav = True
        return render(request, 'school-detail-lecturers.html', {
            'all_lecturers': all_lecturers,
            'school_name': school_name,
            "current_page": current_page,
            "has_fav": has_fav
        })


class AddFavView(View):
    """
    用户收藏与取消收藏功能
    """

    def post(self, request):
        # 表明你收藏的不管是课程，讲师，还是学校。他们的id
        # 默认值取0是因为空串转int报错
        id = request.POST.get('fav_id', 0)
        # 取到你收藏的类别，从前台提交的ajax请求中取
        type = request.POST.get('fav_type', 0)

        # 收藏与已收藏取消收藏
        # 判断用户是否登录:即使没登录会有一个匿名的user
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse(
                '{"status":"fail", "msg":"用户未登录"}',
                content_type='application/json')
        exist_records = UserFavorite.objects.filter(
            user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2:
                school = SchoolName.objects.get(id=int(id))
                school.fav_nums -= 1
                if school.fav_nums < 0:
                    school.fav_nums = 0
                school.save()
            elif int(type) == 3:
                lecturer = Lecturer.objects.get(id=int(id))
                lecturer.fav_nums -= 1
                if lecturer.fav_nums < 0:
                    lecturer.fav_nums = 0
                lecturer.save()

            return HttpResponse(
                '{"status":"success", "msg":"收藏"}',
                content_type='application/json')
        else:
            user_fav = UserFavorite()
            # 过滤掉未取到fav_id type的默认情况
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()

                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    school = SchoolName.objects.get(id=int(id))
                    school.fav_nums += 1
                    school.save()
                elif int(type) == 3:
                    lecturer = Lecturer.objects.get(id=int(id))
                    lecturer.fav_nums += 1
                    lecturer.save()
                return HttpResponse(
                    '{"status":"success", "msg":"已收藏"}',
                    content_type='application/json')
            else:
                return HttpResponse(
                    '{"status":"fail", "msg":"收藏出错"}',
                    content_type='application/json')


class LecturerListView(View):
    """课程讲师列表页"""

    def get(self, request):
        all_lecturer = Lecturer.objects.all()
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_lecturer = all_lecturer.order_by("-click_nums")

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_lecturer = all_lecturer.filter(Q(name__icontains=search_keywords) | Q(
                work_company__icontains=search_keywords))

        # 排行榜讲师
        rank_lecturer = Lecturer.objects.all().order_by("-fav_nums")[:5]
        # 总共有多少老师使用count进行统计
        lecturer_nums = all_lecturer.count()
        # 对讲师进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allschool中取五个出来，每页显示5个
        p = Paginator(all_lecturer, 4, request=request)
        lecturers = p.page(page)
        return render(request, "lecturers-list.html", {
            "all_lecturer": lecturers,
            "lecturer_nums": lecturer_nums,
            "sort": sort,
            "rank_lecturers": rank_lecturer,
            "search_keywords": search_keywords,
        })


class LecturerDetailView(View):
    """教师详情页面"""

    def get(self, request, lecturer_id):
        lecturer = Lecturer.objects.get(id=int(lecturer_id))
        lecturer.click_nums += 1
        lecturer.save()
        all_course = lecturer.course_set.all()
        # 排行榜讲师
        rank_lecturer = Lecturer.objects.all().order_by("-fav_nums")[:5]

        has_fav_lecturer = False
        if UserFavorite.objects.filter(
                user=request.user,
                fav_type=3,
                fav_id=lecturer.id):
            has_fav_lecturer = True
        has_fav_school = False
        if UserFavorite.objects.filter(
                user=request.user,
                fav_type=2,
                fav_id=lecturer.school.id):
            has_fav_school = True
        return render(request, "lecturer-detail.html", {
            "lecturer": lecturer,
            "all_course": all_course,
            "rank_lecturer": rank_lecturer,
            "has_fav_lecturer": has_fav_lecturer,
            "has_fav_school": has_fav_school,
        })
