$(document).ready(function() {
    console.log("Hello");
    start_time_lock("submit_btn"); 
	
    console.log("hahahahahahahahaha");
    console.log(window.location.href);
    console.log(gup("assignmentId"));
    console.log($(form_selector));
    console.log("hahahahahahahahaha"); 

    if((aid = gup("assignmentId"))!="" && $(form_selector).length>0) {
        // If the HIT hasn't been accepted yet, disabled the form fields.
        if(aid == "ASSIGNMENT_ID_NOT_AVAILABLE") {
            $('input,textarea,select').attr("DISABLED", "disabled");
        }

        // Add a new hidden input element with name="assignment_id" that
        // with assignment_id as its value.
        // var aid_input = $("<input type='hidden' name='assignment_id' value='" + aid + "'>").appendTo($(form_selector));
        $("#mturk_assignment_id").val(aid);

        // Make sure the submit form's method is POST
        $(form_selector).attr('method', 'POST');

        // Set the Action of the form to the provided "turkSubmitTo" field
        if((submit_url=gup("turkSubmitTo"))!="") {
            $(form_selector).attr('action', submit_url + '/mturk/externalSubmit');
        }
    }
});

var start_time_lock = function(element_id) {
    var element = $("#"+element_id);
    var ori_text = element.val();
    var time = parseInt(element.attr("time-lock"));
    setInterval(function() {
        if (time > 0) {
            element.val(ori_text+" ("+time+")");
            time -= 1;
        } else {
            element.val(ori_text);
            element.attr("disabled", false);
        }
    }, 1000);
}

var warning = function(w) {
    if (arguments.length) {
        console.log(w);
        $("#warning").text(w);
        if (w == "") {
            $(".answer_table").removeClass("warning");
        } else {
            $(".answer_table").addClass("warning");
        }
    } else {
        return $("#warning").text();
    }
    return false;
}

// selector used by jquery to identify your form
var form_selector = "#mturk_form";

// function for getting URL parameters
function gup(name) {
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.href);
    if(results == null)
        return "";
    else return unescape(results[1]);
}

function validateForm() {
    warning("");
    var q1 = $('input[name="q1"]:checked').val();
    console.log(q1);
    console.log($(form_selector).attr('action'));
    if (q1 == null || q1 == undefined) {
        warning("Please select an answer.");
        return false;
    }
    return true;
}
