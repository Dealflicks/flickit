Version
=======

0.0.1



flickit
=======

Never forget the movie you want to see. Just flick it.



Notes
======

mkvirtualenv flickit
cd /flickit/src/www
pip install -r requirements.txt


sudo nginx -c /Users/zcancio/Development/flickit/flickit/nginx.conf



Async load, debug, hover:

(function(d){
  var f = d.getElementsByTagName('SCRIPT')[0], p = d.createElement('SCRIPT');
  p.type = 'text/javascript';
  p.setAttribute('data-flickit-debug', true);
  p.setAttribute('data-flickit-dev', 'local');
  p.setAttribute('data-flickit-hover', true);
  p.async = true;
  p.src = '//www.justflickit.dev/static/js/flickit.js';
  f.parentNode.insertBefore(p, f);
}(document));


