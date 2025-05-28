"""
五马循环计算器测试脚本
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.compatibility import CompatibilityData
from src.five_horses_calculator import FiveHorsesCalculator
import time


# def test_five_horses_calculator_basic():
#     """测试五马循环计算器基础功能"""
#     print("开始测试五马循环计算器基础功能...")
#     print("=" * 60)

#     # 记录开始时间
#     start_time = time.time()

#     # 初始化数据处理器和五马循环计算器
#     print("正在初始化相性数据处理器...")
#     data = CompatibilityData("data/相性数据表.csv")
    
#     print("正在初始化五马循环计算器...")
#     calculator = FiveHorsesCalculator(data)

#     # 获取所有可用的马娘列表
#     all_umas = list(data.get_all_umas())
#     print(f"共发现 {len(all_umas)} 只马娘可供选择")

#     # 测试案例1：指定组合计算
#     print("\n测试案例1：计算指定五马组合的相性点数")
#     print("-" * 50)
    
#     test_combination = {
#         'parent': "特别周",
#         'grandparent1': "无声铃鹿",
#         'grandparent2': "草上飞",
#         'chromo1': "神鹰",
#         'chromo2': "小栗帽"
#     }
    
#     print(f"测试组合:")
#     print(f"  目标马娘 (Parent): {test_combination['parent']}")
#     print(f"  祖父马娘1 (Grandparent1): {test_combination['grandparent1']}")
#     print(f"  祖父马娘2 (Grandparent2): {test_combination['grandparent2']}")
#     print(f"  染色体马娘1 (Chromo1): {test_combination['chromo1']}")
#     print(f"  染色体马娘2 (Chromo2): {test_combination['chromo2']}")
    
#     score = calculator.calculate_specific_combination(
#         parent=test_combination['parent'],
#         grandparent1=test_combination['grandparent1'],
#         grandparent2=test_combination['grandparent2'],
#         chromo1=test_combination['chromo1'],
#         chromo2=test_combination['chromo2']
#     )
#     print(f"\n指定组合的相性点数: {score}")

#     # 测试案例2：另一个指定组合
#     print("\n测试案例2：另一个指定组合")
#     print("-" * 50)
    
#     test_combination_2 = {
#         'parent': "丸善斯基",
#         'grandparent1': "鲁道夫象征",
#         'grandparent2': "目白麦昆",
#         'chromo1': "稻荷一",
#         'chromo2': "伏特加"
#     }
    
#     print(f"测试组合:")
#     print(f"  目标马娘 (Parent): {test_combination_2['parent']}")
#     print(f"  祖父马娘1 (Grandparent1): {test_combination_2['grandparent1']}")
#     print(f"  祖父马娘2 (Grandparent2): {test_combination_2['grandparent2']}")
#     print(f"  染色体马娘1 (Chromo1): {test_combination_2['chromo1']}")
#     print(f"  染色体马娘2 (Chromo2): {test_combination_2['chromo2']}")
    
#     score_2 = calculator.calculate_specific_combination(
#         parent=test_combination_2['parent'],
#         grandparent1=test_combination_2['grandparent1'],
#         grandparent2=test_combination_2['grandparent2'],
#         chromo1=test_combination_2['chromo1'],
#         chromo2=test_combination_2['chromo2']
#     )
#     print(f"\n指定组合的相性点数: {score_2}")

#     # 输出基础测试用时
#     basic_time = time.time() - start_time
#     print(f"\n基础功能测试用时: {basic_time:.2f} 秒")


def test_five_horses_calculator_optimization():
    """测试五马循环计算器优化功能"""
    print("\n开始测试五马循环计算器优化功能...")
    print("=" * 60)

    # 记录开始时间
    start_time = time.time()

    # 初始化数据处理器和五马循环计算器
    print("正在初始化数据处理器...")
    data = CompatibilityData("data/相性数据表.csv")
    calculator = FiveHorsesCalculator(data)

    # 测试案例1：计算最优组合（使用热门马娘）
    print("\n测试案例1：计算特别周的最优五马组合")
    print("-" * 50)
    
    target_parent = "特别周"
    print(f"目标马娘: {target_parent}")
    
    opt_start_time = time.time()
    best_combination, best_score = calculator.calculate_best_combination(
        parent=target_parent,
        verbose=True
    )
    opt_time = time.time() - opt_start_time
    
    print(f"\n最优组合计算用时: {opt_time:.2f} 秒")
    calculator.display_result(best_combination, best_score)

    # 测试案例2：获取前5个最优组合
    print(f"\n测试案例2：获取{target_parent}的前5个最优组合")
    print("-" * 50)
    
    top_start_time = time.time()
    top_results = calculator.get_top_combinations(
        parent=target_parent,
        top_n=5,
        verbose=True
    )
    top_time = time.time() - top_start_time
    
    print(f"\n前5优组合计算用时: {top_time:.2f} 秒")
    calculator.display_top_results(top_results)

    # 测试案例3：另一只马娘的最优组合
    print(f"\n测试案例3：计算丸善斯基的最优五马组合")
    print("-" * 50)
    
    target_parent_2 = "丸善斯基"
    print(f"目标马娘: {target_parent_2}")
    
    best_combination_2, best_score_2 = calculator.calculate_best_combination(
        parent=target_parent_2,
        verbose=True
    )
    
    calculator.display_result(best_combination_2, best_score_2)

    # # 测试案例4：比较不同马娘的最优分数
    # print(f"\n测试案例4：比较不同马娘的最优分数")
    # print("-" * 50)
    
    # comparison_targets = ["目白麦昆", "东海帝王", "无声铃鹿", "草上飞"]
    # comparison_results = []
    
    # for target in comparison_targets:
    #     print(f"正在计算 {target} 的最优组合...")
    #     best_combo, best_score = calculator.calculate_best_combination(
    #         parent=target,
    #         verbose=False  # 关闭详细输出以提高速度
    #     )
    #     comparison_results.append((target, best_score, best_combo))
    
    # print("\n各马娘最优分数对比:")
    # print("-" * 60)
    # comparison_results.sort(key=lambda x: x[1], reverse=True)
    # for i, (target, score, combo) in enumerate(comparison_results, 1):
    #     print(f"第{i}名: {target} - 最优分数: {score}")
    #     print(f"    最优组合: GP1={combo['grandparent1']}, GP2={combo['grandparent2']}")
    #     print(f"             C1={combo['chromo1']}, C2={combo['chromo2']}")

    # 输出优化测试用时
    optimization_time = time.time() - start_time
    print(f"\n优化功能测试总用时: {optimization_time:.2f} 秒")


def test_five_horses_calculator_edge_cases():
    """测试五马循环计算器边界情况"""
    print("\n开始测试五马循环计算器边界情况...")
    print("=" * 60)

    # 初始化数据处理器和五马循环计算器
    data = CompatibilityData("data/相性数据表.csv")
    calculator = FiveHorsesCalculator(data)

    # 测试案例1：错误输入处理
    print("\n测试案例1：错误输入处理")
    print("-" * 40)
    
    # 测试不存在的马娘
    try:
        calculator.calculate_best_combination(parent="不存在的马娘")
        print("错误：应该抛出异常但没有")
    except ValueError as e:
        print(f"✓ 正确处理不存在的马娘: {e}")
    
    # 测试重复马娘
    try:
        calculator.calculate_specific_combination(
            parent="特别周",
            grandparent1="特别周",  # 与parent重复
            grandparent2="草上飞",
            chromo1="神鹰",
            chromo2="小栗帽"
        )
        print("错误：应该抛出异常但没有")
    except ValueError as e:
        print(f"✓ 正确处理重复马娘: {e}")

    # 测试案例2：验证映射关系的正确性
    print("\n测试案例2：验证映射关系")
    print("-" * 40)
    
    # 手动计算相同组合的分数，验证映射关系
    from src.calculator import CompatibilityCalculator
    manual_calculator = CompatibilityCalculator(data)
    
    test_horses = {
        'parent': "目白麦昆",
        'grandparent1': "鲁道夫象征", 
        'grandparent2': "东海帝王",
        'chromo1': "稻荷一",
        'chromo2': "特别周"
    }
    
    # 使用五马循环计算器
    score_five_horses = calculator.calculate_specific_combination(
        parent=test_horses['parent'],
        grandparent1=test_horses['grandparent1'],
        grandparent2=test_horses['grandparent2'],
        chromo1=test_horses['chromo1'],
        chromo2=test_horses['chromo2']
    )
    
    # 使用底层七马计算器（手动映射）
    score_manual = manual_calculator.calculate_compatibility_score(
        target=test_horses['parent'],           # parent -> target
        parent1=test_horses['grandparent1'],   # grandparent1 -> parent1
        parent2=test_horses['grandparent2'],   # grandparent2 -> parent2  
        grandparent1=test_horses['chromo1'],   # chromo1 -> grandparent1
        grandparent2=test_horses['chromo2'],   # chromo2 -> grandparent2
        grandparent3=test_horses['chromo2'],   # chromo2 -> grandparent3
        grandparent4=test_horses['grandparent1'], # grandparent1 -> grandparent4
        verbose=False
    )
    
    print(f"五马循环计算器结果: {score_five_horses}")
    print(f"手动映射计算结果: {score_manual}")
    print(f"映射关系验证: {'✓ 正确' if score_five_horses == score_manual else '✗ 错误'}")

    print("\n边界情况测试完成！")


if __name__ == "__main__":
    # 选择要运行的测试
    print("五马循环计算器测试脚本")
    print("=" * 40)
    print("选择要运行的测试:")
    print("1. 优化功能测试") 
    print("2. 边界情况测试")
    print("3. 运行所有测试")

    choice = input("请输入选择 (1/2/3): ").strip()

    if choice == "1":
        test_five_horses_calculator_optimization()
    elif choice == "2":
        test_five_horses_calculator_edge_cases()
    elif choice == "3":
        test_five_horses_calculator_optimization()
        test_five_horses_calculator_edge_cases()
        print("\n" + "=" * 80)
        print("所有测试完成！")
    else:
        print("无效选择，运行所有测试...")
        test_five_horses_calculator_optimization()
        test_five_horses_calculator_edge_cases()
        print("\n" + "=" * 80)
        print("所有测试完成！")
