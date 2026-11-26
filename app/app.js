const views = ["overview","map","discoveries","vehicles","missions","secrets","saved","progress"];
const labels = {overview:"VUE D'ENSEMBLE",map:"CARTE INTERACTIVE",discoveries:"DÉCOUVERTES",vehicles:"VÉHICULES",missions:"MISSIONS & ACTIVITÉS",secrets:"SECRETS & COLLECTIONS",saved:"MES FAVORIS",progress:"MA PROGRESSION"};
const $ = (s, root=document) => root.querySelector(s);
const $$ = (s, root=document) => [...root.querySelectorAll(s)];
let favorites = new Set(JSON.parse(localStorage.getItem("gta6-favorites") || "[]"));
let found = new Set(JSON.parse(localStorage.getItem("gta6-found") || "[]"));
function toast(message){const el=$("#toast");el.textContent=message;el.classList.add("show");clearTimeout(toast.timer);toast.timer=setTimeout(()=>el.classList.remove("show"),2300)}
function showView(name){if(!views.includes(name))return;$$(".view").forEach(v=>v.classList.toggle("active",v.id===`view-${name}`));$$(".nav-item").forEach(b=>b.classList.toggle("active",b.dataset.view===name));$("#crumb").textContent=labels[name];window.scrollTo({top:0,behavior:"smooth"});if(name==="map")refreshMap()}
$$(".nav-item").forEach(b=>b.addEventListener("click",()=>showView(b.dataset.view)));
$$("[data-goto]").forEach(b=>b.addEventListener("click",()=>showView(b.dataset.goto)));
function refreshStats(){$("#foundCount").textContent=found.size;$("#favoriteCount").textContent=favorites.size;$("#foundBar").style.width=Math.min(found.size/20*100,100)+"%"}
refreshStats();
$("#premiumButton").addEventListener("click",()=>toast("Les offres premium seront activées après le lancement."));
$("#notifications").addEventListener("click",()=>toast("Aucune nouvelle alerte pour le moment."));
$("#globalSearch").addEventListener("keydown",e=>{if(e.key==="Enter"){showView("discoveries");toast("La recherche sera reliée à la base de découvertes.")}});
document.addEventListener("keydown",e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==="k"){e.preventDefault();$("#globalSearch").focus()}});
const mapFilters=$$(".filter-group input");
function refreshMap(){const selected=mapFilters.filter(x=>x.checked).length;$("#markerCount").textContent=selected?"0 marqueur affiché · base en préparation":"Filtres masqués"}
mapFilters.forEach(x=>x.addEventListener("change",refreshMap));
$("#clearFilters").addEventListener("click",()=>{mapFilters.forEach(x=>x.checked=false);refreshMap()});
$("#mapSearch").addEventListener("input",()=>{});
let zoom=1;
function setZoom(next){zoom=Math.max(.8,Math.min(1.5,next));$(".map-art").style.transform=`scale(${zoom})`}
$("#zoomIn").addEventListener("click",()=>setZoom(zoom+.1));
$("#zoomOut").addEventListener("click",()=>setZoom(zoom-.1));
$("#resetMap").addEventListener("click",()=>setZoom(1));
if("serviceWorker" in navigator && location.protocol.startsWith("http")){window.addEventListener("load",()=>navigator.serviceWorker.register("./sw.js").catch(()=>{}))}
