$(function () {
    var $text = $('#talkwords'),
        $sendBtn = $('#talksub'),
        $mesBox = $('#words');

    function cleanMarkdown(text) {
        text = text.replace(/\*\*\*(.*?)\*\*\*/g, '$1');
        text = text.replace(/\*\*(.*?)\*\*/g, '$1');
        text = text.replace(/\*(.*?)\*/g, '$1');
        text = text.replace(/^#{1,6}\s+/gm, '');
        text = text.replace(/^[-*+]\s+/gm, '• ');
        text = text.replace(/`(.*?)`/g, '$1');
        text = text.replace(/```[\s\S]*?```/g, function (match) {
            return match.replace(/```\w*\n?/g, '').replace(/```/g, '');
        });
        text = text.replace(/\n{3,}/g, '\n\n');

        return text;
    }

    function formatText(text) {
        text = cleanMarkdown(text);
        text = text.replace(/\n/g, '<br>');

        return text;
    }

    function detectPoem(text) {
        var poemPattern = /《([^》]+)》[\s\S]*?[，。；！？]/g;
        return poemPattern.test(text);
    }

    function typeWriter(element, text, speed, callback) {
        element.innerHTML = text;

        element.style.opacity = '0';
        element.style.animation = 'fadeIn 0.3s ease-in forwards';

        setTimeout(function () {
            element.style.opacity = '1';
            element.style.animation = '';

            scrollToBottom();

            if (callback) callback();
        }, 300);
    }

    function scrollToBottom() {
        var talkShow = document.getElementById('words');
        if (talkShow) {
            talkShow.scrollTo({
                top: talkShow.scrollHeight,
                behavior: 'smooth'
            });
        }
    }

    function copyToClipboard(text) {
        var tempDiv = document.createElement('div');
        tempDiv.innerHTML = text;
        var plainText = tempDiv.textContent || tempDiv.innerText || '';

        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(plainText).then(function () {
                showCopySuccess();
            }).catch(function (err) {
                fallbackCopy(plainText);
            });
        } else {
            fallbackCopy(plainText);
        }
    }

    function fallbackCopy(text) {
        var textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            document.execCommand('copy');
            showCopySuccess();
        } catch (err) {
            alert('复制失败，请手动复制');
        }

        document.body.removeChild(textArea);
    }

    function showCopySuccess() {
        var toast = document.createElement('div');
        toast.className = 'copy-toast';
        toast.textContent = '已复制到剪贴板';
        document.body.appendChild(toast);

        setTimeout(function () {
            toast.classList.add('show');
        }, 10);

        setTimeout(function () {
            toast.classList.remove('show');
            setTimeout(function () {
                document.body.removeChild(toast);
            }, 300);
        }, 2000);
    }

    function createMessageWithCopy(text, isUser) {
        var messageClass = isUser ? 'btalk' : 'atalk';
        var avatar = isUser ? 'xuezi.jpg' : 'fuzi.jpg';
        var avatarAlt = isUser ? 'User Avatar' : 'MyBot Avatar';

        var messageHtml = '<div class="' + messageClass + '">' +
            '<img src="../img/' + avatar + '" alt="' + avatarAlt + '" class="avatar">' +
            '<div class="message-wrapper">' +
            '<span class="message-text">' + text + '</span>';

        if (!isUser) {
            messageHtml += '<button class="copy-btn" onclick="copyToClipboard(\'' +
                text.replace(/'/g, "\\'").replace(/\n/g, '\\n') + '\')" title="复制回答">' +
                '复制</button>';
        }

        messageHtml += '</div></div>';

        return messageHtml;
    }

    window.copyToClipboard = copyToClipboard;

    function sendMessage() {
        var StextCon = $text.val().trim();
        if (StextCon === '') {
            alert('请输入内容');
            return;
        }

        var sMesContent = createMessageWithCopy(StextCon, true);
        $mesBox.append(sMesContent);
        $text.val('');

        scrollToBottom();

        $.ajax({
            url: '/question/find/',
            method: 'POST',
            data: {
                question: StextCon,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            },
            success: function (response) {
                var formattedAnswer = formatText(response.answer);
                var isPoem = detectPoem(response.answer);
                var poemClass = isPoem ? 'poem-content' : '';

                var sMesContent = '<div class="atalk"><img src="../img/fuzi.jpg" alt="MyBot Avatar" class="avatar"><div class="message-wrapper"><span class="message-text ' + poemClass + '"></span><button class="copy-btn" title="复制回答">复制</button></div></div>';
                $mesBox.append(sMesContent);

                var $lastMessage = $mesBox.find('.atalk:last .message-text');
                var $copyBtn = $mesBox.find('.atalk:last .copy-btn');

                $copyBtn.on('click', function () {
                    copyToClipboard(formattedAnswer);
                });

                typeWriter($lastMessage[0], formattedAnswer, 30);
            },
            error: function (xhr, status, error) {
                console.error('请求后端失败：', error);
                var sMesContent = '<div class="atalk"><img src="../img/fuzi.jpg" alt="MyBot Avatar" class="avatar"><span>抱歉，出现了错误，请稍后再试。</span></div>';
                $mesBox.append(sMesContent);
                scrollToBottom();
            }
        });
    }

    $sendBtn.click(sendMessage);

    $text.keydown(function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
});