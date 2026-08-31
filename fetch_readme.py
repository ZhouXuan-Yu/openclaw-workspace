import subprocess

urls = {
    'prime-agent': 'https://raw.githubusercontent.com/PrimeIntellect-ai/prime-agent/main/README.md',
    'reverse-skill': 'https://raw.githubusercontent.com/zhaoxuya520/reverse-skill/main/README.md',
}
for name, url in urls.items():
    try:
        out = subprocess.run(['curl.exe', '-s', '-L', '--max-time', '25', url], capture_output=True, text=True, encoding='utf-8', errors='replace')
        text = out.stdout
        print('=== {} === len: {}'.format(name, len(text)))
        print(text[:2500])
        print()
    except Exception as e:
        print(name, 'ERROR', e)
