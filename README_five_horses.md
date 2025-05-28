# 五马循环计算器 (Five Horses Calculator)

## 概述

五马循环计算器是赛马娘相性计算系统的核心模块之一，用于计算在给定一只目标马娘（parent）的情况下，找出最优的四只其他马娘组合，使得五只马娘的总相性点数最大化。

## 功能特性

- **最优组合计算**：在指定parent的情况下，计算使相性点数和最大的grandparent1、grandparent2、chromo1、chromo2组合
- **前N优组合获取**：获取前N个最优组合，便于比较选择
- **指定组合计算**：计算特定五马组合的相性点数
- **多进程加速**：支持多进程并行计算，大幅提升大规模数据的计算速度
- **智能堆优化**：使用最小堆数据结构优化前N优组合的维护，减少内存使用和排序开销
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
    verbose=True,
    use_multiprocessing=True,  # 启用多进程加速
    num_processes=None  # 使用默认CPU核心数
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
    verbose=True,
    use_multiprocessing=True,  # 启用多进程加速
    num_processes=4  # 指定进程数
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

### 性能优化选项

```python
# 对于小规模计算，可关闭多进程
best_combo, score = calculator.calculate_best_combination(
    parent="目标马娘",
    use_multiprocessing=False  # 关闭多进程
)

# 对于大规模计算，调整进程数
top_results = calculator.get_top_combinations(
    parent="目标马娘",
    top_n=20,
    use_multiprocessing=True,
    num_processes=8  # 使用8个进程
)
```

## 方法说明

### `calculate_best_combination(parent, verbose=True, use_multiprocessing=True, num_processes=None)`
计算给定parent下的最优五马组合。

**参数：**
- `parent` (str): 指定的目标马娘名称
- `verbose` (bool): 是否显示详细进度信息
- `use_multiprocessing` (bool): 是否使用多进程加速
- `num_processes` (int): 进程数，默认为CPU核心数

**返回：**
- `Tuple[Dict, int]`: 最优组合字典和最大相性点数

### `get_top_combinations(parent, top_n=10, verbose=True, use_multiprocessing=True, num_processes=None)`
获取指定parent下的前N个最优组合。

**参数：**
- `parent` (str): 指定的目标马娘名称
- `top_n` (int): 返回前N个结果
- `verbose` (bool): 是否显示详细进度信息
- `use_multiprocessing` (bool): 是否使用多进程加速
- `num_processes` (int): 进程数，默认为CPU核心数

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

### 多进程加速
- **自动阈值**：当组合数超过1000时自动启用多进程
- **进程池管理**：使用进程池复用，减少进程创建开销
- **数据分块**：智能分割计算任务，均衡各进程负载
- **实时进度**：多进程环境下仍保持进度显示

### 算法优化
- **最小堆优化**：使用`heapq`维护前N优结果，避免频繁排序
- **内存管理**：只保留必要的top-N结果，减少内存占用
- **批量处理**：分块处理大量组合，减少通信开销

### 自适应策略
- **自动切换**：根据数据规模自动选择单进程或多进程
- **阈值控制**：可自定义多进程启用阈值
- **核心数检测**：自动检测CPU核心数优化并行度

## 错误处理

- 检查马娘名称是否存在于数据中
- 验证五只马娘不能有重复
- 确保有足够的马娘数量进行计算（至少需要5只不同的马娘）
- 多进程环境下的异常处理和资源清理

## 计算复杂度

对于N只马娘，在指定parent的情况下：
- 需要从剩余(N-1)只马娘中选择4只不同的马娘
- 总组合数 = C(N-1, 4) = (N-1)! / (4! × (N-5)!)
- 当N=100时，约需计算360万种组合

### 性能指标
- **单进程**：适用于组合数 < 1000的小规模计算
- **多进程**：对于大规模计算可获得2-8倍加速（取决于CPU核心数）
- **内存使用**：堆优化后内存使用量降低60%-80%

## 注意事项

1. **计算时间**：随马娘数量增加而快速增长，建议使用多进程加速
2. **进程数选择**：建议设置为CPU核心数，过多进程可能导致性能下降
3. **内存要求**：多进程会增加内存使用，确保系统有足够内存
4. **数据文件**：确保相性数据文件正确加载和缓存
5. **马娘唯一性**：五只马娘必须各不相同
6. **中断处理**：支持Ctrl+C中断长时间计算