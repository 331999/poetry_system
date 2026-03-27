let vm = new Vue({
    el: '#app',
    data: {
        poetry_name: '',
        poet_name: '',
        poetry_content: '',

    },

    methods: {
        submit_poetry: function (event) {
            event.preventDefault(); // 阻止表单默认提交行为

            // 收集表单数据
            const formData = new FormData();
            formData.append('poetry_name', this.poetry_name);
            formData.append('poet_name', this.poet_name);
            formData.append('poetry_content', this.poetry_content);
            console.log(formData)


            // 使用 fetch 发送数据到后端
            fetch('/write/selfWrite/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.csrf_token // 如果你的网站使用 CSRF 令牌，你需要从 cookie 中获取它并添加到请求头
                }
            })
                .then(data => {
                    // 处理响应数据
                    // console.log(data);
                    // alert('作品提交成功！');
                })
                .catch(error => {
                    // 处理错误
                    console.error('提交失败:', error);
                });
        }
    },
    mounted: function () {
        this.csrf_token = getCookie('csrftoken')
        // 监听表单的 submit 事件
        this.$el.querySelector('#main-contact-form').addEventListener('submit', this.submit_poetry);
    }
});

// 辅助函数，用于获取 CSRF 令牌
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}