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
            
            console.log('提交的数据:', {
                poetry_name: this.poetry_name,
                poet_name: this.poet_name,
                poetry_content: this.poetry_content
            });

            // 使用 axios 发送数据到后端
            axios.post('/write/selfWrite/', formData, {
                headers: {
                    'X-CSRFToken': this.csrf_token,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => {
                    console.log('响应数据:', response.data);
                    if (response.data.success) {
                        // 提交成功后刷新页面，加载新提交的诗词
                        alert('作品提交成功！');
                        window.location.reload();
                    } else {
                        // 显示错误信息
                        console.error('表单验证失败:', response.data.errors);
                        alert('提交失败，请检查输入内容！');
                    }
                })
                .catch(error => {
                    // 处理错误
                    console.error('提交失败:', error);
                    if (error.response) {
                        console.error('错误响应:', error.response.data);
                    }
                    alert('提交失败，请重试！');
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