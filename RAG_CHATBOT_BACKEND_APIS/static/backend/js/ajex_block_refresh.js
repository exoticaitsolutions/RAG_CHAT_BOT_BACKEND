if (document.getElementById("div_for_refresh")) {
    $(document).ready(function(){
    setInterval(function(){
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var chat_id = document.getElementById("chat_id").value;
        var user_id = document.getElementById("user_id").value;

        $.ajax({
            type: "GET",
            url : "/refresh_div/",
            headers:{
                'X-CSRFToken' : csrftoken
            },
            data: {'chat_id' : chat_id, 'user_id': user_id },
            success: function(response){

            $("#div_for_refresh").html(response);
            $('[data-bs-toggle="tooltip"]').tooltip();
            },
            error: function(response){
            console.log("An error occured-----------------------")
                //alert('An error occured')
            }
        });
    },10000);
    })
}