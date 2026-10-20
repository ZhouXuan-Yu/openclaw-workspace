const fs = require('fs');
const tmp = process.env.TEMP;
function parse(f) {
  const h = fs.readFileSync(f, 'utf8');
  const arts = h.split('<article').slice(1);
  return arts.map(a => {
    const m = a.match(/<h2[\s\S]*?<a href="\/([^"]+)"/);
    const st = a.match(/([\d,]+)\s*stars\s*(today|this week)/);
    const desc = a.match(/<p class="col-9[^"]*">\s*([\s\S]*?)\s*<\/p>/);
    if (!m) return null;
    return m[1] + ' | +' + (st ? st[1] + ' stars ' + st[2] : '?') + ' | ' + (desc ? desc[1].replace(/<[^>]+>/g, '').trim().slice(0, 100) : '');
  }).filter(Boolean);
}
console.log('=== DAILY ===');
console.log(parse(tmp + '/gh_daily.html').join('\n'));
console.log('=== WEEKLY ===');
console.log(parse(tmp + '/gh_weekly.html').slice(0, 15).join('\n'));
