# 五马循环计算器 (Five Horses Calculator)

## 概述

五马循环计算器是赛马娘相性计算系统的核心模块之一，用于计算在给定一只目标马娘（parent）的情况下，找出最优的四只其他马娘组合，使得五只马娘的总相性点数最大化。

## 功能特性

- **最优组合计算**：在指定parent的情况下，计算使相性点数和最大的grandparent1、grandparent2、chromo1、chromo2组合
- **前N优组合获取**：获取前N个最优组合，便于比较选择
- **指定组合计算**：计算特定五马组合的相性点数
- **进度显示**：使用tqdm显示计算进度，支持大规模计算
- **详细结果展示**：清晰展示计算结果和映射关系

## 映射关系说明

五马循环计算器定义了五只马娘的角色：
- `parent`：目标马娘（由外部指定）
- `grandparent1`：祖父马娘1
- `grandparent2`：祖父马娘2  
- `chromo1`：染色体马娘1
- `chromo2`：染色体马娘2

在调用底层的七马相性计算时，映射关系如下：
```
target = parent
parent1 = grandparent1
parent2 = grandparent2
grandparent1 = chromo1
grandparent2 = chromo2
grandparent3 = chromo2  (注意：chromo2同时映射到grandparent2和grandparent3)
grandparent4 = grandparent1  (注意：grandparent1同时映射到parent1和grandparent4)
```

## 使用方法

### 基本用法

```python
from src.compatibility import CompatibilityData
from src.five_horses_calculator import FiveHorsesCalculator

# 初始化相性数据
compatibility_data = CompatibilityData("data/compatibility_data.csv")

# 创建五马循环计算器
calculator = FiveHorsesCalculator(compatibility_data)

# 计算最优组合
best_combination, best_score = calculator.calculate_best_combination(
    parent="目标马娘名称",
    verbose=True
)

# 显示结果
calculator.display_result(best_combination, best_score)
```

### 获取前N个最优组合

```python
# 获取前10个最优组合
top_results = calculator.get_top_combinations(
    parent="目标马娘名称",
    top_n=10,
    verbose=True
)

# 显示结果
calculator.display_top_results(top_results)
```

### 计算指定组合的相性点数

```python
score = calculator.calculate_specific_combination(
    parent="目标马娘",
    grandparent1="祖父马娘1",
    grandparent2="祖父马娘2",
    chromo1="染色体马娘1",
    chromo2="染色体马娘2"
)

print(f"相性点数: {score}")
```

## 方法说明

### `calculate_best_combination(parent, verbose=True)`
计算给定parent下的最优五马组合。

**参数：**
- `parent` (str): 指定的目标马娘名称
- `verbose` (bool): 是否显示详细进度信息

**返回：**
- `Tuple[Dict, int]`: 最优组合字典和最大相性点数

### `get_top_combinations(parent, top_n=10, verbose=True)`
获取指定parent下的前N个最优组合。

**参数：**
- `parent` (str): 指定的目标马娘名称
- `top_n` (int): 返回前N个结果
- `verbose` (bool): 是否显示详细进度信息

**返回：**
- `List[Tuple[Dict, int]]`: 按分数降序排列的组合列表

### `calculate_specific_combination(parent, grandparent1, grandparent2, chromo1, chromo2)`
计算指定五马组合的相性点数。

**参数：**
- `parent` (str): 目标马娘
- `grandparent1` (str): 祖父马娘1
- `grandparent2` (str): 祖父马娘2
- `chromo1` (str): 染色体马娘1
- `chromo2` (str): 染色体马娘2

**返回：**
- `int`: 相性点数

### `display_result(combination, score)`
显示单个组合的计算结果。

### `display_top_results(results)`
显示前N个最优组合结果。

## 性能优化

- 使用进度条显示计算进度
- 批量计算时关闭详细输出以提高性能
- 在获取前N优组合时，动态维护最优结果列表
- 支持中断计算并显示当前最优结果

## 错误处理

- 检查马娘名称是否存在于数据中
- 验证五只马娘不能有重复
- 确保有足够的马娘数量进行计算（至少需要5只不同的马娘）

## 计算复杂度

对于N只马娘，在指定parent的情况下：
- 需要从剩余(N-1)只马娘中选择4只不同的马娘
- 总组合数 = C(N-1, 4) = (N-1)! / (4! × (N-5)!)
- 当N=100时，约需计算360万种组合

## 注意事项

1. 计算时间随马娘数量增加而快速增长
2. 建议在大规模计算时开启进度显示
3. 确保相性数据文件正确加载
4. 五只马娘必须各不相同 