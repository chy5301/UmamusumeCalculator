import sys
import os
import hashlib
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from src.compatibility import CompatibilityData

def calculate_data_hash(data):
    """计算数据的MD5哈希值"""
    # 将元组键转换为字符串
    converted_data = {}
    for key, value in data.items():
        if isinstance(key, tuple):
            # 将元组转换为逗号分隔的字符串
            str_key = ",".join(str(k) for k in key)
        else:
            str_key = str(key)
        converted_data[str_key] = value
    
    # 将数据转换为JSON字符串，确保顺序一致
    data_str = json.dumps(converted_data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()

def test_cache_consistency():
    """测试缓存数据的一致性"""
    print("开始测试缓存数据一致性...")
    print("="*50)
    
    # 多次加载数据
    num_tests = 5
    hashes = []
    
    for i in range(num_tests):
        print(f"\n第{i+1}次加载数据:")
        print("-"*30)
        
        # 创建新的数据处理器实例
        data_processor = CompatibilityData()
        
        # 获取数据
        pair_data = data_processor.pair_compatibility
        triple_data = data_processor.triple_compatibility
        
        # 计算哈希值
        pair_hash = calculate_data_hash(pair_data)
        triple_hash = calculate_data_hash(triple_data)
        
        print(f"两两相性数据哈希值: {pair_hash}")
        print(f"三三相性数据哈希值: {triple_hash}")
        
        hashes.append((pair_hash, triple_hash))
    
    # 验证所有哈希值是否一致
    print("\n验证结果:")
    print("="*30)
    
    all_pairs_same = all(h[0] == hashes[0][0] for h in hashes)
    all_triples_same = all(h[1] == hashes[0][1] for h in hashes)
    
    if all_pairs_same and all_triples_same:
        print("✅ 所有加载的数据哈希值完全一致")
    else:
        print("❌ 发现数据不一致:")
        if not all_pairs_same:
            print("- 两两相性数据存在差异")
        if not all_triples_same:
            print("- 三三相性数据存在差异")
    
    # 显示数据统计信息
    print("\n数据统计:")
    print("="*30)
    print(f"两两相性数据条目数: {len(pair_data)}")
    print(f"三三相性数据条目数: {len(triple_data)}")
    
    # 显示一些示例数据
    print("\n数据示例:")
    print("="*30)
    print("两两相性示例:")
    sample_pair = next(iter(pair_data.items()))
    print(f"组合: {sample_pair[0]}")
    print(f"相性值: {sample_pair[1]}")
    
    print("\n三三相性示例:")
    sample_triple = next(iter(triple_data.items()))
    print(f"组合: {sample_triple[0]}")
    print(f"相性值: {sample_triple[1]}")

if __name__ == "__main__":
    test_cache_consistency() 