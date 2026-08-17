
(function(){
  const q=document.getElementById('q'),r=document.getElementById('results');
  if(!q)return;
  const esc=s=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  q.addEventListener('input',()=>{
    const x=q.value.trim().toLowerCase();
    if(!x){r.innerHTML='';return;}
    const hits=VOCAB_INDEX.filter(t=>(t.name+' '+t.kind+' '+t.definition).toLowerCase().includes(x)).slice(0,50);
    r.innerHTML=hits.length
      ? hits.map(t=>`<div class="result"><a href="${t.path}"><code>${esc(t.name)}</code></a> <span class="subtle">${esc(t.kind)}</span><br>${esc(t.definition)}</div>`).join('')
      : '<p class="subtle">No matching terms.</p>';
  });
})();
