(this.webpackJsonpfloresta2030=this.webpackJsonpfloresta2030||[]).push([[0],{60:function(e,n,t){},82:function(e,n,t){"use strict";t.r(n);var a,i=t(2),o=t(32),s=t.n(o),r=t(37),c=t(96),p=(t(60),t(11)),l=t.n(p),u=t(17),d=t(22),f=t(33),h=t(34),m=t(39),g=t(38);var v=t(35),b=t.n(v),y=t(97),w=t(98),M=t(9),j=function(e){Object(m.a)(t,e);var n=Object(g.a)(t);function t(){var e;Object(f.a)(this,t);for(var o=arguments.length,s=new Array(o),r=0;r<o;r++)s[r]=arguments[r];return(e=n.call.apply(n,[this].concat(s))).mapRef=i.createRef(),e.map=void 0,e.areasEntities={},e.pinEntities={},e.mapChanged=new w.a,e.infobox=void 0,e.updatePins=Object(d.a)(l.a.mark((function n(){var t,i,o,s,r,c,p,d,f,h,m,g,v,y,w,M,j,E;return l.a.wrap((function(n){for(;;)switch(n.prev=n.next){case 0:for(i in t=e.map.getZoom(),e.pinEntities){o=Object(u.a)(e.pinEntities[i]);try{for(o.s();!(s=o.n()).done;)r=s.value,e.map.entities.remove(r)}catch(l){o.e(l)}finally{o.f()}delete e.pinEntities[i]}if(t<10){for(c in e.areasEntities){p=Object(u.a)(e.areasEntities[c]);try{for(p.s();!(d=p.n()).done;)f=d.value,e.map.entities.remove(f)}catch(l){p.e(l)}finally{p.f()}delete e.areasEntities[c]}e.areasEntities={}}return n.next=5,b.a.get("https://rodvieirasilva.pythonanywhere.com/pins?zoom=".concat(t,"&bounds=").concat(e.map.getBounds().bounds));case 5:h=n.sent,m=Object(u.a)(h.data);try{for(m.s();!(g=m.n()).done;){v=g.value,e.areasEntities[v.name]=e.areasEntities[v.name]||[],e.pinEntities[v.name]=e.pinEntities[v.name]||[],!1,y=Object(u.a)(v.geos);try{for(y.s();!(w=y.n()).done;)M=w.value,(j=new a.Maps.Pushpin(new a.Maps.Location(M.lat,M.lng),{text:v.text,color:v.color})).pin=v,e.pinEntities[v.name].push(j),e.map.entities.push(j),a.Maps.Events.addHandler(j,"click",e.pushpinClicked),console.log(t,h.data.length),t>=10&&h.data.length<6&&e.areasEntities[v.name].length!=v.geos.length&&(E=a.Maps.GeoJson.read(M.json),e.areasEntities[v.name].push(E),e.map.entities.push(E))}catch(l){y.e(l)}finally{y.f()}}}catch(l){m.e(l)}finally{m.f()}case 8:case"end":return n.stop()}}),n)}))),e.pushpinClicked=function(n){var t=n.target.pin;t&&e.infobox.setOptions({location:n.target.getLocation(),title:t.title,description:t.description,visible:!0})},e.highlight=function(){var n=Object(d.a)(l.a.mark((function n(t){return l.a.wrap((function(n){for(;;)switch(n.prev=n.next){case 0:console.log(t,e.map.getBounds(),e.map.getZoom());case 1:case"end":return n.stop()}}),n)})));return function(e){return n.apply(this,arguments)}}(),e}return Object(h.a)(t,[{key:"componentDidMount",value:function(){var e=this;(function(e){var n="https://www.bing.com/api/maps/mapcontrol?callback=".concat("bingAPIReady","&branch=experimental");return e&&(n+="&key=".concat(e)),new Promise((function(e,t){var i=document.createElement("script");i.type="text/javascript",i.async=!0,i.defer=!0,i.src=n,window.bingAPIReady=function(){a=window.Microsoft,e()},i.onerror=function(e){t(e)},document.body.appendChild(i)}))})("AlhCe8XWn9qAY3ohEYMFdMNBiyKoBvIAW1X8XSiIXaip2kWTWy6jdLma-eCWCVsO").then(Object(d.a)(l.a.mark((function n(){var t;return l.a.wrap((function(n){for(;;)switch(n.prev=n.next){case 0:t=e.initMap(),e.map=t,a.Maps.loadModule("Microsoft.Maps.GeoJson",(function(){a.Maps.Events.addHandler(t,"click",e.highlight),a.Maps.Events.addHandler(t,"viewchangeend",(function(){return e.mapChanged.next(t)})),e.updatePins(),e.infobox=new a.Maps.Infobox(t.getCenter(),{visible:!1}),e.infobox.setMap(t)}));case 3:case"end":return n.stop()}}),n)})))),this.mapChanged.pipe(Object(y.a)(500)).subscribe(this.updatePins)}},{key:"render",value:function(){return Object(M.jsx)("div",{ref:this.mapRef,className:"map"})}},{key:"initMap",value:function(){var e=a.Maps.LocationRect.fromLocations(new a.Maps.Location(6.067439945929365,-10.128615333183788),new a.Maps.Location(-32.86130440585188,-94.50361533318379));return new a.Maps.Map(this.mapRef.current,{mapTypeId:a.Maps.MapTypeId.aerial,minZoom:5,bounds:e,center:new a.Maps.Location(-13.257928544766926,-49.121355290840725)})}}]),t}(i.Component),E=(r.a.semibold,{childrenGap:15}),O=function(){return Object(M.jsx)(c.a,{horizontalAlign:"center",verticalAlign:"center",verticalFill:!0,styles:{root:{width:"100%",margin:"0 auto",textAlign:"center",color:"#605e5c"}},tokens:E,children:Object(M.jsx)(j,{mapOptions:{center:[-11.123341,-64.481926]}})})},x=function(e){e&&e instanceof Function&&t.e(3).then(t.bind(null,101)).then((function(n){var t=n.getCLS,a=n.getFID,i=n.getFCP,o=n.getLCP,s=n.getTTFB;t(e),a(e),i(e),o(e),s(e)}))};Object(r.d)({":global(body,html,#root)":{margin:0,padding:0,height:"100vh"}}),s.a.render(Object(M.jsx)(O,{}),document.getElementById("root")),x()}},[[82,1,2]]]);
//# sourceMappingURL=main.404c0aa1.chunk.js.map