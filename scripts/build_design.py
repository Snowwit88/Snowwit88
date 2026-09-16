from pathlib import Path
P=Path(__file__).resolve().parents[1]
s=(P/'assets/header-dark.svg').read_text()
colors={'#0b1520':'#f7f3e9','#172d3c':'#e4ede9','#a8c2c9':'#4d6b74','#f4efdf':'#193845','#9ccacb':'#648f95','#d0dce0':'#3c5965','#9bb1bd':'#58737c','#f5eedb':'#fff7d8','#d8d5c6':'#ead6a5','#8fa5a4':'#c4a774','#ccb992':'#9e793b'}
for a,b in colors.items(): s=s.replace(a,b)
s=s.replace('midnight-blue','daylight').replace('Ivory typography','Dark typography')
(P/'assets/header-light.svg').write_text(s)
(P/'assets/typing.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="86" viewBox="0 0 1000 86" role="img" aria-labelledby="title">
<title id="title">保持好奇。阅读世界。动手创造。</title>
<style>
text {fill:#315965;font-family:Arial,'PingFang SC','Microsoft YaHei',sans-serif;font-size:28px;letter-spacing:4px}
.line{opacity:0;animation:show 15s infinite}.two{animation-delay:5s}.three{animation-delay:10s}
.reveal{animation:type 5s steps(5,end) infinite}.cursor{fill:#638c8f;animation:blink 1s steps(1,end) infinite}
@keyframes show{0%,32%{opacity:1}33%,100%{opacity:0}} @keyframes type{0%{width:0}45%,85%{width:160px}100%{width:0}}
@keyframes blink{50%{opacity:0}}
@media(prefers-color-scheme:dark){text{fill:#c5d9dc}.cursor{fill:#a8c2c9}}
@media(prefers-reduced-motion:reduce){.line{animation:none}.one{opacity:1}.reveal{animation:none;width:160px}.cursor{animation:none}}
</style><defs><clipPath id="reveal"><rect class="reveal" x="417" y="0" width="160" height="86"/></clipPath></defs>
<g clip-path="url(#reveal)"><text class="line one" x="420" y="54">保持好奇。</text><text class="line two" x="420" y="54">阅读世界。</text><text class="line three" x="420" y="54">动手创造。</text></g><rect class="cursor" x="583" y="30" width="2" height="27"/>
</svg>''')
(P/'assets/project-card.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="230" viewBox="0 0 1000 230" role="img" aria-labelledby="title desc"><title id="title">WeChat Ink · 微墨</title><desc id="desc">写作、配图与排版。点击卡片访问项目。</desc><defs><linearGradient id="shine"><stop stop-color="#b8d9d8" stop-opacity="0"/><stop offset=".5" stop-color="#b8d9d8" stop-opacity=".12"/><stop offset="1" stop-color="#b8d9d8" stop-opacity="0"/></linearGradient><clipPath id="bounds"><rect width="1000" height="230" rx="18"/></clipPath></defs><style>
.bg{fill:#edf2ef;stroke:#cedcd6}.title{fill:#173b46}.copy{fill:#4e6d75}.line{stroke:#5c9295}.shine{animation:sweep 9s ease-in-out infinite}@keyframes sweep{0%,15%{transform:translateX(-300px)}75%,100%{transform:translateX(1300px)}}
@media(prefers-color-scheme:dark){.bg{fill:#142834;stroke:#28404c}.title{fill:#f1eddd}.copy{fill:#a8c2c9}}@media(prefers-reduced-motion:reduce){.shine{animation:none;opacity:0}}
</style><rect class="bg" x="1" y="1" width="998" height="228" rx="18"/><g font-family="Arial,'PingFang SC','Microsoft YaHei',sans-serif"><text class="copy" x="38" y="40" font-size="12" letter-spacing="3">FEATURED WORK / 01</text><text class="title" x="36" y="101" font-size="40" font-weight="700">WeChat Ink · 微墨</text><text class="copy" x="38" y="142" font-size="20">写作、配图与排版，把时间留给表达。</text><text class="copy" x="38" y="195" font-size="13" letter-spacing="2">AI / WRITING / AUTOMATION</text><path class="line" d="M850 157l58-58m-58 0h58v58" fill="none" stroke-width="2"/></g><g clip-path="url(#bounds)"><rect class="shine" x="0" y="0" width="220" height="230" fill="url(#shine)"/></g></svg>''')
