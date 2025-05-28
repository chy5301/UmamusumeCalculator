from typing import List, Tuple, Dict, Set
from itertools import permutations
from tqdm import tqdm
from .calculator import CompatibilityCalculator
from .compatibility import CompatibilityData
import heapq
import multiprocessing
from multiprocessing import Pool
import math

class FiveHorsesCalculator:
    def __init__(self, compatibility_data: CompatibilityData):
        """
        初始化五马循环计算器
        
        Args:
            compatibility_data: 相性数据处理器实例
        """
        self.compatibility_data = compatibility_data
        self.calculator = CompatibilityCalculator(compatibility_data)
        self.all_umas = list(compatibility_data.get_all_umas())
        
    def calculate_best_combination(self, parent: str, verbose: bool = True, num_processes: int = None) -> Tuple[Dict, int]:
        """
        计算给定parent下的最优五马组合（多进程优化版本）
        
        映射关系：
        - parent -> target
        - grandparent1 -> parent1, grandparent4  
        - grandparent2 -> parent2
        - chromo1 -> grandparent1
        - chromo2 -> grandparent2, grandparent3
        
        Args:
            parent: 指定的父辈马娘
            verbose: 是否显示详细进度信息
            num_processes: 进程数，默认为CPU核心数
            
        Returns:
            最优组合字典和最大相性点数的元组
        """
        if parent not in self.all_umas:
            raise ValueError(f"马娘 '{parent}' 不存在于数据中")
        
        # 排除parent，获取其他可选马娘
        other_umas = [uma for uma in self.all_umas if uma != parent]
        
        if len(other_umas) < 4:
            raise ValueError(f"可用马娘数量不足，需要至少4只其他马娘，当前只有{len(other_umas)}只")
        
        # 使用permutations生成有序的四马组合
        all_combinations = list(permutations(other_umas, 4))
        total_combinations = len(all_combinations)
        
        if verbose:
            print(f"正在为马娘 '{parent}' 计算最优五马组合...")
            print(f"总共需要计算 {total_combinations} 种组合")
            print(f"使用多进程加速（进程数: {num_processes or multiprocessing.cpu_count()}）")
        
        if num_processes is None:
            num_processes = multiprocessing.cpu_count()
        
        # 将组合分块
        chunk_size = math.ceil(len(all_combinations) / num_processes)
        chunks = [all_combinations[i:i + chunk_size] for i in range(0, len(all_combinations), chunk_size)]
        
        # 准备兼容数据
        compatibility_cache = {
            'pair': self.compatibility_data.pair_compatibility,
            'triple': self.compatibility_data.triple_compatibility,
            'all_umas': self.compatibility_data.all_umas
        }
        
        # 使用进程池处理
        with Pool(processes=num_processes) as pool:
            # 准备任务数据
            chunk_data = [(chunk, parent, compatibility_cache) for chunk in chunks]
            
            # 使用tqdm显示进度
            with tqdm(total=total_combinations, desc="计算最优组合", disable=not verbose) as pbar:
                # 使用imap_unordered实时获取结果
                best_score = -1
                best_combination = {}
                
                for chunk_result in pool.imap_unordered(process_best_combination_chunk, chunk_data):
                    # 更新最优结果
                    if chunk_result['best_score'] > best_score:
                        best_score = chunk_result['best_score']
                        best_combination = chunk_result['best_combination']
                    
                    # 更新进度条
                    pbar.update(len(chunk_result['chunk']))
                    
                    if verbose:
                        pbar.set_postfix({'当前最高分': best_score})
        
        return best_combination, best_score

    def display_result(self, combination: Dict, score: int):
        """
        显示计算结果
        
        Args:
            combination: 最优组合字典
            score: 相性点数
        """
        print("\n" + "="*50)
        print("五马循环最优组合结果")
        print("="*50)
        print(f"目标马娘 (Parent): {combination['parent']}")
        print(f"祖父马娘1 (Grandparent1): {combination['grandparent1']}")
        print(f"祖父马娘2 (Grandparent2): {combination['grandparent2']}")
        print(f"染色体马娘1 (Chromo1): {combination['chromo1']}")
        print(f"染色体马娘2 (Chromo2): {combination['chromo2']}")
        print(f"总相性点数: {score}")
        print("="*50)
        
        # 显示映射关系说明
        print("\n映射关系说明:")
        print(f"计算时使用的七马配置:")
        print(f"  Target: {combination['parent']}")
        print(f"  Parent1: {combination['grandparent1']}")
        print(f"  Parent2: {combination['grandparent2']}")
        print(f"  Grandparent1: {combination['chromo1']}")
        print(f"  Grandparent2: {combination['chromo2']}")
        print(f"  Grandparent3: {combination['chromo2']}")
        print(f"  Grandparent4: {combination['grandparent1']}")
    
    def calculate_specific_combination(self, parent: str, grandparent1: str, 
                                     grandparent2: str, chromo1: str, chromo2: str) -> int:
        """
        计算指定五马组合的相性点数
        
        Args:
            parent: 目标马娘
            grandparent1: 祖父马娘1
            grandparent2: 祖父马娘2  
            chromo1: 染色体马娘1
            chromo2: 染色体马娘2
            
        Returns:
            相性点数
        """
        # 检查所有马娘是否存在
        horses = [parent, grandparent1, grandparent2, chromo1, chromo2]
        for horse in horses:
            if horse not in self.all_umas:
                raise ValueError(f"马娘 '{horse}' 不存在于数据中")
        
        # 检查是否有重复
        if len(set(horses)) != 5:
            raise ValueError("五只马娘不能有重复")
        
        # 根据映射关系计算相性点数
        score = self.calculator.calculate_compatibility_score(
            target=parent,
            parent1=grandparent1,
            parent2=grandparent2,
            grandparent1=chromo1,
            grandparent2=chromo2,
            grandparent3=chromo2,
            grandparent4=grandparent1,
            verbose=True  # 单独计算时显示详细信息
        )
        
        return score
    
    def get_top_combinations(self, parent: str, top_n: int = 10, verbose: bool = True, 
                           num_processes: int = None) -> List[Tuple[Dict, int]]:
        """
        获取指定parent下的前N个最优组合（多进程优化版本）
        
        Args:
            parent: 指定的父辈马娘
            top_n: 返回前N个结果
            verbose: 是否显示详细进度信息
            num_processes: 进程数，默认为CPU核心数
            
        Returns:
            按分数降序排列的组合列表
        """
        if parent not in self.all_umas:
            raise ValueError(f"马娘 '{parent}' 不存在于数据中")
        
        # 排除parent，获取其他可选马娘
        other_umas = [uma for uma in self.all_umas if uma != parent]
        
        if len(other_umas) < 4:
            raise ValueError(f"可用马娘数量不足，需要至少4只其他马娘，当前只有{len(other_umas)}只")
        
        total_combinations = len(list(permutations(other_umas, 4)))
        
        if verbose:
            print(f"正在为马娘 '{parent}' 计算前{top_n}个最优组合...")
            print(f"总共需要计算 {total_combinations} 种组合")
            print(f"使用多进程加速（进程数: {num_processes or multiprocessing.cpu_count()}）")
        
        if num_processes is None:
            num_processes = multiprocessing.cpu_count()
        
        # 生成所有四马组合
        all_combinations = list(permutations(other_umas, 4))
        
        # 将组合分块
        chunk_size = math.ceil(len(all_combinations) / num_processes)
        chunks = [all_combinations[i:i + chunk_size] for i in range(0, len(all_combinations), chunk_size)]
        
        # 准备兼容数据
        compatibility_cache = {
            'pair': self.compatibility_data.pair_compatibility,
            'triple': self.compatibility_data.triple_compatibility,
            'all_umas': self.compatibility_data.all_umas
        }
        
        # 使用最小堆维护前N个结果
        min_heap = []  # 存储 (score, index, combination)
        index = 0
        
        # 使用进程池处理
        with Pool(processes=num_processes) as pool:
            # 准备任务数据
            chunk_data = [(chunk, parent, compatibility_cache, top_n) for chunk in chunks]
            
            # 使用tqdm显示进度
            with tqdm(total=total_combinations, desc=f"计算前{top_n}组合", disable=not verbose) as pbar:
                # 使用imap_unordered实时获取结果
                for chunk_result in pool.imap_unordered(process_top_n_combinations_chunk, chunk_data):
                    # 处理这个chunk的结果
                    for combination, score in chunk_result['top_n']:
                        if len(min_heap) < top_n:
                            # 堆未满，直接加入
                            heapq.heappush(min_heap, (score, index, combination))
                            index += 1
                        elif score > min_heap[0][0]:
                            # 当前分数比堆中最小分数大，替换
                            heapq.heapreplace(min_heap, (score, index, combination))
                            index += 1
                    
                    # 更新进度条 - 使用chunk的大小而不是结果数量
                    pbar.update(len(chunk_result['chunk']))
                    
                    if verbose and min_heap:
                        # 显示当前最低入选分数
                        pbar.set_postfix({'第{}名分数'.format(top_n): min_heap[0][0] if len(min_heap) == top_n else '未满'})
        
        # 从最小堆中提取结果并按分数降序排列
        results = [(combo, score) for score, _, combo in min_heap]
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results

def process_best_combination_chunk(chunk_data):
    """
    处理单个数据块并返回该块的最优五马组合（用于calculate_best_combination）
    
    Args:
        chunk_data: 包含(数据块, parent, 兼容数据缓存)的元组
        
    Returns:
        包含最优组合、分数和原始数据块的字典
    """
    chunk, parent, compatibility_data_cache = chunk_data
    
    # 重建CompatibilityCalculator（在子进程中）
    from .compatibility import CompatibilityData
    from .calculator import CompatibilityCalculator
    
    # 创建临时的compatibility data对象
    temp_data = CompatibilityData.__new__(CompatibilityData)
    temp_data.pair_compatibility = compatibility_data_cache['pair']
    temp_data.triple_compatibility = compatibility_data_cache['triple']
    temp_data.all_umas = compatibility_data_cache['all_umas']
    
    calculator = CompatibilityCalculator(temp_data)
    
    # 在子进程中维护最优结果
    best_score = -1
    best_combination = {}
    
    # 处理这个chunk的所有组合
    for four_horses in chunk:
        grandparent1, grandparent2, chromo1, chromo2 = four_horses
        
        # 计算相性分数
        score = calculator.calculate_compatibility_score(
            target=parent,
            parent1=grandparent1,
            parent2=grandparent2,
            grandparent1=chromo1,
            grandparent2=chromo2,
            grandparent3=chromo2,
            grandparent4=grandparent1,
            verbose=False
        )
        
        # 更新最优组合
        if score > best_score:
            best_score = score
            best_combination = {
                'parent': parent,
                'grandparent1': grandparent1,
                'grandparent2': grandparent2,
                'chromo1': chromo1,
                'chromo2': chromo2
            }
    
    # 返回这个chunk的最优结果和原始chunk用于进度更新
    return {
        'best_combination': best_combination,
        'best_score': best_score,
        'chunk': chunk
    }

def process_top_n_combinations_chunk(chunk_data):
    """
    处理单个数据块并返回该块的前N优五马组合（用于get_top_combinations）
    
    Args:
        chunk_data: 包含(数据块, parent, 兼容数据缓存, top_n)的元组
        
    Returns:
        包含最优组合、前N优结果和原始数据块的字典
    """
    chunk, parent, compatibility_data_cache, top_n = chunk_data
    
    # 重建CompatibilityCalculator（在子进程中）
    from .compatibility import CompatibilityData
    from .calculator import CompatibilityCalculator
    
    # 创建临时的compatibility data对象
    temp_data = CompatibilityData.__new__(CompatibilityData)
    temp_data.pair_compatibility = compatibility_data_cache['pair']
    temp_data.triple_compatibility = compatibility_data_cache['triple']
    temp_data.all_umas = compatibility_data_cache['all_umas']
    
    calculator = CompatibilityCalculator(temp_data)
    
    # 在子进程中维护最优结果
    best_score = -1
    best_combination = {}
    
    # 使用最小堆维护前N个结果
    min_heap = []  # 存储 (score, index, combination)
    index = 0
    
    # 处理这个chunk的所有组合
    for four_horses in chunk:
        grandparent1, grandparent2, chromo1, chromo2 = four_horses
        
        # 计算相性分数
        score = calculator.calculate_compatibility_score(
            target=parent,
            parent1=grandparent1,
            parent2=grandparent2,
            grandparent1=chromo1,
            grandparent2=chromo2,
            grandparent3=chromo2,
            grandparent4=grandparent1,
            verbose=False
        )
        
        combination = {
            'parent': parent,
            'grandparent1': grandparent1,
            'grandparent2': grandparent2,
            'chromo1': chromo1,
            'chromo2': chromo2
        }
        
        # 更新最优组合
        if score > best_score:
            best_score = score
            best_combination = combination
        
        # 更新前N优结果
        if len(min_heap) < top_n:
            heapq.heappush(min_heap, (score, index, combination))
            index += 1
        elif score > min_heap[0][0]:
            heapq.heapreplace(min_heap, (score, index, combination))
            index += 1
    
    # 从最小堆中提取前N优结果
    top_results = [(combo, score) for score, _, combo in min_heap]
    top_results.sort(key=lambda x: x[1], reverse=True)
    
    # 返回这个chunk的最优结果和前N优结果，以及原始chunk用于进度更新
    return {
        'best': (best_combination, best_score),
        'top_n': top_results,
        'chunk': chunk
    }