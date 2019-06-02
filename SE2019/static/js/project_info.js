$("#collect-button").click(ajax_submit);

function ajax_submit() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    var v = $("#collect-input").val();//获取表单的输入值;
    var htmlHref = window.location.href;
    htmlHref = htmlHref.replace(/^http:\/\/[^/]+/, "");
    var addr = htmlHref.substr(htmlHref.lastIndexOf('/', htmlHref.lastIndexOf('/') - 1) + 1);
    var proj_id = addr.slice(addr.lastIndexOf("\/")+1);

    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            // alert(addr);
            // alert(proj_id);
        },

        type: "post",  //数据提交方式（post/get）
        cache: false,
        url: proj_id,  //提交到的url
        data: {"feature":v},//提交的数据
        async: true,
        dataType: "json",//返回的数据类型格式
        success: function(msg){
            var op = msg.msg;
            // alert(op);
            var btn = $('#collect-button');
            if(op === ('de-collect')){
                btn.text('收藏☆');
                btn.attr('class', 'btn btn-primary');
                $('#collect-input').val('收藏');
            }else if(op === 'collect'){
                btn.text('已收藏★');
                btn.attr('class', 'btn btn-success');
                $('#collect-input').val('取消收藏');
            }
        }
    });
    return false;
}