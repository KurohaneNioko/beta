(function () {
    "use strict";

    // initialize with defaults
    var a = $("#id_proposal");
    // a.fileinput();
    // with plugin options
    a.fileinput({'showUpload': false, 'previewFileType':'any', 'language': 'zh',});
})(window.jQuery);
    $(function(){
    $('.captcha').css({
        'cursor': 'pointer'
    })
    $('.captcha').click(function(){
         $.getJSON("/captcha/refresh/",
                  function(result){
             $('.captcha').attr('src', result['image_url']);
             $('#id_captcha_0').val(result['key'])
          });});
    /*$('#id_captcha_1').blur(function(){
  // #id_captcha_1为输入框的id，当该输入框失去焦点是触发函数
        json_data={
            'response':$('#id_captcha_1').val(),  // 获取输入框和隐藏字段id_captcha_0的数值
            'hashkey':$('#id_captcha_0').val()
        }
        $.getJSON('/ajax_val', json_data, function(data){ //ajax发送            $('#captcha_status').remove()
            if(data['status']){ //status返回1为验证码正确， status返回0为验证码错误， 在输入框的后面写入提示信息
                $('#id_captcha_1').after('<span id="captcha_status" >*验证码正确</span>')
            }else{
                 $('#id_captcha_1').after('<span id="captcha_status" >*验证码错误</span>')
            }
        });
    });*/
    })
