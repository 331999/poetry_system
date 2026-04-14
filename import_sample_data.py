# -*- coding: utf-8 -*-
"""
示例数据导入脚本
从JSON文件导入古诗词数据到Neo4j
"""

import json
import os
from neo4j_data_manager import Neo4jDataManager


def import_sample_data():
    """导入示例数据"""
    
    print("\n" + "="*60)
    print("Neo4j 示例数据导入工具")
    print("="*60 + "\n")
    
    # 检查JSON文件是否存在
    json_file = 'sample_poetry_data.json'
    if not os.path.exists(json_file):
        print(f"✗ 错误：找不到数据文件 {json_file}")
        print(f"  请确保文件存在于当前目录")
        return
    
    # 读取JSON数据
    print(f"正在读取数据文件: {json_file}")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            poets_data = json.load(f)
        print(f"✓ 成功读取 {len(poets_data)} 位诗人的数据\n")
    except Exception as e:
        print(f"✗ 读取数据文件失败: {e}")
        return
    
    # 连接Neo4j
    print("正在连接Neo4j数据库...")
    try:
        manager = Neo4jDataManager()
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        print("\n请检查：")
        print("  1. Neo4j服务是否已启动")
        print("  2. 连接地址是否正确")
        print("  3. 用户名和密码是否正确")
        return
    
    # 显示统计信息（导入前）
    print("\n导入前的数据库统计：")
    manager.print_statistics()
    
    # 确认导入
    print(f"\n准备导入 {len(poets_data)} 位诗人的数据：")
    for i, poet in enumerate(poets_data, 1):
        poetries_count = len(poet.get('poetries', []))
        works_count = len(poet.get('works', []))
        print(f"  {i}. {poet['name']} ({poet['dynasty']}) - {poetries_count}首诗, {works_count}部著作")
    
    confirm = input("\n是否继续导入？(y/n): ")
    if confirm.lower() != 'y':
        print("已取消导入")
        return
    
    # 开始导入
    print("\n开始导入数据...\n")
    print("="*60)
    
    success_count = 0
    failed_count = 0
    
    for poet_data in poets_data:
        try:
            manager.add_poet_complete(poet_data)
            success_count += 1
        except Exception as e:
            print(f"✗ 导入失败: {poet_data['name']} - {e}")
            failed_count += 1
    
    print("="*60)
    
    # 显示统计信息（导入后）
    print("\n导入后的数据库统计：")
    manager.print_statistics()
    
    # 导入结果
    print("\n" + "="*60)
    print("导入完成！")
    print("="*60)
    print(f"成功导入: {success_count} 位诗人")
    if failed_count > 0:
        print(f"导入失败: {failed_count} 位诗人")
    print("="*60 + "\n")
    
    # 验证导入
    print("正在验证导入结果...\n")
    
    # 查询几位诗人验证
    sample_poets = ["李白", "杜甫", "苏轼"]
    for poet_name in sample_poets:
        info = manager.get_poet_info(poet_name)
        if info:
            poetries = manager.get_poet_poetries(poet_name)
            print(f"✓ {poet_name}: {len(poetries)} 首诗歌")
        else:
            print(f"✗ {poet_name}: 未找到")
    
    print("\n✓✓✓ 示例数据导入完成！")
    print("\n你现在可以：")
    print("  1. 在Neo4j Browser中查看数据 (http://localhost:7474)")
    print("  2. 使用neo4j_data_manager.py查询数据")
    print("  3. 在问答系统中测试效果")


def show_menu():
    """显示菜单"""
    print("\n" + "="*60)
    print("Neo4j 数据管理工具")
    print("="*60)
    print("\n请选择操作：")
    print("  1. 导入示例数据")
    print("  2. 查看数据库统计")
    print("  3. 查询所有诗人")
    print("  4. 清空数据库（危险操作）")
    print("  0. 退出")
    print("="*60)


def main():
    """主函数"""
    
    while True:
        show_menu()
        choice = input("\n请输入选项 (0-4): ").strip()
        
        if choice == '1':
            import_sample_data()
        
        elif choice == '2':
            try:
                manager = Neo4jDataManager()
                manager.print_statistics()
            except Exception as e:
                print(f"✗ 连接失败: {e}")
        
        elif choice == '3':
            try:
                manager = Neo4jDataManager()
                poets = manager.get_all_poets()
                print(f"\n共有 {len(poets)} 位诗人：")
                for i, poet in enumerate(poets, 1):
                    print(f"  {i}. {poet}")
            except Exception as e:
                print(f"✗ 查询失败: {e}")
        
        elif choice == '4':
            print("\n⚠️  警告：此操作将删除所有数据！")
            confirm = input("请输入 'DELETE ALL' 确认删除: ")
            if confirm == 'DELETE ALL':
                try:
                    manager = Neo4jDataManager()
                    manager.graph.delete_all()
                    print("✓ 数据库已清空")
                except Exception as e:
                    print(f"✗ 清空失败: {e}")
            else:
                print("已取消操作")
        
        elif choice == '0':
            print("\n再见！")
            break
        
        else:
            print("✗ 无效选项，请重新选择")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    main()
