#!/usr/bin/env python
"""
诊断脚本 - 检查数据库和Poetry模型数据
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

print("=" * 60)
print("数据库诊断报告")
print("=" * 60)

# 1. 检查数据库连接
try:
    total_poems = Poetry.objects.count()
    print(f"\n✓ 数据库连接正常")
    print(f"  Poetry表中的记录总数: {total_poems}")

    # 2. 检查李白的数据
    if total_poems > 0:
        libai_count = Poetry.objects.filter(poet_name='李白').count()
        print(f"\n李白 (李白): {libai_count} 首诗")

        if libai_count > 0:
            libai_poems = list(Poetry.objects.filter(poet_name='李白')[:3].values('poetry_name', 'poet_dynasty'))
            print(f"  示例:")
            for poem in libai_poems:
                print(f"    - {poem['poetry_name']} ({poem['poet_dynasty']})")
        else:
            print(f"  ⚠ 警告: 数据库中没有名为'李白'的诗人")

        # 3. 检查杜甫的数据
        dufu_count = Poetry.objects.filter(poet_name='杜甫').count()
        print(f"\n杜甫 (杜甫): {dufu_count} 首诗")

        if dufu_count > 0:
            dufu_poems = list(Poetry.objects.filter(poet_name='杜甫')[:3].values('poetry_name', 'poet_dynasty'))
            print(f"  示例:")
            for poem in dufu_poems:
                print(f"    - {poem['poetry_name']} ({poem['poet_dynasty']})")
        else:
            print(f"  ⚠ 警告: 数据库中没有名为'杜甫'的诗人")

        # 4. 检查苏轼的数据
        dongpo_count = Poetry.objects.filter(poet_name='苏轼').count()
        print(f"\n苏轼 (东坡): {dongpo_count} 首诗")

        if dongpo_count > 0:
            dongpo_poems = list(Poetry.objects.filter(poet_name='苏轼')[:3].values('poetry_name', 'poet_dynasty'))
            print(f"  示例:")
            for poem in dongpo_poems:
                print(f"    - {poem['poetry_name']} ({poem['poet_dynasty']})")
        else:
            print(f"  ⚠ 警告: 数据库中没有名为'苏轼'的诗人")

        # 5. 检查辛弃疾的数据
        jiaxuan_count = Poetry.objects.filter(poet_name='辛弃疾').count()
        print(f"\n辛弃疾 (稼轩): {jiaxuan_count} 首诗")

        if jiaxuan_count > 0:
            jiaxuan_poems = list(Poetry.objects.filter(poet_name='辛弃疾')[:3].values('poetry_name', 'poet_dynasty'))
            print(f"  示例:")
            for poem in jiaxuan_poems:
                print(f"    - {poem['poetry_name']} ({poem['poet_dynasty']})")
        else:
            print(f"  ⚠ 警告: 数据库中没有名为'辛弃疾'的诗人")

        # 6. 检查所有唯一的诗人
        all_poets = list(Poetry.objects.values('poet_name').distinct())
        print(f"\n数据库中的所有诗人 ({len(all_poets)} 位):")
        for poet in all_poets:
            print(f"  - {poet['poet_name']}")
    else:
        print(f"\n⚠ 警告: Poetry表为空！没有诗歌数据。")

except Exception as e:
    print(f"\n✗ 数据库连接错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("诊断完成")
print("=" * 60)
