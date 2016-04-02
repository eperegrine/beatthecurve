var page = require('webpage').create();


var fs = require('fs');
var file = fs.read('preload/exams/exams.json');
var data = JSON.parse(file);

var system = require('system');

page.onConsoleMessage = function(msg) {
    if (msg == "__quit__") {
        phantom.exit();
      }
    system.stdout.writeLine(msg);
};

phantom.addCookie({
  'name': 'AWSELB',
  'value': '57739FA112D946239A2969DD58550557F507F5176E022D5E8AB41AEAF990158FCD5CF5D53FD2E934F8F804EC41CDA5AD24EF1F36AFADBD8E5265F21C3BD386C378927A8445',
  'domain': '.koofers.com'
});

phantom.addCookie({
  'name': 'PHPSESSID',
  'value': 'i49v91gs2ail2hnmi36qpt2ii2',
  'domain': '.koofers.com'
});

phantom.addCookie({
  'name': 'UserEmail',
  'value': 'charlie.thomas%40attwoodthomas.net',
  'domain': '.koofers.com'
});


var url = system.args[1];
var pages = system.args[2];

page.open(url, function() {
  page.includeJs("http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js", function() {
    page.evaluate(function(url, pages) {

        var i = 0;

        var x = function () {
            $('span[title="Next Page"]').click();
            var i = $(".img_area img").length;


            if (i < pages) {
                setTimeout(x, 3000);
            } else {
                console.log('All loaded');
                var args = ["download_images.py"];
                $(".img_area img").each(function(i) {
                   console.log("url: " + $(this).attr("src"))
                });
                console.log("done");
                 console.log("__quit__");
            }
        };

        x();


    }, url, pages);
  });
});

