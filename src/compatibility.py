import pandas as pd
import json
import os
from typing import List, Dict, Set, Tuple
from itertools import combinations
from tqdm import tqdm
import multiprocessing
from multiprocessing import Pool
import math

def process_chunk(chunk_data):
    """处理一个数据块的函数"""
    chunk, uma_groups, df_data = chunk_data
    chunk_results = {}
    # 重建数据
    uma_to_groups = {k: set(v) for k, v in uma_groups.items()}
    df = pd.DataFrame(df_data)
    
    for uma1, uma2, uma3 in chunk:
        score = 0
        # 找出三个马娘共同所在的组
        groups1 = {g['组号'] for g in get_uma_groups_internal(uma1, uma_to_groups, df)}
        groups2 = {g['组号'] for g in get_uma_groups_internal(uma2, uma_to_groups, df)}
        groups3 = {g['组号'] for g in get_uma_groups_internal(uma3, uma_to_groups, df)}
        common_groups = groups1.intersection(groups2).intersection(groups3)
        
        # 累加共同组的分数
        for group in get_uma_groups_internal(uma1, uma_to_groups, df):
            if group['组号'] in common_groups:
                score += group['分数']
        
        # 存储所有可能的排列
        for perm in [(uma1, uma2, uma3), (uma1, uma3, uma2), 
                    (uma2, uma1, uma3), (uma2, uma3, uma1),
                    (uma3, uma1, uma2), (uma3, uma2, uma1)]:
            chunk_results[perm] = score
    return chunk_results

def get_uma_groups_internal(uma_name: str, uma_to_groups: Dict[str, Set[int]], df: pd.DataFrame) -> List[Dict]:
    """获取指定马娘所在的所有组信息"""
    if uma_name not in uma_to_groups:
        return []
        
    group_ids = uma_to_groups[uma_name]
    groups = df[df['组号'].isin(group_ids)].to_dict('records')
    return groups

class CompatibilityData:
    def __init__(self, csv_path: str, cache_dir: str = "data/cache", num_processes: int = None):
        """
        初始化相性数据处理器
        
        Args:
            csv_path: CSV文件路径
            cache_dir: 缓存目录路径
            num_processes: 计算三三相性时使用的进程数，默认为CPU核心数
        """
        self.cache_dir = cache_dir
        self.num_processes = num_processes or multiprocessing.cpu_count()
        os.makedirs(cache_dir, exist_ok=True)
        
        # 尝试从缓存加载数据
        if self._load_from_cache():
            return
            
        print("正在加载CSV数据...")
        # 如果没有缓存，则从CSV加载并计算
        self.df = pd.read_csv(csv_path)
        self.df['成员'] = self.df['成员'].apply(lambda x: [name.strip() for name in x.split(',')])
        
        print("正在创建马娘到组号的映射...")
        # 创建马娘到组号的映射
        self.uma_to_groups: Dict[str, Set[int]] = {}
        for _, row in tqdm(self.df.iterrows(), total=len(self.df), desc="处理组数据"):
            group_id = row['组号']
            for uma in row['成员']:
                # 跳过"无"，但保留名字中带"无"的马娘
                if uma == "无":
                    continue
                if uma not in self.uma_to_groups:
                    self.uma_to_groups[uma] = set()
                self.uma_to_groups[uma].add(group_id)
        
        # 获取所有马娘列表（去重）
        self.all_umas = set(self.uma_to_groups.keys())
        
        print(f"共发现 {len(self.all_umas)} 个马娘")
        print("马娘列表：")
        for uma in sorted(self.all_umas):
            print(f"- {uma}")
        
        # 计算并缓存相性数据
        self._calculate_compatibility()
        self._save_to_cache()
    
    def _calculate_compatibility(self):
        """计算所有马娘之间的相性分数"""
        print("\n正在计算两两相性...")
        # 计算两两相性
        self.pair_compatibility: Dict[Tuple[str, str], int] = {}
        pair_combinations = list(combinations(sorted(self.all_umas), 2))
        for uma1, uma2 in tqdm(pair_combinations, desc="计算两两相性"):
            score = self._calculate_pair_score(uma1, uma2)
            self.pair_compatibility[(uma1, uma2)] = score
            self.pair_compatibility[(uma2, uma1)] = score  # 对称性
        
        print("\n正在计算三三相性...")
        # 计算三三相性
        self.triple_compatibility: Dict[Tuple[str, str, str], int] = {}
        triple_combinations = list(combinations(sorted(self.all_umas), 3))
        
        # 将组合列表分成多个块，每个进程处理一个块
        chunk_size = math.ceil(len(triple_combinations) / self.num_processes)
        chunks = [triple_combinations[i:i + chunk_size] for i in range(0, len(triple_combinations), chunk_size)]
        
        # 准备进程间共享的数据
        uma_groups_data = {k: list(v) for k, v in self.uma_to_groups.items()}
        df_data = self.df.to_dict('records')
        
        # 使用进程池并行处理
        with Pool(processes=self.num_processes) as pool:
            # 准备任务数据
            chunk_data = [(chunk, uma_groups_data, df_data) for chunk in chunks]
            
            # 使用tqdm显示总体进度
            with tqdm(total=len(triple_combinations), desc="计算三三相性") as pbar:
                # 处理完成的任务
                for chunk_results in pool.imap_unordered(process_chunk, chunk_data):
                    self.triple_compatibility.update(chunk_results)
                    # 更新进度条
                    pbar.update(chunk_size)
    
    def _calculate_pair_score(self, uma1: str, uma2: str) -> int:
        """计算两个马娘之间的相性分数"""
        score = 0
        groups1 = self.get_uma_groups(uma1)
        groups2 = self.get_uma_groups(uma2)
        
        # 找出两个马娘共同所在的组
        group_ids1 = {g['组号'] for g in groups1}
        group_ids2 = {g['组号'] for g in groups2}
        common_groups = group_ids1.intersection(group_ids2)
        
        # 累加共同组的分数
        for group in groups1:
            if group['组号'] in common_groups:
                score += group['分数']
                
        return score
    
    def _calculate_triple_score(self, uma1: str, uma2: str, uma3: str) -> int:
        """计算三个马娘之间的相性分数"""
        score = 0
        groups1 = self.get_uma_groups(uma1)
        groups2 = self.get_uma_groups(uma2)
        groups3 = self.get_uma_groups(uma3)
        
        # 找出三个马娘共同所在的组
        group_ids1 = {g['组号'] for g in groups1}
        group_ids2 = {g['组号'] for g in groups2}
        group_ids3 = {g['组号'] for g in groups3}
        common_groups = group_ids1.intersection(group_ids2).intersection(group_ids3)
        
        # 累加共同组的分数
        for group in groups1:
            if group['组号'] in common_groups:
                score += group['分数']
                
        return score
    
    def _save_to_cache(self):
        """将计算结果保存到缓存"""
        print("\n正在保存计算结果到缓存...")
        # 保存两两相性
        pair_cache = {f"{k[0]},{k[1]}": v for k, v in tqdm(self.pair_compatibility.items(), desc="保存两两相性")}
        with open(os.path.join(self.cache_dir, "pair_compatibility.json"), "w", encoding="utf-8") as f:
            json.dump(pair_cache, f, ensure_ascii=False, indent=2)
        
        # 保存三三相性
        triple_cache = {f"{k[0]},{k[1]},{k[2]}": v for k, v in tqdm(self.triple_compatibility.items(), desc="保存三三相性")}
        with open(os.path.join(self.cache_dir, "triple_compatibility.json"), "w", encoding="utf-8") as f:
            json.dump(triple_cache, f, ensure_ascii=False, indent=2)

        # 保存马娘列表
        uma_list_cache = list(self.all_umas)
        with open(os.path.join(self.cache_dir, "uma_list.json"), "w", encoding="utf-8") as f:
            json.dump(uma_list_cache, f, ensure_ascii=False, indent=2)
            
        print("缓存保存完成！")
    
    def _load_from_cache(self) -> bool:
        """从缓存加载数据"""
        pair_cache_path = os.path.join(self.cache_dir, "pair_compatibility.json")
        triple_cache_path = os.path.join(self.cache_dir, "triple_compatibility.json")
        uma_list_path = os.path.join(self.cache_dir, "uma_list.json")
        
        if not (os.path.exists(pair_cache_path) and os.path.exists(triple_cache_path) and os.path.exists(uma_list_path)):
            return False
        
        print("正在从缓存加载数据...")
        # 加载两两相性
        with open(pair_cache_path, "r", encoding="utf-8") as f:
            pair_cache = json.load(f)
        self.pair_compatibility = {tuple(k.split(",")): v for k, v in tqdm(pair_cache.items(), desc="加载两两相性")}
        
        # 加载三三相性
        with open(triple_cache_path, "r", encoding="utf-8") as f:
            triple_cache = json.load(f)
        self.triple_compatibility = {tuple(k.split(",")): v for k, v in tqdm(triple_cache.items(), desc="加载三三相性")}
        
        # 加载马娘列表
        with open(uma_list_path, "r", encoding="utf-8") as f:
            uma_list = json.load(f)
        self.all_umas = set(uma_list)
        
        print("缓存加载完成！")
        return True
    
    def get_pair_compatibility(self, uma1: str, uma2: str) -> int:
        """获取两个马娘之间的相性分数"""
        return self.pair_compatibility.get((uma1, uma2), 0)
    
    def get_triple_compatibility(self, uma1: str, uma2: str, uma3: str) -> int:
        """获取三个马娘之间的相性分数"""
        return self.triple_compatibility.get((uma1, uma2, uma3), 0)
    
    def get_uma_groups(self, uma_name: str) -> List[Dict]:
        """
        获取指定马娘所在的所有组信息
        
        Args:
            uma_name: 马娘名称
            
        Returns:
            包含组信息的字典列表，每个字典包含组号、分数、分类、补充和成员信息
        """
        if uma_name not in self.uma_to_groups:
            return []
            
        group_ids = self.uma_to_groups[uma_name]
        groups = self.df[self.df['组号'].isin(group_ids)].to_dict('records')
        return groups
    
    def get_uma_compatibility(self, uma_name: str) -> Dict[str, int]:
        """
        获取指定马娘与其他马娘的相性分数
        
        Args:
            uma_name: 马娘名称
            
        Returns:
            字典，键为其他马娘名称，值为相性分数
        """
        compatibility = {}
        groups = self.get_uma_groups(uma_name)
        
        for group in groups:
            score = group['分数']
            for other_uma in group['成员']:
                if other_uma != uma_name:
                    if other_uma not in compatibility:
                        compatibility[other_uma] = 0
                    compatibility[other_uma] += score
                    
        return compatibility

    def get_all_umas(self) -> Set[str]:
        """
        获取所有马娘的列表
        
        Returns:
            包含所有马娘名称的集合
        """
        return self.all_umas 