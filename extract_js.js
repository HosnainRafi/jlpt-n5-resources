const entry = document.querySelector('.entry-content') || document.body;
const audios = [...document.querySelectorAll('audio')].map(a=>a.src);
const imgs = [...entry.querySelectorAll('img')].map(i=>i.src).filter(u=>u.includes('/image/'));
const pdf = (()=>{const a=[...entry.querySelectorAll('a[href]')].find(x=>x.href.endsWith('.pdf')); return a?a.href:null;})();
const text = document.body.innerText;
// answer key
const ansPart = (text.match(/Answer Key[\s\S]*?(?=JLPT N5 Kanji Lesson|New words|Download)/)||[])[0]||'';
const answers = [...ansPart.matchAll(/Question\s+(\d+)\s*:\s*(.+)/g)].map(m=>({q:+m[1], a:m[2].trim()}));
// new words
const vocPart = (text.match(/New words[\s\S]*?(?=View transcript|Learn JLPT N5 Grammar|contact me|Download the video)/)||[])[0]||'';
const vocLines = vocPart.split('\n').map(l=>l.trim()).filter(l=>l && !/^New words/.test(l));
const voc = vocLines.map(l=>{const m=l.match(/^(.+?)\s*\((.+?)\)\s*:\s*(.+)$/); return m?{jp:m[1].trim(),rm:m[2].trim(),en:m[3].trim()}:{jp:l,rm:'',en:''};});
return JSON.stringify({title: document.querySelector('h1')?.innerText, audios, imgs, pdf, answers, voc});
