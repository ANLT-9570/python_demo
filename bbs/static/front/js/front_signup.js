$("#cap-img").click(function(){
    var self = $(this)


})

    $("#sms").click(function (event) {
        event.preventDefault();
        phone = $("input[name='telephone']").val();
        if(phone == null || phone == ""){
            alert("手机号不能为空")
            return ;
        }
        var timestamp = (new Date()).getTime();
        var sign = hex_md5(timestamp+phone+"fsdgsdfg56sfd/*dsfa");
        console.info(phone+"timestamp"+timestamp+"sign"+sign)
       /* $.ajax({
            url:'/front/sms_captchas',
            type:'get',
            data:{
                "telephone":phone,
            },
            contentType:'application/json',
            //headers: {'X-CSRF-Token': $("meta[name=csrf_tokens]").attr("content")},
            success:function (response) {
                console.info(response);
            }
        })*/
       var data= JSON.stringify({telephone:phone,timestamp:timestamp,sign:sign});
       $.ajax({
            url:'/common/sms_captchas',
            type:'POST',
            data:data,
            contentType:'application/json',
            headers: {'X-CSRFToken': $("meta[name=csrf_tokens]").attr("content")},
            success:function (response) {
                console.info(response);
            }
        })

    })

$("").click(function (event) {//#sub-btn
    event.preventDefault();

    var telephone = $("input[name='telephone']").val();
    var sms_capycha = $("input[name='sms_capycha']").val();
    var username = $("input[name='username']").val();
    var password = $("input[name='password']").val();
    var password2 = $("input[name='password2']").val();
    var graph_captcha = $("input[name='graph_captcha']").val();

    $.ajax({
            url:'/front/signup',
            type:'POST',
            data:{
                "telephone":telephone,
                "sms_capycha":sms_capycha,
                "username":username,
                "password":password,
                "password2":password2,
                "graph_captcha":graph_captcha,
            },
            contentType:'application/json',
            headers: {'X-CSRFToken': $("meta[name=csrf_tokens]").attr("content")},
            success:function (response) {
                console.info(response);
            }
        })

})