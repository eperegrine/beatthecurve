var page = require('webpage').create();


var fs = require('fs');
var file = fs.read('./exams.json');
var data = JSON.parse(file);

var system = require('system');

page.onConsoleMessage = function(msg) {
    system.stdout.writeLine(msg);
};

phantom.addCookie({
  'name': 'AWSELB',
  'value': '57739FA112D946239A2969DD58550557F507F5176E022D5E8AB41AEAF990158FCD5CF5D53FD2E934F8F804EC41CDA5AD24EF1F36AFADBD8E5265F21C3BD386C378927A8445',
  'domain': '.koofers.com'
});

phantom.addCookie({
  'name': 'PHPSESSID',
  'value': '6sn9u5iq7o0q6earp7qgtvg4u4',
  'domain': '.koofers.com'
});

phantom.addCookie({
  'name': 'UserEmail',
  'value': 'charlie.thomas%40attwoodthomas.net',
  'domain': '.koofers.com'
});



for (var x=0; x < data['exams'].length; x++) {
    var object = data['exams'][x];

    page.open('https://koofers.com/files/exam-' + object['exam-code'], function() {
      page.includeJs("http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js", function() {
        page.evaluate(function(object) {

            var i = 0;

            var x = function () {
                $('span[title="Next Page"]').click();
                var i = $(".img_area img").length;


                if (i < object['pages']) {
                    setTimeout(x, 3000);
                } else {
                    console.log('All loadded');
                    var args = ["download_images.py"];
                    $(".img_area img").each(function(i) {
                       console.log("url: " + $(this).attr("src"))
                    });
                }
            };

            return x(object);


        }, object);

      });
    });

    break
}
