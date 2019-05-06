$(document).ready(function() {

    var update_num = function(panel_id) {
        console.log("#"+panel_id+" .selected");
        var length = $("#"+panel_id+" .selected").length;
        $("#"+panel_id+" .num").text( "( "+length+" )" );
    };

    $(document).on("click", ".not_selected", function(evt) {
        var target;
        if (!$(evt.target).hasClass("sentence")) {
            target = $(evt.target).parents(".sentence");
        } else {
            target = $(evt.target);
        }

        target.removeClass("not_selected").addClass("selected");
        update_num(target.parents(".sentence_panel").attr("id"));
    });
    $(document).on("click", ".selected", function(evt) {
        var target;
        if (!$(evt.target).hasClass("sentence")) {
            target = $(evt.target).parents(".sentence");
        } else {
            target = $(evt.target);
        }
        target.removeClass("selected").addClass("not_selected");
        update_num(target.parents(".sentence_panel").attr("id"));
    });

    $(document).on("click", "#submit_btn", function(evt) {
        $("#warning").text("");

        // check number of "selected" answers
        var w1_answers = $("#sentence_panel_1 .selected");
        var w2_answers = $("#sentence_panel_2 .selected");

        if (w1_answers.length < 5 || w2_answers.length < 5) {
            $("#warning").text("Please select at least 5 sentences.");
            return false;
        }

        var answer = {
            "w1": $.map(w1_answers, function(e, index) {return $(e).attr("id")}),
            "w2": $.map(w2_answers, function(e, index) {return $(e).attr("id")}),
        };

        $("#answer").val(JSON.stringify(answer));

        $("#mturk_form").submit();
    });
});

var temp;