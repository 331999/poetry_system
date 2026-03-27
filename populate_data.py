#!/usr/bin/env python
"""
填充诗歌数据脚本
"""
import os
import sys
import django

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(__file__))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poetry_system.settings')
django.setup()

from poetry.models import Poetry

def populate_data():
    """填充诗歌数据"""

    # 1. 李白的数据
    print("正在添加李白的数据...")
    poems_libai = [
        {
            'poet_name': '李白',
            'poet_dynasty': '唐代',
            'poetry_name': '送友人',
            'poetry_info': '青山横北郭，白水绕东城。此地一为别，孤蓬万里征。\n浮云游子意，落日故人情。\n挥手自兹去，萧萧班马鸣。'
        },
        {
            'poet_name': '李白',
            'poet_dynasty': '唐代',
            'poetry_name': '将进酒',
            'poetry_info': '君不见，黄河之水天上来，奔流到海不复回。\n君不见，高堂明镜悲白发，朝如青丝暮成雪。\n人生得意须尽欢，莫使金樽空对月。\n天生我材必有用，千金散尽还复来。\n烹羊宰牛且为乐，会须一饮三百杯。'
        },
        {
            'poet_name': '李白',
            'poet_dynasty': '唐代',
            'poetry_name': '静夜思',
            'poetry_info': '床前明月光，疑是地上霜。\n举头望明月，低头思故乡。'
        },
        {
            'poet_name': '李白',
            'poet_dynasty': '唐代',
            'poetry_name': '月下独酌',
            'poetry_info': '花间一壶酒，独酌无相亲。\n举杯邀明月，对影成三人。\n月既不解饮，影徒随我身。\n暂伴月将影，行乐须及春。\n我歌月徘徊，我舞影零乱。\n醒时相交欢，醉后各分散。\n永结无情游，相期邈云汉。'
        },
    ]

    # 检查是否已有数据
    if Poetry.objects.filter(poet_name='李白').exists():
        print("李白的数据已存在，跳过。")
    else:
        for poem_data in poems_libai:
            Poetry.objects.create(**poem_data)
        print(f"✓ 成功添加 {len(poems_libai)} 首李白的诗")

    # 2. 杜甫的数据
    print("\n正在添加杜甫的数据...")
    poems_dufu = [
        {
            'poet_name': '杜甫',
            'poet_dynasty': '唐代',
            'poetry_name': '春望',
            'poetry_info': '国破山河在，城春草木深。\n感时花溅泪，恨别鸟惊心。\n烽火连三月，家书抵万金。\n白头搔更短，浑欲不胜簪。'
        },
        {
            'poet_name': '杜甫',
            'poet_dynasty': '唐代',
            'poetry_name': '登高',
            'poetry_info': '风急天高猿啸哀，渚清沙白鸟飞回。\n无边落木萧萧下，不尽长江滚滚来。\n万里悲秋常作客，百年多病独登台。\n艰难苦恨繁霜鬓，潦倒新停浊酒杯。'
        },
    ]

    if Poetry.objects.filter(poet_name='杜甫').exists():
        print("杜甫的数据已存在，跳过。")
    else:
        for poem_data in poems_dufu:
            Poetry.objects.create(**poem_data)
        print(f"✓ 成功添加 {len(poems_dufu)} 首杜甫的诗")

    # 3. 苏轼的数据
    print("\n正在添加苏轼的数据...")
    poems_dongpo = [
        {
            'poet_name': '苏轼',
            'poet_dynasty': '宋代',
            'poetry_name': '水调歌头·明月几时有',
            'poetry_info': '明月几时有？把酒问青天。\n不知天上宫阙，今夕是何年。\n我欲乘风归去，又恐琼楼玉宇，高处不胜寒。\n起舞弄清影，何似在人间。\n转朱阁，低绮户，照无眠。\n不应有恨，何事长向别时圆？\n人有悲欢离合，月有阴晴圆缺，此事古难全。\n但愿人长久，千里共婵娟。'
        },
        {
            'poet_name': '苏轼',
            'poet_dynasty': '宋代',
            'poetry_name': '念奴娇·赤壁怀古',
            'poetry_info': '大江东去，浪淘尽，千古风流人物。\n故垒西边，人道是，三国周郎赤壁。\n乱石穿空，惊涛拍岸，卷起千堆雪。\n江山如画，一时多少豪杰。\n遥想公瑾当年，小乔初嫁了，雄姿英发。\n羽扇纶巾，谈笑间，樯橹灰飞烟灭。\n故国神游，多情应笑我，早生华发。\n人生如梦，一尊还酹江月。'
        },
    ]

    if Poetry.objects.filter(poet_name='苏轼').exists():
        print("苏轼的数据已存在，跳过。")
    else:
        for poem_data in poems_dongpo:
            Poetry.objects.create(**poem_data)
        print(f"✓ 成功添加 {len(poems_dongpo)} 首苏轼的诗")

    # 4. 辛弃疾的数据
    print("\n正在添加辛弃疾的数据...")
    poems_jiaxuan = [
        {
            'poet_name': '辛弃疾',
            'poet_dynasty': '宋代',
            'poetry_name': '破阵子·为陈同甫赋壮词以寄之',
            'poetry_info': '醉里挑灯看剑，梦回吹角连营。\n八百里分麾下炙，五十弦翻塞外声，沙场秋点兵。\n马作的卢飞快，弓如霹雳弦惊。\n了却君王天下事，赢得生前身后名。\n可怜白发生！'
        },
    ]

    if Poetry.objects.filter(poet_name='辛弃疾').exists():
        print("辛弃疾的数据已存在，跳过。")
    else:
        for poem_data in poems_jiaxuan:
            Poetry.objects.create(**poem_data)
        print(f"✓ 成功添加 {len(poems_jiaxuan)} 首辛弃疾的诗")

    print("\n" + "=" * 60)
    print("数据填充完成！")
    print("=" * 60)

if __name__ == '__main__':
    populate_data()
