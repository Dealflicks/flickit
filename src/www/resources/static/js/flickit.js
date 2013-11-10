// updated header for grid widgets; scroll grid body for some browsers
// based heavily on https://github.com/pinterest/widgets/blob/master/pinit.js


(function (w, d, a) {
  var $ = w[a.k] = {
    'w': w,
    'd': d,
    'a': a,
    's': {},
    'f': (function () {
      return {
        // an empty array of callbacks to be populated later
        callback: [],

        // get a DOM property or text attribute
        get: function (el, att) {
          var v = null;
          if (typeof el[att] === 'string') {
            v = el[att];
          } else {
            v = el.getAttribute(att);
          }
          return v;
        },

        // get a data: attribute
        getData: function (el, att) {
          att = $.a.dataAttributePrefix + att;
          return $.f.get(el, att);
        },

        // set a DOM property or text attribute
        set: function (el, att, string) {
          if (typeof el[att] === 'string') {
            el[att] = string;
          } else {
            el.setAttribute(att, string);
          }
        },

        // create a DOM element
        make: function (obj) {
          var el = false, tag, att;
          for (tag in obj) {
            if (obj[tag].hasOwnProperty) {
              el = $.d.createElement(tag);
              for (att in obj[tag]) {
                if (obj[tag][att].hasOwnProperty) {
                  if (typeof obj[tag][att] === 'string') {
                    $.f.set(el, att, obj[tag][att]);
                  }
                }
              }
              break;
            }
          }
          return el;
        },

        // remove a DOM element
        kill: function (obj) {
          if (typeof obj === 'string') {
            obj = $.d.getElementById(obj);
          }
          if (obj && obj.parentNode) {
            obj.parentNode.removeChild(obj);
          }
        },

        // replace one DOM element with another
        replace: function (before, after) {
          before.parentNode.insertBefore(after, before);
          $.f.kill(before);
        },

        // find an event's target element
        getEl: function (e) {
          var el = null;
          if (e.target) {
            el = (e.target.nodeType === 3) ? e.target.parentNode : e.target;
          } else {
            el = e.srcElement;
          }
          return el;
        },

        // listen for events in a cross-browser fashion
        listen : function (el, ev, fn) {
          if (typeof $.w.addEventListener !== 'undefined') {
            el.addEventListener(ev, fn, false);
          } else if (typeof $.w.attachEvent !== 'undefined') {
            el.attachEvent('on' + ev, fn);
          }
        },

        call: function (url, func, a_count) {
          var n, id, sep = '?';

          // n = $.f.callback.length;  
          n = a_count;


          id = $.a.k + '.f.callback[' + n + ']';

          $.f.debug(id);
          // create the callback
          $.f.callback[n] = function (r) {
            $.f.debug(r);
            func(r, n);
            $.f.kill(id);
          };

          // some calls may come with a query string already set
          if (url.match(/\?/)) {
            sep = '&';
          }

          // make and call the new script node
          $.d.b.appendChild( $.f.make({'SCRIPT': {
              'id': id,
              'type': 'text/javascript',
              'charset': 'utf-8',
              'src': url + sep + 'callback=' + id
            }
          }));
        },

        // console.log only if debug is on
        debug: function (obj) {
          if ($.v.config.debug && $.w.console && $.w.console.log) {
            $.w.console.log(obj);
          }
        },

        // build stylesheet
        presentation : function () {
          var css, cdn, rules;

          css = $.f.make({'STYLE': {'type': 'text/css'}});

          // suspenders AND belt; if some weird protocol sneaks through, default to http
          cdn = $.a.cdn[$.v.protocol] || $.a.cdn['http:'];

          rules = $.a.rules.join('\n');

          // each rule has our randomly-created key at its root to minimize style collisions
          rules = rules.replace(/\._/g, '.' + a.k + '_');

          // every rule ending in ; also gets !important
          rules = rules.replace(/;/g, '!important;');

          // pick the right content distribution network
          rules = rules.replace(/_cdn/g, cdn);

          // pick the right resolution
          rules = rules.replace(/_rez/g, $.v.resolution);

          // add rules to stylesheet
          if (css.styleSheet) {
            css.styleSheet.cssText = rules;
          } else {
            css.appendChild($.d.createTextNode(rules));
          }

          // add stylesheet to page
          if ($.d.h) {
            $.d.h.appendChild(css);
          } else {
            $.d.b.appendChild(css);
          }
        },

        getPos: function (el) {
          var x = 0, y = 0;
          if (el.offsetParent) {
            do {
              x = x + el.offsetLeft;
              y = y + el.offsetTop;
            } while (el = el.offsetParent);
            return {"left": x, "top": y};
          }
        },

        hideFloatingButton: function () {
          if ($.s.floatingButton) {
            $.s.floatingButton.style.display = 'none';
          }
        },

        getThis: function (widget, id) {
          var href = $.a.endpoint.builder +  widget + '&' + id;
          $.f.log('&type=getThis&href=' + encodeURIComponent(href));
          $.w.open(href, 'flick' + new Date().getTime());
        },

        showFloatingButton: function (img) {
          // size > 80x80 and source is not a data: uri?
          if (img.height > $.a.minImgSize && img.width > $.a.minImgSize && !img.src.match(/^data/)) {
            // do this only once
            if (!$.s.floatingButton) {
              $.s.floatingButton = $.f.make({'A': {'className': $.a.k + '_flickit_button ' + $.a.k + '_flickit_button_floating', 'title': 'Flick it!', 'target': '_blank'}});
              $.f.set($.s.floatingButton, $.a.dataAttributePrefix + 'log', 'button_flickit_floating');
              $.d.b.appendChild($.s.floatingButton);
            }
            // get position, start href
            var p = $.f.getPos(img), href = $.a.endpoint.create;
            // set the button href
            href = href + 'url=' + encodeURIComponent($.d.URL) + '&media=' + encodeURIComponent(img.src) + '&description=' + encodeURIComponent(img.getAttribute('data-flick-description') || img.title || img.alt || $.d.title);
            $.s.floatingButton.href = href;
            // pop new window and hide on click
            $.s.floatingButton.onclick = function () {
              // $.w.open(this.href, 'flick' + new Date().getTime(), $.a.pop);
              // $.f.hideFloatingButton();
              // $.v.hazFloatingButton = false;

              $.f.debug(img.src);
              $.f.createFlickFromImageUrl(img.src);


              // don't open href; we've successfully popped a window
              return false;
            };
            // set height and position
            $.s.floatingButton.style.top = (p.top + $.a.floatingButtonOffsetTop) + 'px';
            $.s.floatingButton.style.left = (p.left + $.a.floatingButtonOffsetLeft) + 'px';
            // show it
            $.s.floatingButton.style.display = 'block';
          }
        },

        // mouse over; only active if we have floaters
        over: function (v) {
          var t, el;
          t = v || $.w.event;
          el = $.f.getEl(t);
          if (el) {
            if (el.tagName === 'IMG' && el.src && !$.f.getData(el, 'no-hover') && !$.f.get(el, 'noflick') && $.v.config.hover) {
              // we are inside an image
              if ($.v.hazFloatingButton === false) {
                // show the floating button
                $.v.hazFloatingButton = true;
                $.f.showFloatingButton(el);
              } else {
                // we have moved from one image to another while the floater was on
                $.f.hideFloatingButton();
                $.f.showFloatingButton(el);
              }
            } else {
              // we are outside an image. Do we need to hide the floater?
              if ($.v.hazFloatingButton === true) {
                // don't hide the floater if we are over it
                if (el !== $.s.floatingButton) {
                  // hide it
                  $.v.hazFloatingButton = false;
                  $.f.hideFloatingButton();
                }
              }
            }
          }
        },

        // a click!
        click: function (v) {
          v = v || $.w.event;
          var el, log;
          el = $.f.getEl(v);
          if (el) {
            // log this click
            log = $.f.getData(el, 'log');
            if (log) {
              $.f.log('&type=' + log + '&href=' + encodeURIComponent(el.href || $.f.getData(el, 'href')));
              // gray out the button
              if (!el.className.match(/hazClick/)) {
                el.className = el.className + ' ' + $.a.k + '_hazClick';
              }
            }
          }
        },

        filter: function (str) {
          var decoded, ret;
          decoded = '';
          ret = '';
          try {
            decoded = decodeURIComponent(str);
          } catch (e) { }
          ret = decoded.replace(/</g, '&lt;');
          ret = ret.replace(/>/g, '&gt;');
          return ret;
        },

        behavior: function () {
          // TODO: add a single event listener to the body for minimal impact
          // $.f.listen($.d.b, 'click', $.f.click);
          if ($.v.config.hover) {
            $.f.listen($.d.b, 'mouseover', $.f.over);
          }
        },

        getFlickCount: function (movie_id, a_count) {
          var query = '?movie_id=' + movie_id + '&ref=' + encodeURIComponent($.v.here) + '&source=' + $.a.countSource;
          $.f.call($.a.endpoint.flick_count + query, $.f.ping.count, a_count);
        },

        createFlick: function (movie_id, a_count) {
          $.f.debug("Create Flick for " + movie_id);
          var query = '?movie_id=' + movie_id + '&ref=' + encodeURIComponent($.v.here) + '&source=' + $.a.countSource;
          $.f.call($.a.endpoint.flick_create + query, $.f.ping.count, a_count);
        },

        createFlickFromImageUrl: function(img_src) {
          $.f.debug("Create Flick for img.src: " + img_src);
          var query = '?imgurl=' + encodeURIComponent(img_src) + '&ref=' + encodeURIComponent($.v.here) + '&source=' + $.a.countSource;
          $.f.call($.a.endpoint.flick_create_image_url + query, $.f.ping.log, $.f.callback.length);


        },

        prettyFlickCount: function (n) {
          if (n > 999) {
            if (n < 1000000) {
              n = parseInt(n / 1000, 10) + 'K+';
            } else {
              if (n < 1000000000) {
                n = parseInt(n / 1000000, 10) + 'M+';
              } else {
                n = '++';
              }
            }
          }
          return n;
        },
        
    
        // add a CSS class to the container if specified
        cssHook: function (parent, container) {
          var cssHook = $.f.getData(parent, 'css-hook');
          if (cssHook) {
            container.className = container.className + ' ' + cssHook;
          }
        },

        // callbacks
        ping: {
          log: function (r, k) {
            // drop logging callbacks on the floor
          },
          count: function (r, k) {

            var container = $.d.getElementById($.a.k + '_flick_count_' + k);
            if (container) {
              $.f.debug('API replied with count: ' + r.count);
              var parent = container.parentNode;
              var config = $.f.getData(parent, 'config');

              if (r.count === 0) {
                if (config === 'above') {
                  $.f.debug('Rendering zero count above.');
                  container.className = $.a.k + '_flickit_button_count';
                  container.appendChild($.d.createTextNode('0'));
                } else {
                  $.f.debug('Zero flick count not rendered to the side.');
                }
              }

              if (r.count > 0) {
                $.f.debug('Got ' + r.count + ' flicks for the requested URL.');
                if (config === 'above' || config === 'beside') {
                  $.f.debug('Rendering flick count ' + config);
                  container.className = $.a.k + '_flickit_button_count';

                  if (container.childNodes.length > 1){
                    //TODO: remove all but first
                    container.removeChild(container.lastChild);
                  }

                  container.appendChild($.d.createTextNode($.f.prettyFlickCount(r.count)));
                } else {
                  $.f.debug('No valid flick count position specified; not rendering.');
                }
              }

              if (r.has_flicked === true){
                $.f.debug('User has flicked');

                if (!container.className.match(/hazClick/)) {
                  container.className = container.className + ' ' + $.a.k + '_hazClick';
                }

                if (!parent.className.match(/hazClick/)) {
                  parent.className = parent.className + ' ' + $.a.k + '_hazClick';
                }


                // do nothing if user has already flicked, but prevent href from linking thorugh, for now...
                parent.onclick = function () {
                  return false;
                }

              } else {

                // allow current user to flick

                parent.onclick = function () {
                  // make api request to add to the current user's flick it list
                  // oncallback, refresh count

                  $.f.createFlick(r.movie_id, k);

                  return false;
                }
              }



              $.f.cssHook(parent, container);
            } else {
              $.f.debug('Flickit button container not found.');
            }
          },

        
        },

        // parse an URL, return values for specified keys
        parse: function (str, keys) {
          var query, pair, part, i, n, ret;
          ret = {};
          // remove url hash, split to find query
          query = str.split('#')[0].split('?');
          // found query?
          if (query[1]) {
            // split to pairs
            pair = query[1].split('&');
            // loop through pairs
            for (i = 0, n = pair.length; i < n; i = i + 1){
              // split on equals
              part = pair[i].split('=');
              // found exactly two parts?
              if (part.length === 2) {
                // first part is key; do we have a match in keys?
                if (keys[part[0]]) {
                  // yes: set return value for key to second part, which is value
                  ret[part[0]] = part[1];
                }
              }
            }
          }
          return ret;
        },

        // encode and prepend http: and/or // to URLs
        fixUrl: function (str) {
          // see if this string has been url-encoded
          var decoded = '';
          // try-catch because decodeURIComponent throws errors
          try {
            decoded = decodeURIComponent(str);
          } catch (e) { }
          // encode string if decoded matches original
          if (decoded === str) {
            str = encodeURIComponent(str);
          }
          // does it start with http?
          if (!str.match(/^http/i)) {
            // does it start with //
            if (!str.match(/^%2F%2F/i)) {
              str = '%2F%2F' + str;
            }
            str = 'http%3A' + str;
            $.f.debug('fixed URL: ' + str);
          }
          return str;
        },

        // deep link to flickit apps
        deepLink: {
          ios_safari: function (a) {
            var shallow, deep, start, count, amount, delay, watchForError;

            // link target points to flick/create/button/?url=foo&media=bar
            shallow = a.href;

            // make the deep-link URL
            deep = shallow.split('?')[1];
            deep = deep.replace(/url=/, 'source_url=');
            deep = deep.replace(/media=/, 'image_url=');
            deep = 'flickit://flickit/?' + deep;

            // start the clock ticking
            start = new Date().getTime();
            count = 0;
            amount = 10;
            delay = 80;

            // watch for the clock to fall out of sync, meaning Safari can't find the app
            watchForError = function () {
              $.w.setTimeout(function () {
                if (count < amount) {
                  // keep watching
                  watchForError();
                } else {
                  // is our clock out of sync?
                  var since = start + (count * delay);
                  var now = new Date().getTime();
                  var diff = (now - since) / amount;
                  // yes: Safari has tried to pop the app but failed
                  if (diff < delay) {
                    // send us over to flick/create/button (dismisses error pop-up)
                    $.w.location = shallow;
                  }
                }
                count = count + 1;
              }, delay);
            };

            // attempt to pop the flickit application
            $.w.location = deep;

            // if we're still here, start watching the clock
            watchForError();
          }
        },

        render: {
          buttonFlickit: function (el, a_count) {
            $.f.debug('build Flickit button');

            // get just the url, media, and description parameters and percent-encode them, if needed
            var href, q = {};
            q = $.f.parse(el.href, {'movie_id': true});
         
            // if (q.media) {
            //   q.media = $.f.fixUrl(q.media);
            // } else {
            //   // misconfigured: no media URL was given
            //   q.media = '';
            //   $.f.debug('no media found; click will pop bookmark');
            // }


            // if (q.url) {
            //   q.url = $.f.fixUrl(q.url);
            // } else {
            //   // misconfigured: no page URL was given
            //   q.url = encodeURIComponent($.d.URL);
            //   $.f.debug('no url found; click will flick this page');
            // }

            // automatically fill in document.title (if avaiable) for blank descriptions
            // if (!q.description) {
            //   q.description = encodeURIComponent($.d.title || '');
            // }

            href = $.a.endpoint.create + 'url=' + q.url + '&guid=' + $.v.guid + '-' + $.v.buttonId;
            $.v.buttonId = $.v.buttonId + 1;


            var a = $.f.make({'A': {'href': href, 'className': $.a.k + '_flickit_button ' + $.a.k + '_flickit_button_inline', 'target': '_blank'}});
            $.f.set(a, $.a.dataAttributePrefix + 'log', 'button_flickit');

            var config = $.f.getData(el, 'config');
            if ($.a.config.flickitCountPosition[config] === true) {
              $.f.set(a, $.a.dataAttributePrefix + 'config', config);
              a.className = a.className + ' ' + $.a.k + '_flickit_' + config;
            } else {
              a.className = a.className + ' ' + $.a.k + '_flickit_none';
            }

            // validate and log on click
            // a.onclick = function () {
            //   // search for url and media in this button's href
            //   var q = $.f.parse(this.href, {'url': true, 'media': true, 'description': true});
            //   // log if no default description was specified
            //   if (!q.description) {
            //     $.f.log('&type=config_warning&warning_msg=no_description&href=' + encodeURIComponent($.d.URL));
            //   }
            //   // found valid URLs?
            //   if (q.url && q.url.match(/^http/i) && q.media && q.media.match(/^http/i)) {
            //     // yes
            //     if (!$.v.config.shallow && typeof $.f.deepLink[$.v.deepBrowser] === 'function') {
            //       // attempt to deep link
            //       $.f.deepLink[$.v.deepBrowser](this);
            //     } else {
            //       // pop the flick form
            //       $.w.open(this.href, 'flick' + new Date().getTime(), $.a.pop);
            //     }
            //   } else {
            //     // log an error with descriptive message
            //     $.f.log('&type=config_error&error_msg=invalid_url&href=' + encodeURIComponent($.d.URL));
            //     // fire up the bookmarklet and hope for the best
            //     $.f.fireBookmark();
            //   }
            //   return false;
            // };


     

            

            // why use $.f.callback.length for id?
            
            // var span = $.f.make({'SPAN': {'className': $.a.k + '_hidden', 'id': $.a.k + '_flick_count_' + $.f.callback.length, 'innerHTML': '<i></i>'}});
            var span = $.f.make({'SPAN': {'className': $.a.k + '_hidden', 'id': $.a.k + '_flick_count_' + a_count, 'innerHTML': '<i></i>'}});

            a.appendChild(span);
            $.f.getFlickCount(q.movie_id, a_count);
            $.f.replace(el, a);



           
          }
        },

        getFlicksIn: function (endpoint, path, params) {
          var query = '', sep = '?', p;
          for (p in params) {
            if (params[p].hasOwnProperty) {
              query = query + sep + p + '=' + params[p];
              sep = '&';
            }
          }
          $.f.call($.a.endpoint[endpoint] + path + query, $.f.ping[endpoint]);
        },

        build: function (el) {
          $.f.debug('build');

          var a_count = 0;


          // look for buildable pidgets in element el
          // may be fired by function specified in data-flick-render
          if (typeof el !== 'object' ||  el === null || !el.parentNode) {
            el = $.d;
          }
          // grab all the links on the page
          var temp = el.getElementsByTagName('A'), n, i, doThis, legacyLayout, legacyConfig, legacyTranslate = {'vertical': 'above', 'horizontal': 'beside'}, link = [];
          for (i = 0, n = temp.length; i < n; i = i + 1) {
            link.push(temp[i]);
          }


          // go through all links and look for ours
          for (i = 0, n = link.length; i < n; i = i + 1) {
            if (link[i].href && link[i].href.match($.a.myDomain)) {

              doThis = $.f.getData(link[i], 'do');

              if (typeof $.f.render[doThis] === 'function') {
                // link[i].id = $.a.k + '_' + $.f.callback.length;
                link[i].id = $.a.k + '_' + a_count;
                $.f.render[doThis](link[i], a_count);
                a_count = a_count + 1;
              }
            }
          }
        },

        config: function () {
          // find and apply configuration requests passed as data attributes on SCRIPT tag
          var script = $.d.getElementsByTagName('SCRIPT'), n = script.length, i, j, foundMe = false;

          for (i = 0; i < n; i = i + 1) {
            if ($.a.me && script[i] && script[i].src && script[i].src.match($.a.me)) {
              // only do this for the first instance of the script on the page
              if (foundMe === false) {
                for (j = 0; j < $.a.configParam.length; j = j + 1) {
                  $.v.config[$.a.configParam[j]] = $.f.get(script[i], $.a.dataAttributePrefix + $.a.configParam[j]);
                }
                foundMe = true;
              }
              $.f.kill(script[i]);
            }
          }

          if (typeof $.v.config.build === 'string') {
            $.w[$.v.config.build] = function (el) {
              $.f.build(el);
            };
          }


          // override domains if performing local development
          if (typeof $.v.config.dev === 'string') {
            if ( $.v.config.dev === 'local'){
              $.a.myDomain = /^https?:\/\/(www\.|)justflickit\.dev\//;
              $.a.endpoint = {
                'flick_count': '//www.justflickit.dev/api/v1/flicks/count.json',
                'flick_create': '//www.justflickit.dev/api/v1/flicks/create.json',
                'flick_create_image_url': '//www.justflickit.dev/api/v1/flicks/create-from-imgurl.json'
              };
              $.a.cdn = {
                'https:': 'https://www.justflickit.dev',
                'http:': 'http://www.justflickit.dev',
                // if we are dragging and dropping to test a page, use http instead of file
                'file:': 'http://www.justflickit.dev'
              };
            }

          }


          // }

          $.w.setTimeout(function () {
            if (typeof $.v.config.logc === 'string') {
              $.f.log('&type=pidget&logc=' + $.v.config.logc, $.a.endpoint.logc);
            } else {
              $.f.log('&type=pidget');
            }
          }, 1000);

        },
        // send logging information
        log: function (str, endpoint) {

            // if (!endpoint) {
            //   endpoint = $.a.endpoint.log;
            // }

            // // create the logging call
            // var query = '?via=' + encodeURIComponent($.v.here) + '&guid=' + $.v.guid;

            // // add the optional string to log
            // if (str) {
            //   query = query + str;
            // }

            // $.f.call(endpoint + query, $.f.ping.log);
        },

        init : function () {

          $.d.b = $.d.getElementsByTagName('BODY')[0];
          $.d.h = $.d.getElementsByTagName('HEAD')[0];

          // just a few variables that need to be shared throughout this script
          $.v = {
            'resolution': 1,
            'here': $.d.URL.split('#')[0],
            'hazFloatingButton': false,
            'config': {},
            'strings': $.a.strings.en,
            'guid': '',
            'buttonId': 0,
            'deepBrowser': null,
            'protocol': $.w.location.protocol,
            'userAgent': $.w.navigator.userAgent
          };

          // are we testing by dragging a file into a browser?
          if ($.v.protocol === 'file:') {
            $.v.protocol = 'http:';
          }

          // prepend protocol to endpoints so testing from file:// works
          for (var e in $.a.endpoint) {
            // one endpoint already takes http:, so don't override
            if (!$.a.endpoint[e].match(/^h/)) {
              $.a.endpoint[e] = $.v.protocol + $.a.endpoint[e];
            }
          }

          // are we using an IOS device?
          if ($.v.userAgent.match(/iP/) !== null) {
            // we're on an IOS device. Don't deep link from inside the flickit app or Chrome.
            if ($.v.userAgent.match(/flickit/) === null && $.v.userAgent.match(/CriOS/) === null) {
              $.v.deepBrowser = 'ios_safari';
            }
          }

          // make a 12-digit base-60 number for conversion tracking
          for (var i = 0; i < 12; i = i + 1) {
            $.v.guid = $.v.guid + '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ_abcdefghijkmnopqrstuvwxyz'.substr(Math.floor(Math.random() * 60), 1);
          }

          // do we need to switch languages from en to something else?
          var lang = $.d.getElementsByTagName('HTML')[0].getAttribute('lang');
          if (lang) {
            lang = lang.toLowerCase();
            // direct match for pt-br
            if (typeof $.a.strings[lang] === 'object') {
              $.v.strings = $.a.strings[lang];
            } else {
              // match first part: en-uk = en
              lang = lang.split('-')[0];
              if (typeof $.a.strings[lang] === 'object') {
                $.v.strings = $.a.strings[lang];
              }
            }
          }

          if ($.w.devicePixelRatio && $.w.devicePixelRatio >= 2) {
            $.v.resolution = 2;
          }

          // find the script node we are running now
          // remove it and set config options if we find any
          $.f.config();

          // note: build can also be triggered by a user-specified request passed in data-flick-build
          $.f.build();

          $.f.presentation();
          $.f.behavior();



        }
      };
    }())
  };
  $.f.init();
}(window, document, {
  'k': 'FLICKIT_' + new Date().getTime(),
  'myDomain': /^https?:\/\/(www\.|)justflickit\.com\//,
  'me': /flickit.*?\.js$/,
  'floatingButtonOffsetTop': 10,
  'floatingButtonOffsetLeft': 10,
  'endpoint': {
    'flick_count': '//www.justflickit.com/api/v1/flicks/count.json',
    'flick_create': '//www.justflickit.com/api/v1/flicks/create.json'
  },
  'config': {
    'flickitCountPosition': {
      'none': true,
      'above': true,
      'beside': true
    }
  },
  'minImgSize': 80,
  // source 6 means "flicked with the externally-hosted Flickit button"
  'countSource': 6,
  'dataAttributePrefix': 'data-flickit-',
  // valid config parameters
  'configParam': [ 'build', 'debug', 'style', 'hover', 'logc', 'shallow', 'dev'],
  // configuration for the pop-up window
  'pop': 'status=no,resizable=yes,scrollbars=yes,personalbar=no,directories=no,location=no,toolbar=no,menubar=no,width=632,height=270,left=0,top=0',
  'popLarge': 'status=no,resizable=yes,scrollbars=yes,personalbar=no,directories=no,location=no,toolbar=no,menubar=no,width=900,height=500,left=0,top=0',
  // secure and non-secure content distribution networks
  'cdn': {
    'https:': 'https://www.justflickit.com',
    'http:': 'http://www.justflickit.com',
    // if we are dragging and dropping to test a page, use http instead of file
    'file:': 'http://www.justflickit.com'
  },
  // tiled image settings
  'tile': {
    'scale': {
      'minWidth': 60,
      'minHeight': 60,
      'width': 92,
      'height': 175
    },
    'minWidthToShowAuxText': 150,
    'minContentWidth': 120,
    'minColumns': 1,
    'maxColumns': 6,
    'style': {
      'margin': 2,
      'padding': 10
    }
  },
  'strings': {
    'en': {
      'seeOn': 'See On',
      'getThis': 'get this',
      'attribTo': 'by',
      'flickedBy': 'Flicked by',
      'onto': 'Onto'
    }
  },
  // CSS rules
  'rules': [

    // FLICK IT BUTTON

    'a._flickit_button {  background-image: url(_cdn/static/img/flickit-button-sprite.png); background-repeat: none; background-size: 67px 60px; height: 20px; margin: 0; padding: 0; vertical-align: baseline; text-decoration: none; width: 67px; background-position: 0 0px }',
    'a._flickit_button:hover, span._flickit_button_count:hover { background-position: 0 -20px }',
    'a._flickit_button:active, a._flickit_button._hazClick, span._flickit_button_count:active, span._flickit_button_count._hazClick { background-position: 0 -39px !important}',
    'a._flickit_button_inline { position: relative; display: inline-block; }',
    'a._flickit_button_floating { position: absolute; }',

    // the count
    'a._flickit_button span._flickit_button_count { position: absolute; color: #FFF; text-align: center; text-indent: 0; }',
    // 'a._flickit_above span._flickit_button_count { background: transparent url(_cdn/static/img/flickit-count-above-sprite.png) 0 0 no-repeat; background-size: 40px 29px; position: absolute; bottom: 21px; left: 0px; height: 29px; width: 40px; font: 12px Arial, Helvetica, sans-serif; line-height: 24px; text-indent: 0;}',

    // flick count background
    'a._flickit_beside span._flickit_button_count, a._flickit_beside span._flickit_button_count i {  background-repeat: none; background-size: 43px 60px; background-color: transparent; background-image: url(_cdn/static/img/flickit-count-sprite.png); background-size: 43px 60px; width: 43px; height: 20px; background-position: 0 0px}',

    // flick count flag left side with number
    'a._flickit_beside span._flickit_button_count { padding: 1px 0px 0px 2px; position: absolute; top: 0; left: 66px; height: 20px; font: 10px Arial, Helvetica, sans-serif; line-height: 20px; }',

    // flick count flag right cap
    'a._flickit_beside span._flickit_button_count i { background-position: 100% 0; position: absolute; top: 0; right: -2px; height: 20px; width: 2px; }',
    // 'a._flickit_button._flickit_above { margin-top: 20px; }',

       
    // leave this at the bottom, to avoid trailing commas
    '._hidden { display:none; }'
  ]
}));