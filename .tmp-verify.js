const fs=require('fs');
const p='E:/Obsidian仓库/ZhouXuan私人领域/人物画像.md';
const t=fs.readFileSync(p,'utf8');
const L=t.split(/\r?\n/);
const idx=L.findIndex(x=>x.includes('archived_candidate'));
console.log('status line '+(idx+1)+':');
console.log(L[idx]);
const j=L.findIndex(x=>x.includes('### 10-01 晚间补充'));
console.log('\nevening section at line '+(j+1)+':');
console.log(L.slice(j,j+5).join('\n'));
console.log('\ntotal lines '+L.length);
try{fs.unlinkSync('C:/Users/ZhouXuan/.openclaw/workspace/.tmp-verify.ps1');console.log('tmp removed');}catch(e){}
