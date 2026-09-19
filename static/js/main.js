function toggleFaq(btn){
  const container = btn.closest('.faq-item');
  const content = container.querySelector('.faq-content');
  const icon = btn.querySelector('.icon-chevron');
  const isHidden = content.classList.contains('hidden');
  document.querySelectorAll('.faq-item').forEach(item=>{
    item.querySelector('.faq-content').classList.add('hidden');
    const ic=item.querySelector('.icon-chevron'); if(ic) ic.classList.remove('rotate-180');
  });
  if(isHidden){ content.classList.remove('hidden'); if(icon) icon.classList.add('rotate-180'); }
}
function copyToClipboard(text, btnElement){
  navigator.clipboard.writeText(text).then(()=>{
    const textSpan = btnElement.querySelector('.copy-text');
    const originalText = textSpan ? textSpan.textContent : 'Salin';
    if(textSpan) textSpan.textContent='Tersalin!';
    btnElement.classList.add('bg-primary-fixed','text-primary');
    setTimeout(()=>{
      if(textSpan) textSpan.textContent=originalText;
      btnElement.classList.remove('bg-primary-fixed','text-primary');
    },2000);
  }).catch(()=>{ alert('Gagal menyalin: '+text); });
}

// ── typing effect ──
function runTyping(el){
  const texts = JSON.parse(el.dataset.typing || '[]');
  if(!texts.length) return;
  let idx=0, char=0, deleting=false;
  const speed = 90, pause=1800, delSpeed=45;
  el.classList.add('typing-cursor');
  function tick(){
    const cur = texts[idx];
    if(!deleting){
      el.textContent = cur.slice(0, char+1);
      char++;
      if(char===cur.length){ deleting=true; setTimeout(tick, pause); return; }
      setTimeout(tick, speed + Math.random()*40);
    } else {
      el.textContent = cur.slice(0, char-1);
      char--;
      if(char===0){ deleting=false; idx=(idx+1)%texts.length; setTimeout(tick, 300); return; }
      setTimeout(tick, delSpeed);
    }
  }
  tick();
}

// ── reveal on scroll + pop stagger ──
function initReveal(){
  const els = document.querySelectorAll('.reveal');
  if(!els.length) return;
  const obs = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){ e.target.classList.add('active'); obs.unobserve(e.target); }
    });
  }, {threshold:0.12});
  els.forEach(el=>obs.observe(el));
}

document.addEventListener('DOMContentLoaded',()=>{
  // typing
  document.querySelectorAll('[data-typing]').forEach(runTyping);
  initReveal();

  // hamburger modal
  const btn=document.getElementById('hamburgerBtn');
  const overlay=document.getElementById('mobileNavOverlay');
  const drawer=document.getElementById('mobileNavDrawer');
  const icon=document.getElementById('hamburgerIcon');
  function openNav(){
    overlay.classList.remove('hidden'); drawer.classList.remove('hidden');
    requestAnimationFrame(()=>{ overlay.classList.remove('opacity-0'); drawer.classList.add('pop-card'); });
    btn.setAttribute('aria-expanded','true'); if(icon) icon.textContent='close';
    document.body.style.overflow='hidden';
  }
  function closeNav(){
    overlay.classList.add('opacity-0'); drawer.classList.remove('pop-card');
    setTimeout(()=>{ overlay.classList.add('hidden'); drawer.classList.add('hidden'); }, 220);
    btn.setAttribute('aria-expanded','false'); if(icon) icon.textContent='menu';
    document.body.style.overflow='';
  }
  if(btn && overlay && drawer){
    btn.addEventListener('click', ()=>{ const open=btn.getAttribute('aria-expanded')==='true'; open?closeNav():openNav(); });
    overlay.addEventListener('click', closeNav);
    drawer.querySelectorAll('a').forEach(a=>a.addEventListener('click', closeNav));
    document.addEventListener('keydown', e=>{ if(e.key==='Escape') closeNav(); });
  }

  // search
  const searchInput=document.getElementById('blogSearchInput');
  if(searchInput){
    searchInput.addEventListener('input', e=>{
      const q=e.target.value.toLowerCase();
      document.querySelectorAll('article[data-searchable]').forEach(a=>{
        a.style.display = a.innerText.toLowerCase().includes(q) ? '' : 'none';
      });
    });
  }
  document.querySelectorAll('[data-filter]').forEach(button=>{
    button.addEventListener('click', ()=>{
      document.querySelectorAll('[data-filter]').forEach(btn=>{
        btn.classList.remove('bg-primary','text-on-primary','font-semibold','shadow-xs');
        btn.classList.add('bg-surface-container-lowest','text-on-surface-variant','font-medium');
      });
      button.classList.add('bg-primary','text-on-primary','font-semibold','shadow-xs');
      button.classList.remove('bg-surface-container-lowest','text-on-surface-variant','font-medium');
      const f=button.dataset.filter;
      document.querySelectorAll('[data-category]').forEach(card=>{
        if(f==='all' || card.dataset.category===f) card.style.display='';
        else card.style.display='none';
      });
    });
  });
});
