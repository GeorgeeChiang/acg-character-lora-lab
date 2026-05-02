# 產圖測試計畫

目的：測試角色 LoRA 是否能保留角色識別度，同時允許不同構圖。

比較不同 checkpoint 時，請固定 seed 組、base model、sampler、LoRA strength 與 negative prompt。

## 預設 Prompt 組件

Trigger 佔位：

```txt
<trigger>, 1girl
```

品質與風格基準：

```txt
ACG illustration, anime style, detailed eyes, clean lineart, soft shading
```

Negative 基準：

```txt
low quality, worst quality, bad anatomy, extra fingers, missing fingers, distorted face, text, watermark, logo
```

LoRA strength 起點：

```txt
0.70
```

## 10 組構圖測試

1. 頭像識別度
   - Prompt：`<trigger>, 1girl, close-up portrait, looking at viewer, gentle smile`
   - 目的：測臉、眼睛、髮型與基礎相似度。

2. 上半身角色姿勢
   - Prompt：`<trigger>, 1girl, upper body, standing in classroom, one hand on chest, soft morning light`
   - 目的：測標準 ACG 角色構圖可用性。

3. 全身站姿
   - Prompt：`<trigger>, 1girl, full body, standing, simple background, neutral pose`
   - 目的：測服裝與輪廓一致性。

4. 側臉角度
   - Prompt：`<trigger>, 1girl, side view, looking away, wind blowing hair, outdoor walkway`
   - 目的：測非正面角度下的角色識別度。

5. 回頭構圖
   - Prompt：`<trigger>, 1girl, looking back over shoulder, three-quarter view, evening street`
   - 目的：測鏡頭角度彈性。

6. 窗邊坐姿
   - Prompt：`<trigger>, 1girl, sitting by window, knees together, soft backlight, quiet room`
   - 目的：測坐姿與情緒場景。

7. 動態動作
   - Prompt：`<trigger>, 1girl, running, dynamic pose, hair flowing, school courtyard`
   - 目的：測姿勢彈性與動態破圖。

8. 情緒特寫
   - Prompt：`<trigger>, 1girl, close-up, teary eyes, sad expression, night lighting`
   - 目的：測表情變化，同時保持識別度。

9. 服裝變化
   - Prompt：`<trigger>, 1girl, casual hoodie, city cafe, relaxed smile`
   - 目的：測角色在換裝後是否仍能維持身分。

10. Inpaint 修復測試
   - Prompt：先產生任一手部或臉部失敗圖，再只對錯誤區域 inpaint。
   - 目的：確認修復流程，而不只測原始產圖。

## 可選 ControlNet 測試

原始 prompt 測完後，可用 OpenPose 重複測試第 3、5、6、7 組。

評估：

- 姿勢是否跟參考圖一致？
- LoRA strength 0.60-0.85 時，角色識別度是否仍穩定？
- ControlNet 是否讓圖變得過度僵硬？

## 評分表

每張圖以 1-5 分評估：

- 角色相似度
- Prompt 遵循度
- 姿勢/構圖
- 臉部品質
- 手部/身體品質
- 服裝彈性
- 原圖過擬合風險

偏好的 checkpoint：

- 角色相似度平均 >= 4
- 姿勢/構圖平均 >= 3
- 過擬合風險 <= 2
- 不需要把 LoRA strength 拉到 0.9 以上
