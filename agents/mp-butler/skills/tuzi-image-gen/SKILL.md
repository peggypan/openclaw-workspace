---
name: tuzi-image-gen
description: 调用 TuziAPI 生成图片。当用户需要生成图片、AI绘画、文生图时使用。支持根据文本描述生成图片并返回图片URL。
---

# TuziAPI 图片生成

调用 TuziAPI 接口根据文本描述生成图片。

## 接口信息

- **接口地址**: `https://api.dashu.ai/tuziapi/images_generation`
- **鉴权方式**: 请求参数中携带 `token`
- **API Key**: `sk-ULZz57jJf2lkANMJsbZdxMEhVVWGgWl7xi1pluvfW0zntRtE`

## 使用方法

### 生成图片

```bash
curl -X POST "https://api.dashu.ai/tuziapi/images_generation" \
     -d "prompt=描述图片内容的英文提示词" \
     -d "token=sk-ULZz57jJf2lkANMJsbZdxMEhVVWGgWl7xi1pluvfW0zntRtE"
```

### 响应格式

返回 OpenAI 兼容格式：

```json
{
  "data": [
    {
      "url": "https://cdn-path/image.png",
      "revised_prompt": "模型实际理解的提示词"
    }
  ]
}
```

### 提取图片

从 `data[0].url` 获取生成的图片地址。

## 注意事项

- 提示词建议使用英文以获得更精确的效果
- 生成过程通常需要 10-20 秒
- 如返回 `Error: token is required` 表示鉴权失败
- 如返回 `Error: prompt is required` 表示缺少提示词
