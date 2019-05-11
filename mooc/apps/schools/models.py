from django.db import models
from datetime import datetime


class CityDict(models.Model):
    """城市字典"""
    name = models.CharField(max_length=20, verbose_name=u"城市")
    # 城市描述：备用不一定展示出来
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SchoolName(models.Model):
    """学校名称"""
    # ORG_CHOICES = (
    #     #     ("pxjg", u"培训机构"),
    #     #     ("gx", u"高校"),
    #     #     ("gr", u"个人"),
    #     # )

    Name_CHOICES = (
        ("one", u"国内名校"),
        ("two", u"普通本科院校"),
        ("three", u"普通专科院校"),
    )

    name = models.CharField(max_length=50, verbose_name=u"学校名称")
    # 学校描述，后面会替换为富文本展示
    desc = models.TextField(verbose_name=u"学校描述")
    # 学校类别:
    category = models.CharField(max_length=20, choices=Name_CHOICES, verbose_name=u"学校类别", default="one")
    tag = models.CharField(max_length=10, default=u"国内名校", verbose_name=u"学校标签")
    # 不需要学校的点击数和收藏数
    # click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    # fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(
        upload_to="org/%Y/%m",
        verbose_name=u"Logo",
        max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"学校地址")
    # 一个城市可以有很多学校，通过将city设置外键，变成学校的一个字段
    # 可以让我们通过学校找到城市
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name=u"所在城市")
    # 当学生点击学习课程，找到所属学校，学习人数加1
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    # 当发布课程就加1
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"学校名称"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "学校名称: {0}".format(self.name)


class Lecturer(models.Model):
    """讲师"""
    # 一个学校会有很多老师，所以我们在讲师表添加外键并把学校名称保存下来
    # 可以使我们通过讲师找到对应的学校
    org = models.ForeignKey(SchoolName, on_delete=models.CASCADE, verbose_name=u"所属学校")
    name = models.CharField(max_length=50, verbose_name=u"教师名称")
    work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
    # 这里去掉了就职公司
    # work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"职称")
    age = models.IntegerField(default=18, verbose_name=u"年龄")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(
        default='',
        upload_to="teacher/%Y/%m",
        verbose_name=u"头像",
        max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"讲师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[{0}]的讲师: {1}".format(self.org, self.name)

