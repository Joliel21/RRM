(() => {
  const pages = {
    'page-86.png': [
      ['Beacon for Rare Diseases','https://www.rarebeacon.org/',9,12,55,20],
      ['Cambridge Rare Disease Network — CamRARE','https://www.camraredisease.org/',66,12,61,20],
      ['Childhood Tumour Trust','https://www.childhoodtumourtrust.org.uk/',128,10,65,29],
      ["Matthew’s Friends",'https://www.matthewsfriends.org/',194,10,38,27],
      ["Matthew’s Friends KetoCollege",'https://www.matthewsfriends.org/ketocolleges/',232,10,38,27],
      ['Pitt Hopkins UK','https://pitthopkins.org.uk/',12,39,49,39],
      ['International Fibrodysplasia Ossificans Progressiva Association — IFOPA','https://www.ifopa.org/',66,40,62,30],
      ['Gene People','https://genepeople.org.uk/',177,42,92,24],
      ['Salivary Gland Cancer UK','https://salivaryglandcancer.uk/',131,55,52,48],
      ['The Muscle Help Foundation','https://www.musclehelp.com/',61,65,69,24],
      ['Niemann-Pick UK — NPUK','https://www.npuk.org/',13,79,51,47],
      ['Global Liver Institute','https://globalliver.org/',65,85,66,42],
      ['Medics for Rare Disease','https://www.m4rd.org/',194,67,70,54],
      ['Epilepsy Sparks','https://epilepsysparks.com/',130,101,65,40],
      ["Huntington’s Disease Youth Organization — HDYO",'https://www.hdyo.org/',198,105,67,47],
      ['Congenital Hyperinsulinism International / Hyperinsulinism Hope','https://congenitalhi.org/',68,117,67,34],
      ['Tuberous Sclerosis Association','https://tuberous-sclerosis.org/',12,136,53,45],
      ['Ataxia and Me','https://www.ataxiaandme.org/',67,143,64,47],
      ["Gaucher’s Association",'https://www.gauchers.org.uk/',135,134,58,48],
      ['PSP Association','https://www.pspassociation.org.uk/',203,140,59,36],
      ['The CATS Foundation — Cure and Action for Tay-Sachs','https://cats-foundation.org/',9,178,55,44],
      ['Barth Syndrome Foundation','https://www.barthsyndrome.org/',69,178,64,37],
      ['Wolfram Syndrome UK','https://www.wolframsyndrome.co.uk/',135,176,62,36],
      ['FOP Friends','https://www.fopfriends.com/',69,207,64,39],
      ["International Waldenstrom’s Macroglobulinemia Foundation — IWMF",'https://iwmf.com/',135,211,61,40],
      ['Charcot-Marie-Tooth UK — CMTUK','https://www.cmt.org.uk/',202,204,63,47],
      ['Metabolic Support UK','https://metabolicsupportuk.org/',68,238,65,43],
      ['PTLS Hope Research Foundation','https://www.ptlshope.org/',135,246,62,38],
      ['VHL UK/Ireland','https://vhl-uk-ireland.org/',10,211,53,45],
      ['Schinzel-Giedion Syndrome Foundation','https://schinzel-giedion.org/',10,263,57,50],
      ['Cards2Warriors','https://www.cards2warriors.org/',68,287,65,46],
      ['wAIHA Warriors','https://waihawarriors.org/',136,293,60,48],
      ['CureDuchenne','https://www.cureduchenne.org/',9,337,62,44],
      ['Teach RARE','https://teachrare.org/',194,329,72,51]
    ],
    'page-87.png': [
      ['Rett UK','https://www.rettuk.org/',8,9,64,25],['DEBRA UK','https://www.debra.org.uk/',80,7,54,28],
      ['Alström Syndrome UK','https://www.alstrom.org.uk/',7,37,73,24],['Courageous Parents Network','https://courageousparentsnetwork.org/',84,35,65,28],
      ['Ring20 Research and Support UK','https://www.ring20researchsupport.co.uk/',7,61,72,24],['EURORDIS — Rare Diseases Europe','https://www.eurordis.org/',82,61,69,27],
      ['PBC Foundation','https://www.pbcfoundation.org.uk/',7,84,70,27],["Annabelle’s Challenge",'https://www.annabelleschallenge.org/',84,85,61,30],
      ['CSF Leak Association','https://csfleak.info/',7,111,60,44],['HypoPARAthyroidism Association','https://www.hypopara.org/',67,109,57,46],['CYFIP2 Network','https://www.cyfip2network.org/',121,113,52,42],
      ['SMA Europe','https://www.sma-europe.eu/',6,157,58,43],['Lysosomal and Glycoprotein Disease Association — LGDA','https://www.lgda.org.uk/',63,154,57,48],['The Ehlers-Danlos Society','https://www.ehlers-danlos.com/',118,155,54,47],
      ['Ehlers-Danlos Support UK','https://www.ehlers-danlos.org/',6,199,61,29],['Nicolaides-Baraitser Syndrome Foundation — NCBRS','https://www.ncbrs.org/',67,197,51,33],['Cure CLCN4','https://cureclcn4.org/',118,196,55,32],
      ['Chromosome 6 Foundation','https://www.chromosome6.org/',117,225,55,30],['PRISMS','https://www.prisms.org/',59,233,59,31],['CPA Research Foundation','https://www.cparesearch.org/',118,243,55,31],
      ['Rare Diseases International','https://www.rarediseasesinternational.org/',7,267,59,30],['The Sturge-Weber Foundation','https://sturge-weber.org/',67,267,68,30],
      ['HBA Support','https://hbasupport.org/',7,293,63,25],['Keep Me Breathing','https://keepmebreathing.com/',71,293,67,25],
      ['International Niemann-Pick Disease Registry — INPDR','https://www.inpdr.org/',7,324,51,34],['Rare Genes Movement','https://raregenesmovement.org/',58,325,65,29],['Situs Foundation','https://situsfoundation.org/',122,323,50,34]
    ]
  };
  const W=280,H=397;
  function apply(img){
    if (img.dataset.logoHotspotsApplied) return;
    const key=Object.keys(pages).find(k => (img.currentSrc||img.src||'').includes(k));
    if(!key) return;
    img.dataset.logoHotspotsApplied='true';
    const parent=img.parentElement;
    if(!parent) return;
    const position=getComputedStyle(parent).position;
    if(position==='static') parent.style.position='relative';
    const layer=document.createElement('div');
    layer.className='rrm-logo-hotspots';
    Object.assign(layer.style,{position:'absolute',inset:'0',zIndex:'30',pointerEvents:'none'});
    pages[key].forEach(([label,href,x,y,w,h])=>{
      const a=document.createElement('a');
      a.href=href;a.target='_blank';a.rel='noopener noreferrer';a.title=label;a.setAttribute('aria-label',label);
      Object.assign(a.style,{position:'absolute',left:`${x/W*100}%`,top:`${y/H*100}%`,width:`${w/W*100}%`,height:`${h/H*100}%`,display:'block',pointerEvents:'auto'});
      layer.appendChild(a);
    });
    parent.appendChild(layer);
  }
  function scan(){document.querySelectorAll('img').forEach(apply)}
  new MutationObserver(scan).observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['src']});
  window.addEventListener('load',scan); scan();
})();
