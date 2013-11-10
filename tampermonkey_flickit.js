// ==UserScript==
// @name       Flickit
// @namespace  http://justflickit.com/
// @version    0.1
// @description  enter something useful
// @match      http://*/*
// @copyright  2013+, Flickit
// ==/UserScript==


(function(d){
  var f = d.getElementsByTagName('SCRIPT')[0], p = d.createElement('SCRIPT');
  p.type = 'text/javascript';
  p.setAttribute('data-flickit-hover', true);
  p.async = true;
  p.src = '//www.justflickit.com/static/js/flickit.js';
  f.parentNode.insertBefore(p, f);
}(document));