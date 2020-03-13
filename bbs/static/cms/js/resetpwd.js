$(function () {
var csrg = $("meta[name=csrf_token]").attr("content");
console.info(csrg+"*------8956")
// alert(csrg)
})

    $("#submits").click(function (event) {
        //阻止按钮的提交表单事件
        event.preventDefault();
        var oldpwd = $("input[name=oldpwd]").val();
        var newpwd = $("input[name=newpwd]").val();
        var new2pwd = $("input[name=new2pwd]").val();

        //var csrg = $("meta[name=csrf_tokens]").attr("content");
        // console.info(csrg)
        $.ajax({
            url:'/cms/resetpwd/',
            type:'POST',
            data:{
                "oldpwd":oldpwd,
                "newpwd":newpwd,
                "new2pwd":new2pwd
            },
            contentType:'application/json',
            headers: {'X-CSRFToken': $("meta[name=csrf_tokens]").attr("content")},
            success:function (response) {
                console.info(response);
            }
        })

    })