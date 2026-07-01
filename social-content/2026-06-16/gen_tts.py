import os, sys

# Remove proxy from env
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']:
    os.environ.pop(k, None)

import edge_tts, asyncio

async def main():
    text = open(r'C:\Users\ZhouXuan\.openclaw\workspace\social-content\2026-06-16\tts-text.txt', encoding='utf-8').read()
    comm = edge_tts.Communicate(text, 'zh-CN-YunxiNeural', proxy='')
    await comm.save(r'C:\Users\ZhouXuan\.openclaw\workspace\social-content\2026-06-16\tts.mp3')
    print('TTS done')

asyncio.run(main())
