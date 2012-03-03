

$(document).ready(function() {
    $('#getdata-button').click(function() {
        $.getJSON('resource.js', function(data) {
            var mydata = "";
            for (value in data) {
                mydata = mydata + "<p>"+data[value].name+"</p>";
            }
            $('#showdata').html(mydata);
//            timedCount();
        });
    });
});

var tt=0;

function timedCount() {
    $('#showdata').html(tt++);
    setTimeout("timedCount()", 1000);
}
