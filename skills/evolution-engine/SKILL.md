---
name: evolution-engine
description: "鑷繘鍖栧紩鎿庯細鍩轰簬 OpenSpace 鎬濊矾锛屾瘡娆′换鍔″悗鑷姩鍒嗘瀽鎴愯触锛岃Е鍙?Skill 杩涘寲锛團IX/DERIVED/CAPTURED锛夈€?
parent: ""
origin: "imported"
generation: 0
created: "2026-06-12"
metadata: {"openclaw":{"emoji":"馃К"}}
---

# Skill Evolution Engine 鈥?鑷繘鍖栧紩鎿?
鍩轰簬 OpenSpace 鎬濊矾锛岄€傞厤 OpenClaw 鏂囦欢绯荤粺鏋舵瀯銆備笁绉嶈繘鍖栨ā寮忥細FIX / DERIVED / CAPTURED銆?
## 姒傝堪

姣忔浠诲姟鎵ц鍚庯紝鑷姩鍒嗘瀽缁撴灉锛屽喅瀹氭槸鍚﹁Е鍙戣繘鍖栵細
- **FIX**: 淇鍑洪敊/杩囨椂鐨?Skill锛坒ailure >= 2 瑙﹀彂锛?- **DERIVED**: 浠庣幇鏈?Skill 鍒涘缓澧炲己鐗堬紙鐢ㄦ埛绾犳瑙﹀彂锛?- **CAPTURED**: 浠庢垚鍔熸墽琛屼腑鎹曡幏鍙鐢ㄦā寮忥紙鎴愬姛+鏃燬kill瑙﹀彂锛?
## 杩涘寲瑙﹀彂鏉′欢

| 妯″紡 | 瑙﹀彂鏉′欢 | 鎿嶄綔 |
|------|---------|------|
| FIX | Skill 鎵ц澶辫触 鈮?2娆?| 鍘熷湴淇 SKILL.md |
| DERIVED | 鐢ㄦ埛璇?涓嶈杩欐牱"/"鎹釜鏂瑰紡" | 鍒涘缓澧炲己鐗堬紙甯?parent锛?|
| CAPTURED | 浠诲姟鎴愬姛 + 鏃犵幇鏈?Skill 鍖归厤 | 鎹曡幏涓烘柊 Skill |

## 鏂囦欢缁撴瀯

```
skills/
鈹溾攢鈹€ evolution-engine/
鈹?  鈹溾攢鈹€ SKILL.md          # 鏈枃浠?鈹?  鈹斺攢鈹€ .skill_id         # 鍞竴鏍囪瘑
鈹溾攢鈹€ memory/evolution/.skill-quality.json   # 鍏ㄥ眬璐ㄩ噺璁℃暟鍣?鈹斺攢鈹€ ...
```

## SKILL.md Frontmatter 鎵╁睍瑙勮寖

```yaml
---
name: skill-name
description: "绠€鐭弿杩?
parent: ""           # 鐖?Skill ID锛堣繘鍖栭摼锛岀┖=鏍硅妭鐐癸級
origin: "imported"   # imported | captured | derived | fixed
generation: 0        # 杩涘寲浠ｆ暟锛團IX/DERIVED 鏃?+1锛?created: "2026-06-12"
---
```

## 璐ㄩ噺璁℃暟鍣?(memory/evolution/.skill-quality.json)

```json
{
  "version": 1,
  "skills": {
    "skill-name": {
      "success": 0,
      "failure": 0,
      "last_used": "2026-06-12T02:30:00+08:00",
      "last_status": "success",
      "error_types": []
    }
  },
  "evolution_log": []
}
```

## 闆嗘垚鐐?
| 缁勪欢 | 闆嗘垚鏂瑰紡 |
|------|---------|
| 鍙嶅皠绠￠亾 (23:30 cron) | 鎵ц鍚庡垎鏋?鈫?瑙﹀彂杩涘寲 |
| 璁板繂鏁村悎 (02:00 cron) | 璇嗗埆閲嶅妯″紡 鈫?鍗囩骇涓?Skill |
| AGENTS.md | 鍙嶅皠绠￠亾绔犺妭宸叉墿灞?|
| learnings.md | 澶辫触鏁欒鑷姩鍐欏叆 |


