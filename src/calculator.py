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
                                    grandparent4: str) -> int:
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
            print(f"三三相性 ({uma1}, {uma2}, {uma3}): {score}")
        
        print(f"总相性点数: {total_score}")
        return total_score
    
    def calculate_compatibility_score_simple(self, horses: List[str]) -> int:
        """
        简化版本：直接传入7匹马的列表进行计算
        
        Args:
            horses: 马娘列表，顺序为 [target, parent1, parent2, grandparent1, grandparent2, grandparent3, grandparent4]
            
        Returns:
            相性点数和
        """
        if len(horses) != 7:
            raise ValueError("必须提供7匹马娘")
        
        target, parent1, parent2, grandparent1, grandparent2, grandparent3, grandparent4 = horses
        
        return self.calculate_compatibility_score(
            target, parent1, parent2, grandparent1, grandparent2, grandparent3, grandparent4
        )
    
    def get_detailed_breakdown(self, 
                             target: str, 
                             parent1: str, 
                             parent2: str, 
                             grandparent1: str, 
                             grandparent2: str, 
                             grandparent3: str, 
                             grandparent4: str) -> dict:
        """
        获取详细的相性分解信息
        
        Returns:
            包含各项相性分数的详细字典
        """
        breakdown = {
            'pair_scores': {},
            'triple_scores': {},
            'total_score': 0
        }
        
        # 计算两两相性
        pair_combinations = [
            (target, parent1),
            (target, parent2),
            (parent1, parent2)
        ]
        
        for uma1, uma2 in pair_combinations:
            score = self.compatibility_data.get_pair_compatibility(uma1, uma2)
            breakdown['pair_scores'][f"({uma1}, {uma2})"] = score
            breakdown['total_score'] += score
        
        # 计算三三相性
        triple_combinations = [
            (target, parent1, grandparent1),
            (target, parent1, grandparent2),
            (target, parent2, grandparent3),
            (target, parent2, grandparent4)
        ]
        
        for uma1, uma2, uma3 in triple_combinations:
            score = self.compatibility_data.get_triple_compatibility(uma1, uma2, uma3)
            breakdown['triple_scores'][f"({uma1}, {uma2}, {uma3})"] = score
            breakdown['total_score'] += score
        
        return breakdown
    
    def validate_horses(self, horses: List[str]) -> bool:
        """
        验证马娘列表是否有效（所有马娘都存在于数据库中）
        
        Args:
            horses: 马娘列表
            
        Returns:
            是否所有马娘都有效
        """
        all_umas = self.compatibility_data.get_all_umas()
        for horse in horses:
            if horse not in all_umas:
                print(f"警告: 马娘 '{horse}' 不存在于数据库中")
                return False
        return True 