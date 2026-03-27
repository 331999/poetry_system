$(function () {
    var $text = $('#talkwords'),
        $sendBtn = $('#talksub'),
        $mesBox = $('#words');

    // 发送消息的函数
    function sendMessage() {
        var StextCon = $text.val().trim();
        if (StextCon === '') {
            alert('请输入内容');
            return;
        }
        // 使用AJAX发送用户问题到后端
        $.ajax({
            url: '/question/find/',
            method: 'POST',
            data: {
                question: StextCon,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            },
            success: function (response) {
                // console.log('后端响应：', response);
                var sMesContent = '<div class="atalk"><img src="../img/fuzi.jpg" alt="MyBot Avatar" class="avatar"><span>' + response.answer + '</span></div>';
                $mesBox.append(sMesContent);
            },
            error: function (xhr, status, error) {
                console.error('请求后端失败：', error);
            }
        });

        var sMesContent = '<div class="btalk"><img src="../img/xuezi.jpg" alt="User Avatar" class="avatar"><span>' + StextCon + '</span></div>';
        $mesBox.append(sMesContent);
        $text.val('');
    }

    // 提交按钮点击事件处理程序
    $sendBtn.click(sendMessage);

    // 键盘事件处理程序
    $text.keydown(function (e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // 阻止默认行为
            sendMessage();
        }
    });
});