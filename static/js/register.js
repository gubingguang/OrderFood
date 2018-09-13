
/*
*功能: 检查手机号码是否符合规范
*返回值:
*  true: 通过验证
*  false: 未通过验证
*/
function checkUphone(){
    var value = $("[name='uphone']").val();
    // 向window对象中增加一个变量flag, 默认值为false
    window.flag = false;
    // trim() 去除两端空格,再验证长度
    if(value.trim().length == 11){
        // 验证手机号是否存在
        $.ajax({
           url: "/check_uphone/",
           type: 'post',
           // data: 'uphone='+value+'&'+$("[name='csrfmiddlewaretoken']").val(),
           data:{
               uphone: value,
               csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
           },
           async: false,
           dataType: 'json',
           success: function(data){
               $('#uphone-show').html(data.text);
               if(data.status==1){
                   window.flag = true;
               }else{
                   window.flag = false;
               }

           }
        });

    }else{
        $('#uphone-show').html('手机号码位数不正确');
        window.flag = false;
    }
    return window.flag;
}

/* 功能: 检查密码是否符号规范
 * 规范:
 *   1. 大于6位
 * 返回值:
 *   true: 通过验证
 *   false: 未通过验证
*/
function checkUpwd(){
    var upwd = $("[name='upwd']").val();
    if(upwd.length >= 6){
        $('#upwd-show').html('通过');
        return true;
    }else{
        $('#upwd-show').html('密码长度不少于6位');
        return false;
    }
}

/*
 * 功能: 确认密码必须与密码一致
*/
function checkCpwd(){
    var cpwd = $("#cpwd").val();
    var upwd = $("[name='upwd']").val();
    if(upwd == cpwd && cpwd != ''){
        $('#cpwd-show').html('密码一致');
        return true;
    }else{
        $('#cpwd-show').html('密码不一致');
        return false;
    }
}

/*
 * 功能: 确认用户名不能为空
*/
function checkUname(){
    var uname = $("[name='uname']").val();
    if(uname.trim().length>0){
        $('#uname-show').html('用户名验证通过');
        return true;
    }else{
        $('#uname-show').html('用户名不能为空');
        return false;
    }
}

/*
 * 功能: 确认邮箱不能为空,需要确保格式正确
*/
function checkUemail(){
    var uemail = $("[name='uemail']").val();
    var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if(uemail){
        $('#uemail-show').html('邮箱验证通过');
        return true;
    }else{
        $('#uemail-show').html('邮箱格式不正确');
        return false;
    }
}


/*
 * DOM 树加载完毕时要执行的操作
 * 包含初始化的行为操作 如: 事件的绑定
*/
$(function(){
    /* 为 name=uphone 的元素绑定 blur 事件*/
    $("[name='uphone']").blur(function(){
        checkUphone();
    });

    /* 为 name=upwd 的元素绑定 blur 事件*/
    $("[name='upwd']").blur(function(){
        checkUpwd();
    });

    $('#cpwd').blur(function(){
       checkCpwd();
    });

    $("[name='uname']").blur(function(){
        checkUname();
    });

    $("[name='uemail']").blur(function(){
        checkUemail();
    });

    /* 为 #formRegister 绑定 submit 事件 */
    $("#formRegister").submit(function(){
        return checkUphone() && checkUpwd() && checkCpwd() && checkUname() && checkUemail();
    });
});



