---
name: skill-builder
description: 简化版技能创建助手。当用户想要创建新技能或改进现有技能时使用。提供6步标准化流程：理解需求→规划内容→初始化→编辑实现→打包发布→迭代优化。包含技能模板生成、打包验证等实用脚本。
---

# Skill Builder - 技能创建助手

一个简化版的技能创建工具，帮助你快速构建高质量的 OpenClaw Skill。

## 什么是 Skill

Skill 是模块化、自包含的功能包，通过提供专业知识和工作流来扩展 Claude 的能力。可以把 Skill 看作 Claude 的"专业培训手册"——让通用 AI 变成特定领域的专家。

### Skill 能提供什么

1. **专业工作流** - 特定领域的多步骤流程
2. **工具集成** - 特定文件格式或 API 的操作指南
3. **领域知识** - 公司特定的知识、规范、业务逻辑
4. **资源包** - 脚本、参考资料、模板等可复用资源

## Skill 的核心设计原则

### 1. 简洁至上

上下文窗口是有限的共享资源。Skill 的元数据会一直占用上下文，所以要精简。

**默认假设：Claude 已经很聪明了。** 只添加 Claude 不知道的信息。质疑每一段内容："Claude 真的需要这个解释吗？"

优先使用简洁示例，而非冗长说明。

### 2. 适当的自由度

根据任务的脆弱性和变化性匹配具体程度：

- **高自由度**（文本指令）：多种方法都有效，决策依赖上下文
- **中自由度**（伪代码/参数脚本）：有推荐模式，但允许变化
- **低自由度**（特定脚本，少参数）：操作脆弱，一致性关键

想象 Claude 在探索路径：悬崖上的窄桥需要护栏（低自由度），开阔的草地允许多条路线（高自由度）。

### 3. 渐进式披露

三级加载系统高效管理上下文：

1. **元数据**（name + description）- 始终在上下文 (~100 字)
2. **SKILL.md 主体** - Skill 触发时加载 (<5k 字)
3. **资源包** - 按需加载（无限制，脚本可执行不占用上下文）

## Skill 目录结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter 元数据 (必需)
│   │   ├── name: (必需)
│   │   └── description: (必需)
│   └── Markdown 指令 (必需)
└── 资源包 (可选)
    ├── scripts/          - 可执行代码 (Python/Bash等)
    ├── references/       - 按需加载的参考资料
    └── assets/           - 输出中使用的文件 (模板、图标等)
```

### SKILL.md (必需)

包含：
- **Frontmatter** (YAML): `name` 和 `description` 字段，这是 Claude 决定何时使用此 Skill 的唯一依据
- **Body** (Markdown): 使用 Skill 的指令和指导

### 资源包 (可选)

#### Scripts (`scripts/`)

可执行代码，用于需要确定性可靠性或重复编写的任务。

- **何时包含**: 重复编写相同代码或需要确定性可靠性时
- **示例**: `scripts/rotate_pdf.py` 用于 PDF 旋转
- **优势**: 节省 token，确定性执行

#### References (`references/`)

参考资料，按需加载到上下文。

- **何时包含**: Claude 工作时需要参考的文档
- **示例**: 数据库 schema、API 文档、公司政策
- **最佳实践**: 大文件 (>10k 字) 在 SKILL.md 中提供 grep 搜索模式
- **避免重复**: 信息只应存在于 SKILL.md 或 references 文件之一，优先放入 references

#### Assets (`assets/`)

不加载到上下文，而是用于最终输出的文件。

- **何时包含**: Skill 需要在最终输出中使用的文件
- **示例**: 品牌 logo、PPT 模板、HTML/React 样板代码

### 不应包含的文件

不要创建无关的文档文件：
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md

Skill 只应包含 AI 代理完成工作所需的必要信息。

## 6步创建流程

### 第1步：用具体例子理解 Skill

明确 Skill 的具体使用场景。通过直接的用户示例或生成并验证的示例来理解。

**关键问题：**
- "这个 Skill 应该支持什么功能？"
- "能举例说明如何使用这个 Skill 吗？"
- "用户会说什么来触发这个 Skill？"

避免一次问太多问题。从最重要的问题开始，按需跟进。

### 第2步：规划可复用内容

分析每个示例，确定要包含的脚本、参考资料和资源：

| 示例场景 | 分析 | 可复用资源 |
|---------|------|-----------|
| 旋转 PDF | 每次都重写相同代码 | `scripts/rotate_pdf.py` |
| 构建前端应用 | 需要相同的样板代码 | `assets/hello-world/` 模板 |
| BigQuery 查询 | 重复发现表结构 | `references/schema.md` 文档 |

### 第3步：初始化 Skill

运行 `init_skill.py` 脚本生成模板：

```bash
python scripts/init_skill.py <skill-name> --path <输出目录>
```

脚本会自动创建：
- Skill 目录结构
- 带 TODO 占位符的 SKILL.md 模板
- scripts/、references/、assets/ 示例目录

### 第4步：编辑 Skill

#### 先创建可复用资源

从已识别的资源开始：`scripts/`、`references/`、`assets/`。

**重要**: 脚本必须实际运行测试，确保无 bug 且输出符合预期。

删除不需要的示例文件。

#### 更新 SKILL.md

**写作指南**: 使用祈使/不定式形式（命令式）。

**Frontmatter:**

```yaml
---
name: skill-name
description: 清晰描述 Skill 功能和触发条件。包含：(1) 功能描述，(2) 具体使用场景和触发词
---
```

**Body:**

编写使用 Skill 和其资源的指令。

**渐进式披露模式：**

**模式1：高级指南 + 参考资料**

```markdown
# PDF 处理

## 快速开始
提取文本：
[代码示例]

## 高级功能
- **表单填写**: 详见 [FORMS.md](references/FORMS.md)
- **API 参考**: 详见 [REFERENCE.md](references/REFERENCE.md)
```

**模式2：按领域组织**

```
bigquery-skill/
├── SKILL.md (概览和导航)
└── references/
    ├── finance.md (收入、计费指标)
    ├── sales.md (商机、管道)
    └── marketing.md (活动、归因)
```

**模式3：条件详情**

```markdown
# DOCX 处理

## 创建文档
使用 docx-js。详见 [DOCX-JS.md](references/DOCX-JS.md)。

## 编辑文档
简单编辑直接修改 XML。

**修订追踪**: 详见 [REDLINING.md](references/REDLINING.md)
```

**重要指南：**
- **避免深层嵌套引用** - 保持 references 文件直接从 SKILL.md 链接，层级不超过一层
- **长引用文件结构化** - 超过 100 行的文件在顶部包含目录

### 第5步：打包 Skill

开发完成后，打包为可分发格式：

```bash
python scripts/package_skill.py <skill文件夹路径> [输出目录]
```

打包脚本会：
1. **验证** Skill 是否符合要求
2. **打包** 为 .skill 文件（zip 格式，.skill 扩展名）

### 第6步：迭代

测试后根据实际使用改进：
1. 在真实任务中使用 Skill
2. 发现问题或低效之处
3. 更新 SKILL.md 或资源
4. 重新测试

## 使用本 Skill

**创建新 Skill：**
> "帮我创建一个处理 Excel 文件的 Skill"

**改进现有 Skill：**
> "优化这个 Skill 的结构，把大段文档移到 references"

**打包 Skill：**
> "打包 /path/to/my-skill 目录"

**验证 Skill：**
> "检查这个 Skill 是否符合规范"

---

*保持简洁，保持专注，让 Skill 真正有用。*