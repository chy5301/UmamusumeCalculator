from typing import Tuple, Dict
from .compatibility import CompatibilityData

class UmaCalculator:
    def __init__(self, compatibility_data: CompatibilityData):
        """
        初始化计算器
        
        Args:
            compatibility_data: 相性数据对象
        """
        self.compatibility_data = compatibility_data
    
    def calculate_five_uma_score(
        self,
        parent: str,
        grandparent1: str,
        grandparent2: str,
        chromo1: str,
        chromo2: str
    ) -> int:
        """
        计算五马相性点数和
        
        Args:
            parent: 父马娘
            grandparent1: 祖父马娘1
            grandparent2: 祖父马娘2
            chromo1: 染色马娘1
            chromo2: 染色马娘2
            
        Returns:
            相性点数和
        """
        # 计算两两相性
        parent_gp1_score = self.compatibility_data.get_pair_compatibility(parent, grandparent1)
        parent_gp2_score = self.compatibility_data.get_pair_compatibility(parent, grandparent2)
        gp1_gp2_score = self.compatibility_data.get_pair_compatibility(grandparent1, grandparent2)
        
        # 计算三三相性
        parent_gp1_chromo1_score = self.compatibility_data.get_triple_compatibility(parent, grandparent1, chromo1)
        parent_gp1_chromo2_score = self.compatibility_data.get_triple_compatibility(parent, grandparent1, chromo2)
        parent_gp2_chromo2_score = self.compatibility_data.get_triple_compatibility(parent, grandparent2, chromo2)
        parent_gp2_gp1_score = self.compatibility_data.get_triple_compatibility(parent, grandparent2, grandparent1)
        
        # 计算总分
        total_score = (
            parent_gp1_score +
            parent_gp2_score +
            gp1_gp2_score +
            parent_gp1_chromo1_score +
            parent_gp1_chromo2_score +
            parent_gp2_chromo2_score +
            parent_gp2_gp1_score
        )
        
        return total_score
    
    def get_detailed_scores(
        self,
        parent: str,
        grandparent1: str,
        grandparent2: str,
        chromo1: str,
        chromo2: str
    ) -> Dict[str, int]:
        """
        获取详细的相性分数明细
        
        Args:
            parent: 父马娘
            grandparent1: 祖父马娘1
            grandparent2: 祖父马娘2
            chromo1: 染色马娘1
            chromo2: 染色马娘2
            
        Returns:
            包含各项相性分数的字典
        """
        scores = {
            f"({parent}, {grandparent1})": self.compatibility_data.get_pair_compatibility(parent, grandparent1),
            f"({parent}, {grandparent2})": self.compatibility_data.get_pair_compatibility(parent, grandparent2),
            f"({grandparent1}, {grandparent2})": self.compatibility_data.get_pair_compatibility(grandparent1, grandparent2),
            f"({parent}, {grandparent1}, {chromo1})": self.compatibility_data.get_triple_compatibility(parent, grandparent1, chromo1),
            f"({parent}, {grandparent1}, {chromo2})": self.compatibility_data.get_triple_compatibility(parent, grandparent1, chromo2),
            f"({parent}, {grandparent2}, {chromo2})": self.compatibility_data.get_triple_compatibility(parent, grandparent2, chromo2),
            f"({parent}, {grandparent2}, {grandparent1})": self.compatibility_data.get_triple_compatibility(parent, grandparent2, grandparent1)
        }
        
        scores["总分"] = sum(scores.values())
        return scores 