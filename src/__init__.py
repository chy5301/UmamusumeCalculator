# -*- coding: utf-8 -*-
"""
赛马娘相性计算系统

这个包包含了赛马娘相性计算的核心模块：
- compatibility: 相性数据处理
- calculator: 七马相性计算器
- five_horses_calculator: 五马循环计算器
"""

__version__ = "1.0.0"
__author__ = "UmamusumeCalculator"

from .compatibility import CompatibilityData
from .calculator import CompatibilityCalculator
from .five_horses_calculator import FiveHorsesCalculator

__all__ = [
    'CompatibilityData',
    'CompatibilityCalculator', 
    'FiveHorsesCalculator'
] 