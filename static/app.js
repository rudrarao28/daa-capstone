const $ = (id) => document.getElementById(id);
let cityData = null;
const positions = {
  "City Center":[300,165], "Railway Station":[130,75], "University":[310,55],
  "Hospital":[490,105], "Shopping Mall":[455,245], "Bus Stand":[115,245],
  "Airport Road":[535,320], "Technology Park":[285,305]
};

async function loadCity(){
  const response = await fetch('/api/locations');
  cityData = await response.json();
  $('locationCount').textContent = cityData.locations.length;
  $('roadCount').textContent = cityData.roads.length;
  for(const id of ['start','end']){
    $(id).innerHTML = cityData.locations.map(name => `<option value="${name}">${name}</option>`).join('');
  }
  $('start').value = 'City Center';
  $('end').value = 'Airport Road';
  drawNetwork([]);
}

function line(a,b,cls){
  const p1=positions[a], p2=positions[b];
  return `<line class="${cls}" x1="${p1[0]}" y1="${p1[1]}" x2="${p2[0]}" y2="${p2[1]}"/>`;
}
function drawNetwork(path){
  if(!cityData) return;
  $('edges').innerHTML = cityData.roads.map(r=>line(r.source,r.destination,'road')).join('');
  const pathLines=[];
  for(let i=0;i<path.length-1;i++) pathLines.push(line(path[i],path[i+1],'route-road'));
  $('routeEdges').innerHTML=pathLines.join('');
  const active=new Set(path);
  $('nodes').innerHTML=cityData.locations.map(name=>{
    const [x,y]=positions[name];
    const short=name.length>16?name.slice(0,14)+'…':name;
    return `<g class="node ${active.has(name)?'active':''}"><circle cx="${x}" cy="${y}" r="7"/><text x="${x}" y="${y+22}">${short}</text></g>`;
  }).join('');
}

$('findRoute').addEventListener('click', async ()=>{
  const button=$('findRoute');
  button.disabled=true; button.textContent='Calculating route…';
  $('routeResult').className='result';
  $('routeResult').innerHTML='<div class="result-symbol">◌</div><div><b>Calculating shortest path</b><p>Processing the selected road network.</p></div>';
  try{
    const response=await fetch('/api/route',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({start:$('start').value,end:$('end').value,algorithm:$('algorithm').value})});
    const data=await response.json();
    if(!response.ok) throw new Error(data.error||'Unable to calculate route.');
    if(!data.found){
      $('routeResult').innerHTML=`<div class="result-symbol">!</div><div><b>No route found</b><p>${data.message}</p></div>`;
      drawNetwork([]); return;
    }
    $('routeResult').innerHTML=`<div class="result-symbol">✓</div><div><b>Shortest route found</b><div class="distance">${data.distance.toFixed(2)} km</div><p class="path-text">${data.path.join('  →  ')}</p></div>`;
    drawNetwork(data.path);
  }catch(error){
    $('routeResult').innerHTML=`<div class="result-symbol">!</div><div><b>Calculation error</b><p>${error.message}</p></div>`;
  }finally{button.disabled=false;button.innerHTML='Calculate shortest route <span>→</span>';}
});

$('runBenchmark').addEventListener('click',async ()=>{
  const button=$('runBenchmark'), state=$('benchmarkState');
  button.disabled=true;button.textContent='Running…';state.textContent='Generating test graphs and measuring execution time…';
  $('benchmarkTable').innerHTML='';
  try{
    const response=await fetch('/api/benchmark');
    const rows=await response.json();
    $('benchmarkTable').innerHTML=`<table><thead><tr><th>VERTICES</th><th>EDGES</th><th>DIJKSTRA (MS)</th><th>BELLMAN-FORD (MS)</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${r.vertices}</td><td>${r.edges}</td><td class="dijkstra">${r.dijkstra_ms.toFixed(3)}</td><td class="bellman">${r.bellman_ford_ms.toFixed(3)}</td></tr>`).join('')}</tbody></table>`;
    state.textContent='Benchmark completed. Times are average measurements and may vary by computer.';
  }catch(error){state.textContent='Benchmark failed: '+error.message;}
  finally{button.disabled=false;button.textContent='Run benchmark ↗';}
});

loadCity().catch(error=>{ $('routeResult').innerHTML=`<div><b>Unable to load city data</b><p>${error.message}</p></div>`; });
