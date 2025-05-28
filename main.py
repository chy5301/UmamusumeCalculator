# 初始化数据处理器
from src.compatibility import CompatibilityData
from src.calculator import CompatibilityCalculator
import time


def test_compatibility_calculator():
    print("开始测试相性数据处理器...")

    # 记录开始时间
    start_time = time.time()

    # 初始化数据处理器
    print("正在初始化相性数据处理器...")
    data = CompatibilityData("data/相性数据表.csv")

    # 测试一些已知的马娘组合
    test_pairs = [
        ("特别周", "无声铃鹿"),
        ("特别周", "草上飞"),
        ("特别周", "神鹰"),
        ("特别周", "小栗帽"),
    ]

    test_triples = [
        ("特别周", "无声铃鹿", "小栗帽"),
        ("特别周", "草上飞", "神鹰"),
        ("特别周", "目白麦昆", "东海帝王"),
    ]

    print("\n测试两两相性:")
    print("-" * 50)
    for uma1, uma2 in test_pairs:
        score = data.get_pair_compatibility(uma1, uma2)
        print(f"{uma1} 和 {uma2} 的相性分数: {score}")

    print("\n测试三三相性:")
    print("-" * 50)
    for uma1, uma2, uma3 in test_triples:
        score = data.get_triple_compatibility(uma1, uma2, uma3)
        print(f"{uma1}、{uma2} 和 {uma3} 的相性分数: {score}")

    # 测试缓存功能
    print("\n测试缓存功能:")
    print("-" * 50)
    print("重新初始化相性数据处理器（应该从缓存加载）...")
    cache_start_time = time.time()
    data2 = CompatibilityData("data/相性数据表.csv")
    cache_time = time.time() - cache_start_time
    print(f"从缓存加载用时: {cache_time:.2f} 秒")

    # 验证两次加载的结果是否一致
    test_uma = "特别周"
    score1 = data.get_pair_compatibility(test_uma, "无声铃鹿")
    score2 = data2.get_pair_compatibility(test_uma, "无声铃鹿")
    print(f"\n验证缓存数据一致性:")
    print(f"第一次加载的分数: {score1}")
    print(f"第二次加载的分数: {score2}")
    print(f"数据一致性: {'一致' if score1 == score2 else '不一致'}")

    # 输出总用时
    total_time = time.time() - start_time
    print(f"\n总用时: {total_time:.2f} 秒")


def test_compatibility_calculator_advanced():
    """测试相性计算器"""
    print("开始测试相性计算器...")
    print("=" * 60)

    # 初始化数据处理器和计算器
    print("正在初始化数据处理器...")
    data = CompatibilityData("data/相性数据表.csv")
    calculator = CompatibilityCalculator(data)

    # 测试案例1：经典组合
    print("\n测试案例1：经典组合")
    print("-" * 40)
    test_horses_1 = [
        "特别周",  # target
        "无声铃鹿",  # parent1
        "草上飞",  # parent2
        "神鹰",  # grandparent1
        "小栗帽",  # grandparent2
        "目白麦昆",  # grandparent3
        "东海帝王",  # grandparent4
    ]

    total_score_1 = calculator.calculate_compatibility_score_simple(test_horses_1)
    print(f"案例1总分: {total_score_1}")

    # 测试案例2：另一个组合
    print("\n测试案例2：另一个组合")
    print("-" * 40)
    test_horses_2 = [
        "丸善斯基",  # target
        "鲁道夫象征",  # parent1
        "目白麦昆",  # parent2
        "稻荷一",  # grandparent1
        "小栗帽",  # grandparent2
        "东海帝王",  # grandparent3
        "伏特加",  # grandparent4
    ]

    total_score_2 = calculator.calculate_compatibility_score_simple(test_horses_2)
    print(f"案例2总分: {total_score_2}")

    print("\n相性计算器测试完成！")


if __name__ == "__main__":
    # 可以选择运行哪个测试
    print("选择要运行的测试:")
    print("1. 相性数据处理器测试")
    print("2. 相性计算器测试")
    print("3. 运行所有测试")

    choice = input("请输入选择 (1/2/3): ").strip()

    if choice == "1":
        test_compatibility_calculator()
    elif choice == "2":
        test_compatibility_calculator_advanced()
    elif choice == "3":
        test_compatibility_calculator()
        print("\n" + "=" * 80 + "\n")
        test_compatibility_calculator_advanced()
    else:
        print("无效选择，运行所有测试...")
        test_compatibility_calculator()
        print("\n" + "=" * 80 + "\n")
        test_compatibility_calculator_advanced()
