"""GitHub 密钥有效性验证 — 测试密钥是否可用+有余额"""
import json, requests, time, sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

HISTORY_JSON = Path("tools/github-key-scanner/scan_history.json")
VERIFY_RESULTS = Path("tools/github-key-scanner/verify_results.json")
OBSIDIAN_DIR = Path("E:/Obsidian仓库/ZhouXuan私人领域/密钥存储")

PROVIDER_CHECKS = {
    "OpenAI类": {
        "url": "https://api.openai.com/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "OpenAI Proj": {
        "url": "https://api.openai.com/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "headers": lambda key: {"x-api-key": key, "anthropic-version": "2023-06-01"},
        "ok_status": [200, 400],  # 400 = valid key but bad request body
        "bad_status": 401,
    },
    "DeepSeek": {
        "url": "https://api.deepseek.com/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Google Gemini": {
        "url": lambda key: f"https://generativelanguage.googleapis.com/v1beta/models?key={key}",
        "headers": lambda key: {},
        "ok_status": 200,
    },
    "Google AI": {
        "url": lambda key: f"https://generativelanguage.googleapis.com/v1beta/models?key={key}",
        "headers": lambda key: {},
        "ok_status": 200,
    },
    "HuggingFace": {
        "url": "https://huggingface.co/api/whoami-v2",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Groq": {
        "url": "https://api.groq.com/openai/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Replicate": {
        "url": "https://api.replicate.com/v1/models",
        "headers": lambda key: {"Authorization": f"Token {key}"},
        "ok_status": 200,
    },
    "Perplexity": {
        "url": "https://api.perplexity.ai/chat/completions",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": [200, 400],
        "bad_status": 401,
    },
    "Mistral": {
        "url": "https://api.mistral.ai/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Cohere": {
        "url": "https://api.cohere.com/v2/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Together": {
        "url": "https://api.together.xyz/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Fireworks AI": {
        "url": "https://api.fireworks.ai/inference/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Fireworks": {
        "url": "https://api.fireworks.ai/inference/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "通义千问": {
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "DashScope": {
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Moonshot Kimi": {
        "url": "https://api.moonshot.cn/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "百川智能": {
        "url": "https://api.baichuan-ai.com/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "智谱": {
        "url": "https://open.bigmodel.cn/api/paas/v4/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "MiniMax": {
        "url": "https://api.minimax.chat/v1/text/chatcompletion_v2",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": [200, 400],
        "bad_status": 401,
    },
    "MiniMax JWT": {
        "url": "https://api.minimax.chat/v1/text/chatcompletion_v2",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": [200, 400],
        "bad_status": 401,
    },
    "SiliconFlow": {
        "url": "https://api.siliconflow.cn/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
    "Unknown": {
        "url": "https://api.openai.com/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
        "ok_status": 200,
    },
}

def check_status(status, provider_config):
    ok = provider_config.get("ok_status", 200)
    bad = provider_config.get("bad_status")
    ok_list = ok if isinstance(ok, list) else [ok]
    if status in ok_list:
        return "valid"
    if bad and status in (bad if isinstance(bad, list) else [bad]):
        return "invalid_auth"
    if status == 429:
        return "rate_limited"
    if status in (401, 403):
        return "invalid_auth"
    return f"unknown_{status}"

def verify_key(provider, key):
    config = PROVIDER_CHECKS.get(provider)
    if not config:
        return {"status": "unknown", "error": f"No check config for {provider}"}

    url = config["url"]
    if callable(url):
        url = url(key)
    headers = config["headers"](key)
    headers["User-Agent"] = "GitHub-Key-Scanner/1.0"

    try:
        r = requests.get(url, headers=headers, timeout=15)
        status = check_status(r.status_code, config)
        result = {"status": status, "http_code": r.status_code}

        if status == "valid":
            resp = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
            # Try to extract balance/plan info if available
            if "data" in resp:
                result["models_count"] = len(resp.get("data", []))
            elif isinstance(resp, list):
                result["models_count"] = len(resp)
            if "hard_limit_usd" in resp:
                result["limit_usd"] = resp["hard_limit_usd"]
            if "total_granted" in resp or "total_used" in resp:
                result["grant_info"] = True
        elif status == "invalid_auth":
            result["error"] = "Invalid or revoked key"
        elif status == "rate_limited":
            result["error"] = "Rate limited"

        return result
    except requests.exceptions.Timeout:
        return {"status": "timeout", "error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"status": "connection_error", "error": "Connection failed"}
    except Exception as e:
        return {"status": "error", "error": str(e)[:100]}

def main():
    if not HISTORY_JSON.exists():
        print("No scan history found. Run scan first.")
        return

    h = json.loads(HISTORY_JSON.read_text(encoding="utf-8"))
    sk = h.get("seen_keys", {})
    if not sk:
        print("No keys in history.")
        return

    # Load previous verify results if any
    prev_results = {}
    if VERIFY_RESULTS.exists():
        prev_results = json.loads(VERIFY_RESULTS.read_text(encoding="utf-8"))

    valid_keys = []
    invalid_keys = []
    results = {}

    total = len(sk)
    print("=" * 60)
    print(f"🔬 密钥验证 | {total} keys | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    for i, (kid, v) in enumerate(sk.items(), 1):
        provider = v["provider"]
        key = v.get("key_full", "")
        if not key:
            print(f"[{i}/{total}] {provider} — ❌ no full key stored")
            invalid_keys.append({"key_id": kid, "provider": provider, "reason": "no_full_key"})
            continue

        # Check cache
        if kid in prev_results and prev_results[kid].get("status") == "valid":
            print(f"[{i}/{total}] {provider} — ✅ cached valid")
            valid_keys.append({**v, "key_id": kid, "verify": prev_results[kid]})
            results[kid] = prev_results[kid]
            continue

        print(f"[{i}/{total}] {provider} ({v['repo']}) — testing...", end=" ", flush=True)
        result = verify_key(provider, key)
        results[kid] = result

        if result.get("status") == "valid":
            print("✅ VALID")
            valid_keys.append({**v, "key_id": kid, "verify": result})
        elif result.get("status") == "invalid_auth":
            print("❌ INVALID")
            invalid_keys.append({**v, "key_id": kid, "reason": "invalid_auth"})
        else:
            print(f"⚠️ {result.get('status', 'unknown')}")
            # Unknown status: keep as potentially valid but flagged
            invalid_keys.append({**v, "key_id": kid, "reason": result.get("status", "unknown")})

        time.sleep(0.8)  # Rate limit ourselves

    # Save results
    results_data = {
        "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total": total,
        "valid": len(valid_keys),
        "invalid": len(invalid_keys),
        "results": results
    }
    VERIFY_RESULTS.write_text(json.dumps(results_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Print summary
    print("\n" + "=" * 60)
    print("📊 验证结果")
    print(f"   ✅ 有效: {len(valid_keys)}")
    print(f"   ❌ 无效: {len(invalid_keys)}")
    if valid_keys:
        print("\n有效密钥:")
        for vk in valid_keys:
            print(f"   [{vk['provider']}] {vk['repo']}/{vk['file']} → {vk['key_preview']}")
    print("=" * 60)

    # Update scan_history with verify status
    for kid, result in results.items():
        if kid in sk:
            sk[kid]["verified"] = result.get("status")
            sk[kid]["verified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    h["seen_keys"] = sk
    HISTORY_JSON.write_text(json.dumps(h, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
