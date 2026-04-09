from django.urls import path

from poetry import views

urlpatterns = [
    # 响应自己写的诗
    path('write/', views.WritePoetry.as_view(), name='write'),

    # 响应唐诗宋词选读界面
    path('select/', views.SelectRead.as_view(), name='selectRead'),

    # 响应李白
    path('libai/', views.libai.as_view(), name='libai'),
    path('dufu/', views.dufu.as_view(), name='dufu'),
    path('dongpo/', views.dongpo.as_view(), name='dongpo'),
    path('jiaxuan/', views.jiaxuan.as_view(), name='jiaxuan'),
    path('chutang/', views.chutang.as_view(), name='chutang'),
    path('shengtang/', views.shengtang.as_view(), name='shengtang'),
    path('zhongtang/', views.zhongtang.as_view(), name='zhongtang'),
    path('wantang/', views.wantang.as_view(), name='wantang'),
    path('wudai/', views.wudai.as_view(), name='wudai'),
    path('beisong1/', views.beisong1.as_view(), name='beisong1'),
    path('beisong2/', views.beisong2.as_view(), name='beisong2'),
    path('nansong/', views.nansong.as_view(), name='nansong'),

    # http://localhost:4686/dynasty/search/?page=1&q=%E8%8D%89
    # path('search/<int:page>/',views.searchPoetry.as_view(), name='search_poetry_page'),
]
