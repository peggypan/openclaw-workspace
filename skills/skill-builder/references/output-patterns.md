# Skill 输出模式

## 概述

本文档提供设计 Skill 输出格式和模板的最佳实践。

## 输出类型

### 1. 文件生成

当 Skill 生成文件时：

```markdown
## 输出规范

- **格式**: 指定文件扩展名
- **编码**: 明确编码（通常是 UTF-8）
- **路径**: 说明默认输出位置
- **覆盖**: 说明是否覆盖现有文件
```

### 2. 文本输出

当 Skill 返回文本内容时：

```markdown
## 输出格式

- **结构**: 标题、列表、代码块的使用
- **长度**: 预期输出长度
- **语言**: 输出语言
```

### 3. 结构化数据

当 Skill 返回 JSON/YAML 等结构化数据时：

```markdown
## 输出 Schema

```json
{
  "field1": "string - 说明",
  "field2": "number - 说明",
  "field3": {
    "nested": "boolean"
  }
}
```
```

## 模板模式

### 基础模板

```markdown
# {{title}}

## 概述
{{summary}}

## 详情
{{details}}

## 示例
{{example}}
```

### 报告模板

```markdown
# {{report_title}}

生成时间: {{timestamp}}

## 执行摘要
{{executive_summary}}

## 详细结果
{{#each sections}}
### {{title}}
{{content}}
{{/each}}

## 建议
{{recommendations}}
```

### 代码模板

```markdown
## 使用示例

```python
from {{module}} import {{class}}

# 初始化
instance = {{class}}({{params}})

# 执行
result = instance.{{method}}({{args}})

# 输出
print(result)
```
```

## 质量保证

### 一致性

确保输出风格一致：
- 使用相同的标题级别
- 保持相同的列表样式
- 统一的代码块格式

### 完整性

输出应包含：
- 所有必需的信息
- 清晰的标签和说明
- 适当的示例

### 可读性

优化可读性：
- 使用空白行分隔段落
- 适当使用加粗和斜体
- 代码块标注语言

## 示例：文档生成输出

```markdown
## 生成的文档结构

1. **标题部分**
   - 主标题（H1）
   - 副标题（可选）
   
2. **元数据部分**
   - 创建时间
   - 作者
   - 版本

3. **内容部分**
   - 概述（H2）
   - 详细说明（H2/H3）
   - 示例（H2 + 代码块）
   
4. **参考部分**
   - 相关链接
   - 进一步阅读
```

## 示例：代码输出

```markdown
## 代码输出规范

- 包含必要的导入语句
- 添加类型注解（Python）
- 包含 docstring
- 添加使用示例

```python
def process_data(data: list[dict]) -> dict:
    \"\"\"
    处理数据列表并返回汇总结果。
    
    Args:
        data: 包含记录的字典列表
        
    Returns:
        包含统计信息的字典
        
    Example:
        >>> data = [{"name": "A", "value": 10}]
        >>> process_data(data)
        {"count": 1, "total": 10}
    \"\"\"
    return {
        "count": len(data),
        "total": sum(d.get("value", 0) for d in data)
    }
```
```

## 检查清单

设计输出时，确保：

- [ ] 输出格式符合用户预期
- [ ] 包含所有必要信息
- [ ] 有清晰的标签和说明
- [ ] 示例完整可运行
- [ ] 错误情况有明确说明