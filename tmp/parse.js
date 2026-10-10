const fs = require('fs');
for (const f of ['daily', 'weekly']) {
  const html = fs.readFileSync('C:/Users/ZhouXuan/.openclaw/workspace/tmp/' + f + '.html', 'utf8');
  const re = /<h2 class="h3 lh-condensed">[\s\S]*?<a href="\/([^"]+)"/g;
  let m, names = [];
  while ((m = re.exec(html))) names.push(m[1]);
  console.log('== ' + f + ' (' + names.length + ') ==');
  console.log(names.join('\n'));
  console.log('');
}
