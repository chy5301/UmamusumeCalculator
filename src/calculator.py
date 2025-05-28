from typing import List, Tuple
from .compatibility import CompatibilityData

class CompatibilityCalculator:
    def __init__(self, compatibility_data: CompatibilityData):
        """
        初始化相性计算器
        
        Args:
            compatibility_data: 相性数据处理器实例
        """
        self.compatibility_data = compatibility_data

    def calculate_compatibility_score(self,
                                    target: str,
                                    parent1: str,
                                    parent2: str,
                                    grandparent1: str,
                                    grandparent2: str,
                                    grandparent3: str,
                                    grandparent4: str,
                                    verbose: bool = False) -> int:
        """
        计算七只马娘的相性点数和
        
        公式：相性点数和 = (target, parent1) + (target, parent2) + (parent1, parent2) +
                      (target, parent1, grandparent1) + (target, parent1, grandparent2) +
                      (target, parent2, grandparent3) + (target, parent2, grandparent4)
        
        Args:
            target: 目标马娘
            parent1: 父辈1
            parent2: 父辈2
            grandparent1: 祖辈1（与parent1相关）
            grandparent2: 祖辈2（与parent1相关）
            grandparent3: 祖辈3（与parent2相关）
            grandparent4: 祖辈4（与parent2相关）
            verbose: 是否打印详细计算信息
            
        Returns:
            相性点数和
        """
        total_score = 0

        # 计算两两相性
        pair_scores = [
            (target, parent1),
            (target, parent2),
            (parent1, parent2)
        ]

        for uma1, uma2 in pair_scores:
            score = self.compatibility_data.get_pair_compatibility(uma1, uma2)
            total_score += score
            if verbose:
                print(f"两两相性 ({uma1}, {uma2}): {score}")

        # 计算三三相性
        triple_scores = [
            (target, parent1, grandparent1),
            (target, parent1, grandparent2),
            (target, parent2, grandparent3),
            (target, parent2, grandparent4)
        ]

        for uma1, uma2, uma3 in triple_scores:
            score = self.compatibility_data.get_triple_compatibility(uma1, uma2, uma3)
            total_score += score
            if verbose:
                print(f"三三相性 ({uma1}, {uma2}, {uma3}): {score}")

        if verbose:
            print(f"总相性点数: {total_score}")
        return total_score