/**
 * Created by Giang on 2017-11-03.
 */

$(document).ready(function() {
    $("input[name='modes']").change(function(e){
        $("#custom-option").toggle($(this).val() == 3);
    });
});
