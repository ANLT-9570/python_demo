$("#obtain").click(function () {
    var ema = $("input[name=email]").val();
    // var ema = $("#obtain").val();
    console.info(ema+"-----*****")
    if (ema == '' || ema == null ){
        console.info("请输入邮箱")
        return ;
    }

    $.ajax({
            url:'/cms/send_en_email/',
            type:'get',
            data:{
                "email":ema,
            },
            contentType:'application/json',
            //headers: {'X-CSRFToken': $("meta[name=csrf_tokens]").attr("content")},
            success:function (response) {
                console.info(response);
            }
        })



})

$("#submit").click(function (event) {
    event.preventDefault();

    var email = $("input[name=email]").val()
    var captch = $("input[name=captch]").val()

    if(email == '' || email == null || captch == '' || captch == null){
        console.info("邮箱或验证码不能为空")
        return ;
    }

    $.ajax({
            url:'/cms/resetmail',
            type:'POST',
            data:{
                "email":email,
                "captch":captch
            },
            contentType:'application/json',
            headers: {'X-CSRFToken': $("meta[name=csrf_tokens]").attr("content")},
            success:function (response) {
                console.info(response);
            }
        })

})