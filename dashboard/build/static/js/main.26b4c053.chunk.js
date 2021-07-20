(this.webpackJsonpdashboard=this.webpackJsonpdashboard||[]).push([[0],{119:function(e,t,n){},145:function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a),c=n(42),o=n.n(c),s=(n(119),n(3)),i=n(166),l=n(162),u=n(163),d=n(169),j=n(171),b=n(167),m=n(106),f=n(13);var h=function(e){var t=e.children,n=e.el,r=Object(a.useState)(!1),c=Object(s.a)(r,2)[1];return Object(a.useEffect)((function(){setTimeout((function(){c(!0)}),100)}),[]),document.getElementById(n)?o.a.createPortal(t,document.getElementById(n)):null},x=n(2);var O=function(){var e=Object(f.f)().pathname;return Object(x.jsxs)(l.a,{justify:"center",direction:"column",alignItems:"center",children:[Object(x.jsx)(u.a,{fontWeight:"bold",fontSize:"lg",children:"404"}),"Page not found ",e]})},p=n.p+"static/media/logo.b2e5a01e.svg",v=n(52),g=v.c,w=n(15),S=n.n(w),_=n(30),y=n(53);function C(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1;return new Promise((function(t){return setTimeout((function(){return t({data:e})}),500)}))}var k=Object(y.b)("counter/fetchCount",function(){var e=Object(_.a)(S.a.mark((function e(t){var n;return S.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,C(t);case 2:return n=e.sent,e.abrupt("return",n.data);case 4:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}()),A=Object(y.c)({name:"counter",initialState:{value:0,status:"idle"},reducers:{increment:function(e){e.value+=1},decrement:function(e){e.value-=1},incrementByAmount:function(e,t){e.value+=t.payload}},extraReducers:function(e){e.addCase(k.pending,(function(e){e.status="loading"})).addCase(k.fulfilled,(function(e,t){e.status="idle",e.value+=t.payload}))}}),N=A.actions,E=N.increment,I=N.decrement,B=N.incrementByAmount,L=function(e){return e.counter.value},U=A.reducer,R=n(33),z=n.n(R);function D(){var e=g(L),t=Object(v.b)(),n=Object(a.useState)("2"),r=Object(s.a)(n,2),c=r[0],o=r[1],i=Number(c)||0;return Object(x.jsxs)("div",{children:[Object(x.jsxs)("div",{className:z.a.row,children:[Object(x.jsx)("button",{className:z.a.button,"aria-label":"Decrement value",onClick:function(){return t(I())},children:"-"}),Object(x.jsx)("span",{className:z.a.value,children:e}),Object(x.jsx)("button",{className:z.a.button,"aria-label":"Increment value",onClick:function(){return t(E())},children:"+"})]}),Object(x.jsxs)("div",{className:z.a.row,children:[Object(x.jsx)("input",{className:z.a.textbox,"aria-label":"Set increment amount",value:c,onChange:function(e){return o(e.target.value)}}),Object(x.jsx)("button",{className:z.a.button,onClick:function(){return t(B(i))},children:"Add Amount"}),Object(x.jsx)("button",{className:z.a.asyncButton,onClick:function(){return t(k(i))},children:"Add Async"}),Object(x.jsx)("button",{className:z.a.button,onClick:function(){return t((e=i,function(t,n){L(n())%2===1&&t(B(e))}));var e},children:"Add If Odd"})]})]})}var T=function(){return Object(x.jsx)("div",{className:"App",children:Object(x.jsxs)("header",{className:"App-header",children:[Object(x.jsx)("img",{src:p,className:"App-logo",alt:"logo"}),Object(x.jsx)(D,{}),Object(x.jsxs)("p",{children:["Edit ",Object(x.jsx)("code",{children:"src/App.tsx"})," and save to reload."]}),Object(x.jsxs)("span",{children:[Object(x.jsx)("span",{children:"Learn "}),Object(x.jsx)("a",{className:"App-link",href:"https://reactjs.org/",target:"_blank",rel:"noopener noreferrer",children:"React"}),Object(x.jsx)("span",{children:", "}),Object(x.jsx)("a",{className:"App-link",href:"https://redux.js.org/",target:"_blank",rel:"noopener noreferrer",children:"Redux"}),Object(x.jsx)("span",{children:", "}),Object(x.jsx)("a",{className:"App-link",href:"https://redux-toolkit.js.org/",target:"_blank",rel:"noopener noreferrer",children:"Redux Toolkit"}),",",Object(x.jsx)("span",{children:" and "}),Object(x.jsx)("a",{className:"App-link",href:"https://react-redux.js.org/",target:"_blank",rel:"noopener noreferrer",children:"React Redux"})]})]})})},q=n(164),W=n(174),P=n(173),V=n(63);var J=function(){var e=Object(V.a)(),t=e.register,n=e.handleSubmit,a=e.errors;return Object(x.jsx)(q.a,{children:Object(x.jsxs)("form",{onSubmit:n((function(e){console.log("onSubmit",e)})),children:[Object(x.jsx)(P.a,{name:"username",ref:t({required:!0})}),Object(x.jsx)(P.a,{name:"password",ref:t({required:!0}),type:"password"}),Object(x.jsxs)(q.a,{m:"1",children:[a.username&&Object(x.jsx)(u.a,{fontSize:"xs",textAlign:"start",color:"tomato",children:"username is required!"}),a.password&&Object(x.jsx)(u.a,{fontSize:"xs",textAlign:"start",color:"tomato",children:"password is required!"})]}),Object(x.jsx)(W.a,{type:"submit",children:"Login"})]})})};var K=function(){return Object(x.jsx)(l.a,{display:"grid",h:"full",placeItems:"center",children:Object(x.jsx)(q.a,{w:"3xl",children:Object(x.jsx)(J,{})})})},Y=n(170),F=n(101),H=n.n(F);var M=function(e){var t=e.columns,n=e.data;return Object(x.jsx)(H.a,{noTableHead:!0,columns:t,data:n})},X=[{name:"ChainID",selector:"chainid",sortable:!0},{name:"Name",selector:"name",sortable:!0},{name:"AgencyId",selector:"agencyid",sortable:!0,right:!0}],$=n(104),G=n.n($);var Q=function(){var e=Object(V.a)(),t=e.register,n=e.handleSubmit,r=Object(a.useState)(!1),c=Object(s.a)(r,2),o=c[0],i=c[1],d=Object(a.useState)([{name:"Chain",column:X,data:[]},{name:"Area",column:X,data:[]},{name:"Agency",column:X,data:[]},{name:"Stores",column:X,data:[]},{name:"Users",column:X,data:[]},{name:"Users Schedules",column:X,data:[]},{name:"SKUs",column:X,data:[]},{name:"Category",column:X,data:[]},{name:"Category Reference",column:X,data:[]},{name:"Stores SKUs",column:X,data:[]}]),j=Object(s.a)(d,1)[0],b=Object(a.useState)(j[0]),m=Object(s.a)(b,2),f=m[0],h=m[1],O=function(e,t){var n=e.replace("file_","")+".xlsx";console.log("uploadValue > ",e),i(!0);var a=new FormData;a.append("file",t,n);var r="/api/upload/template/"+e.replace("file_","");console.log("url",r),G.a.post(r,a).then((function(e){i(!1),console.log("response",e)})).catch((function(e){i(!1),console.log("err",e)}))};return Object(x.jsx)(q.a,{m:"3",children:Object(x.jsx)("form",{onSubmit:n((function(e){var t="file_"+f.name.toLowerCase().replaceAll(" ","_");console.log("onSubmit > form",e),console.log("onSubmit > form",e[t][0]),O(t,e[t][0])})),children:Object(x.jsxs)(Y.e,{children:[Object(x.jsx)(Y.b,{children:j.map((function(e,t){return Object(x.jsx)(Y.a,{onClick:function(t){h(e),t.preventDefault()},fontSize:"sm",children:e.name.toUpperCase()},t)}))}),Object(x.jsx)(Y.d,{children:j.map((function(e,n){return Object(x.jsxs)(Y.c,{children:[Object(x.jsx)(u.a,{fontWeight:"bold",my:"3",children:e.name.toUpperCase()}),Object(x.jsxs)(l.a,{alignItems:"center",children:[Object(x.jsx)(P.a,{accept:".xlsx, .xls",name:"file_"+e.name.toLowerCase().replaceAll(" ","_"),ref:t,type:"file"}),Object(x.jsx)(W.a,{isLoading:o,type:"submit",children:"Upload"})]}),Object(x.jsx)(M,{columns:e.column,data:e.data})]},n+""+e)}))})]})})})};var Z=function(){var e=Object(i.a)(),t=e.isOpen,n=e.onOpen,r=e.onClose,c=Object(a.useState)(null),o=Object(s.a)(c,2),p=o[0],v=o[1],g=new j.a;return Object(a.useEffect)((function(){var e=window.addEventListener("online",(function(){r(),n(),v("online"),setTimeout((function(){r()}),4e3)})),t=window.addEventListener("offline",(function(){n(),v("offline")}));return function(){window.removeEventListener("online",e),window.removeEventListener("offline",t)}})),Object(x.jsxs)(b.a,{client:g,children:[Object(x.jsx)(h,{el:"networkstatus",children:Object(x.jsx)(d.a,{in:t,animateOpacity:!0,children:"online"===p?Object(x.jsx)(l.a,{align:"center",justify:"center",bg:"#0dc445",w:"100%",children:Object(x.jsx)(u.a,{color:"white",fontSize:"sm",p:"1",children:"Your network is restored"})}):Object(x.jsx)(l.a,{align:"center",justify:"center",bg:"#f51b1b",w:"100%",children:Object(x.jsx)(u.a,{color:"white",fontSize:"sm",p:"1",children:"You're on offline mode"})})})}),Object(x.jsx)(m.a,{children:Object(x.jsxs)(f.c,{children:[Object(x.jsx)(f.a,{exact:!0,path:"/:username/templates",component:Q}),Object(x.jsx)(f.a,{exact:!0,path:"/login",component:K}),Object(x.jsx)(f.a,{exact:!0,path:"/",component:T}),Object(x.jsx)(f.a,{component:O})]})})]})},ee=Object(y.a)({reducer:{counter:U}});Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));var te=n(168),ne=n(172),ae=Object(te.a)({colors:{brand:{900:"#1a365d",800:"#153e75",700:"#2a69ac"}}});o.a.render(Object(x.jsx)(r.a.StrictMode,{children:Object(x.jsx)(v.a,{store:ee,children:Object(x.jsxs)(ne.a,{theme:ae,children:[Object(x.jsx)(q.a,{w:"100%",id:"networkstatus"}),Object(x.jsx)(Z,{})]})})}),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))},33:function(e,t,n){e.exports={row:"Counter_row__1C_4f",value:"Counter_value__1d0te",button:"Counter_button__1xpSV",textbox:"Counter_textbox__3ODaX",asyncButton:"Counter_asyncButton__2UAr3 Counter_button__1xpSV"}}},[[145,1,2]]]);
//# sourceMappingURL=main.26b4c053.chunk.js.map