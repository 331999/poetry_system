document.addEventListener('DOMContentLoaded', function () {

    changePasswordBtn.addEventListener('click', function () {
        passwordForm.style.display = 'block'; // 显示密码修改表单  
    });

    cancelPasswordBtn.addEventListener('click', function () {
        passwordForm.style.display = 'none'; // 隐藏密码修改表单  
    });
});

const passwordForm = document.getElementById('passwordForm');
const oldPasswordInput = document.getElementById('oldPassword');
const newPasswordInput = document.getElementById('newPassword');
const repeatPasswordInput = document.getElementById('repeatPassword');
const savePasswordBtn = document.getElementById('savePasswordBtn');
const cancelPasswordBtn = document.getElementById('cancelPasswordBtn');
const passwordSpan = document.getElementById('passwordSpan');
const pwd1Span = document.getElementById('pwd1Span');
const pwd2Span = document.getElementById('pwd2Span');

savePasswordBtn.addEventListener('click', () => {
    const newPassword = newPasswordInput.value;
    const repeatPassword = repeatPasswordInput.value;

    if (newPassword.length < 8 || newPassword.length > 24) {
        pwd1Span.textContent = '密码长度必须在8到24位之间';
        newPasswordInput.classList.add('error');
    } else if (!/[a-zA-Z0-9]/.test(newPassword)) {
        pwd1Span.textContent = '密码必须包含数字和字母';
        newPasswordInput.classList.add('error');
    } else if (newPassword !== repeatPassword) {
        pwd2Span.textContent = '两次输入的密码不一致';
        repeatPasswordInput.classList.add('error');
    } else {
        // 使用 AJAX 提交表单  
        const formData = new FormData(passwordForm);

        fetch('/api/update-password', { // 后端 API 地址  
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('密码更新失败');
                }
                return response.text();
            })
            .then(data => {
                // 密码更新成功
                alert('修改成功');
                window.location.href = 'index.html'; // 重定向到首页  
            })
            .catch(error => {
                // 处理错误  
                console.error('密码更新失败:', error);
            });

        // 阻止表单的默认提交行为  
        event.preventDefault();
    }
});

cancelPasswordBtn.addEventListener('click', () => {
    passwordForm.style.display = 'none';
    oldPasswordInput.value = '';
    newPasswordInput.value = '';
    repeatPasswordInput.value = '';
    passwordSpan.textContent = '';
    pwd1Span.textContent = '';
    pwd2Span.textContent = '';
    oldPasswordInput.classList.remove('error');
    newPasswordInput.classList.remove('error');
    repeatPasswordInput.classList.remove('error');
});

newPasswordInput.addEventListener('input', () => {
    pwd1Span.textContent = '';
    newPasswordInput.classList.remove('error');
});

repeatPasswordInput.addEventListener('input', () => {
    pwd2Span.textContent = '';
    repeatPasswordInput.classList.remove('error');
});