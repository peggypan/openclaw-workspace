---
name: content-creator
description: AI-powered content generation toolkit for creating social media graphics, infographics, and cover images. Generates Xiaohongshu (小红书/RedNote) image series, professional infographics with 20+ layouts, and article cover images. Use when user asks for "小红书图片", "XHS images", "infographic", "cover image", "social media graphics", or any visual content creation needs. Supports multiple styles and layouts with free Pollinations.ai image generation backend.
---

# Content Creator

AI-powered toolkit for generating visual content: social media graphics, infographics, and cover images.

## Features

| Tool | Purpose | Output |
|------|---------|--------|
| `xhs-images` | 小红书/RedNote posts | 3:4 vertical image series (1-10 images) |
| `infographic` | Professional infographics | Custom layouts, multiple aspect ratios |
| `cover-image` | Article/blog headers | 2.35:1 cinematic covers |

## Quick Start

### Generate XHS (小红书) Images

```bash
# Auto style/layout
python3 ${SKILL_DIR}/scripts/xhs_images.py "AI未来的10个趋势"

# Specify style and layout
python3 ${SKILL_DIR}/scripts/xhs_images.py "今日星座运势" --style notion --layout list

# Generate 5 images
python3 ${SKILL_DIR}/scripts/xhs_images.py "健身指南" --style bold --num 5
```

### Generate Infographics

```bash
# Auto layout detection
python3 ${SKILL_DIR}/scripts/infographic.py "AI发展史"

# Specific layout and style
python3 ${SKILL_DIR}/scripts/infographic.py "产品功能对比" --layout comparison-table --style corporate-memphis

# Portrait for mobile
python3 ${SKILL_DIR}/scripts/infographic.py "用户增长漏斗" --layout funnel --aspect portrait
```

### Generate Cover Images

```bash
# Default style
python3 ${SKILL_DIR}/scripts/cover_image.py "AI时代的内容创作"

# With style
python3 ${SKILL_DIR}/scripts/cover_image.py "未来已来" --style gradient-mesh
```

## XHS Image Generator

Creates 3:4 aspect ratio images optimized for Xiaohongshu/RedNote.

### Usage

```bash
python3 ${SKILL_DIR}/scripts/xhs_images.py <content> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--style` | Visual style | `cute` |
| `--layout` | Layout type | `balanced` |
| `--num` | Number of images (1-10) | `3` |
| `--output` | Output directory | `./xhs-output` |
| `--topic` | Topic slug (auto if not set) | - |

### Styles (9 options)

See [references/styles.md](references/styles.md) for full style reference.

Popular styles:
- `cute` - Soft pastels, kawaii (lifestyle/beauty)
- `notion` - Clean documentation (tutorials/knowledge)
- `minimal` - Clean lines, whitespace (business/tips)
- `bold` - High contrast, vibrant (fashion/tech)

### Layouts (6 options)

- `sparse` - 1-2 points (cover/key quotes)
- `balanced` - 3-4 points (regular content)
- `dense` - 5-8 points (knowledge cards)
- `list` - Numbered/bulleted list
- `comparison` - Two-column comparison
- `flow` - 3-6 step process

## Infographic Generator

Creates professional infographics with 20+ layout options.

### Usage

```bash
python3 ${SKILL_DIR}/scripts/infographic.py <content> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--layout` | Layout type (auto-detect if not set) | Auto |
| `--style` | Visual style | `craft-handmade` |
| `--aspect` | Aspect ratio | `landscape` |
| `--output` | Output file path | `./infographic.png` |

### Layouts (20 options)

Categories:
- **Process**: `bridge`, `circular-flow`, `timeline`, `journey-path`
- **Comparison**: `comparison-table`, `do-dont`, `scale-balance`, `venn`
- **Hierarchy**: `pyramid`, `tree-hierarchy`, `layers-stack`, `iceberg`
- **Information**: `feature-list`, `grid-cards`, `priority-quadrants`, `mind-map`
- **Analysis**: `fishbone`, `funnel`, `equation`

See [references/layouts.md](references/layouts.md) for full layout reference.

### Auto Layout Detection

The tool analyzes content keywords to auto-select the best layout:

| Keywords | Selected Layout |
|----------|-----------------|
| "problem", "solution" | `bridge` |
| "compare", "vs" | `comparison-table` |
| "timeline", "history" | `timeline-horizontal` |
| "funnel", "convert" | `funnel` |
| "hierarchy", "levels" | `pyramid` |

## Cover Image Generator

Creates 2.35:1 cinematic cover images for articles and blogs.

### Usage

```bash
python3 ${SKILL_DIR}/scripts/cover_image.py "<title>" [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--style` | Visual style | `bold-typography` |
| `--subtitle` | Optional subtitle | - |
| `--output` | Output file path | `./cover.png` |

### Styles (8 options)

- `bold-typography` - Large impactful text
- `gradient-mesh` - Soft color transitions
- `abstract-geometric` - Modern art composition
- `photographic` - Professional photography style
- `minimalist` - Generous negative space
- `illustrated` - Artistic interpretation
- `duotone` - Two-color palette
- `dark-moody` - Dramatic lighting

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.py`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/xhs_images.py` | XHS infographic series generator |
| `scripts/infographic.py` | Professional infographic generator |
| `scripts/cover_image.py` | Article cover image generator |
| `scripts/generate_image.py` | Core image generation backend |

## Technical Details

### Image Generation Backend

Uses **Pollinations.ai** - Free, no-login image generation API:
- No API key required
- No rate limits for reasonable usage
- Supports custom dimensions
- Good quality for content creation

### Output Naming Convention

Images are saved with descriptive names:

**XHS Images**:
```
xhs-output/<topic-slug>/
├── 01-cover-<topic>.png
├── 02-content-2-<topic>.png
└── 03-content-3-<topic>.png
```

**Infographics**:
```
infographic.png (or specified path)
```

**Cover Images**:
```
cover.png (or specified path)
```

## Examples

### XHS Content Series

```bash
# Fashion tips series
python3 ${SKILL_DIR}/scripts/xhs_images.py \
  "2024春夏穿搭指南：5个必备单品" \
  --style bold \
  --layout list \
  --num 5

# Knowledge sharing
python3 ${SKILL_DIR}/scripts/xhs_images.py \
  "AI提示词工程入门" \
  --style notion \
  --layout dense \
  --num 4
```

### Professional Infographics

```bash
# Business comparison
python3 ${SKILL_DIR}/scripts/infographic.py \
  "产品A vs 产品B功能对比" \
  --layout comparison-table \
  --style corporate-memphis

# Process flow
python3 ${SKILL_DIR}/scripts/infographic.py \
  "用户注册流程优化" \
  --layout funnel \
  --aspect portrait \
  --style minimal-clean
```

### Article Covers

```bash
# Tech blog
python3 ${SKILL_DIR}/scripts/cover_image.py \
  "大模型时代的内容创作革命" \
  --style gradient-mesh

# Business article
python3 ${SKILL_DIR}/scripts/cover_image.py \
  "2024年营销策略趋势" \
  --style bold-typography \
  --subtitle "从AI到私域，全面解析"
```

## Tips

1. **Content First**: Provide clear, structured content for best results
2. **Style Matching**: Match style to your audience and platform
3. **Layout Selection**: Use auto-detection or reference the layout guide
4. **Batch Generation**: Generate multiple images at once for content series
5. **Review Output**: AI-generated images may need refinement prompts
