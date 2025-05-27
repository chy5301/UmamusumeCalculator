# 初始化数据处理器
from src.compatibility import CompatibilityData
from src.calculator import UmaCalculator
import time


def test_compatibility_calculator():
    print("开始测试相性计算器...")

    # 记录开始时间
    start_time = time.time()

    # 初始化数据处理器
    print("正在初始化数据处理器...")
    data = CompatibilityData("data/相性数据表.csv", num_processes=4)

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
    print("重新初始化数据处理器（应该从缓存加载）...")
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


def test_five_uma_calculator():
    print("\n开始测试五马相性计算器...")
    print("-" * 50)
    
    # 初始化数据处理器和计算器
    data = CompatibilityData("data/相性数据表.csv")
    calculator = UmaCalculator(data)
    
    # 测试用例1：使用一些已知的马娘组合
    test_case1 = {
        "parent": "特别周",
        "grandparent1": "无声铃鹿",
        "grandparent2": "草上飞",
        "chromo1": "神鹰",
        "chromo2": "小栗帽"
    }
    
    # 测试用例2：使用另一组马娘
    test_case2 = {
        "parent": "目白麦昆",
        "grandparent1": "东海帝王",
        "grandparent2": "米浴",
        "chromo1": "好歌剧",
        "chromo2": "成田白仁"
    }
    
    # 测试计算总分
    print("测试用例1 - 计算总分:")
    total_score1 = calculator.calculate_five_uma_score(**test_case1)
    print(f"总分: {total_score1}")
    
    print("\n测试用例2 - 计算总分:")
    total_score2 = calculator.calculate_five_uma_score(**test_case2)
    print(f"总分: {total_score2}")
    
    # 测试获取详细分数
    print("\n测试用例1 - 详细分数:")
    detailed_scores1 = calculator.get_detailed_scores(**test_case1)
    for combination, score in detailed_scores1.items():
        print(f"{combination}: {score}")
    
    print("\n测试用例2 - 详细分数:")
    detailed_scores2 = calculator.get_detailed_scores(**test_case2)
    for combination, score in detailed_scores2.items():
        print(f"{combination}: {score}")


if __name__ == "__main__":
    # test_compatibility_calculator()
    test_five_uma_calculator()
