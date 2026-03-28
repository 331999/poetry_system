// static/js/resetPassword.js

// 获取 CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

const step1 = document.getElementById('step1');
const step2 = document.getElementById('step2');
const step3 = document.getElementById('step3');
const getQuestionBtn = document.getElementById('getQuestionBtn');
const resetBtn = document.getElementById('resetBtn');

let currentUsername = '';
// 获取安全问题
getQuestionBtn.addEventListener('click', function () {
    const username = document.getElementById('username').value;
    const usernameSpan = document.getElementById('usernameSpan');
    if (!username || username.length !== 12 || !/^\d+$/.test(username)) {
        usernameSpan.textContent = '请输入正确的12位学号';
        usernameSpan.style.color = 'red';
        return;
    }
    usernameSpan.textContent = '';
    currentUsername = username;
    axios.get('/users/reset-password/?username=' + username)
        .then(function (response) {
            if (response.data.code === 200) {
                document.getElementById('securityQuestion').textContent = response.data.question;
                step1.classList.add('hidden');
                step2.classList.remove('hidden');
            } else {
                usernameSpan.textContent = response.data.msg || '获取安全问题失败';
                usernameSpan.style.color = 'red';
            }
        })
        .catch(function (error) {
            const msg = error.response?.data?.msg || '网络错误，请稍后再试';
            usernameSpan.textContent = msg;
            usernameSpan.style.color = 'red';
        });
});
// 验证密码
function validatePassword() {
    const pwd = document.getElementById('newPassword').value;
    const pwdSpan = document.getElementById('pwdSpan');
    if (pwd.length < 8 || pwd.length > 20) {
        pwdSpan.textContent = '密码长度必须在8到20位之间';
        pwdSpan.style.color = 'red';
        return false;
    }
    if (!/[a-zA-Z]/.test(pwd) || !/\d/.test(pwd)) {
        pwdSpan.textContent = '密码必须包含字母和数字';
        pwdSpan.style.color = 'red';
        return false;
    }
    pwdSpan.textContent = '';
    pwdSpan.style.color = '';
    return true;
}
document.getElementById('newPassword').addEventListener('input', validatePassword);
document.getElementById('confirmPassword').addEventListener('input', function () {
    const pwd = document.getElementById('newPassword').value;
    const confirm = this.value;
    const confirmSpan = document.getElementById('confirmSpan');
    if (confirm !== pwd) {
        confirmSpan.textContent = '两次密码输入不一致';
        confirmSpan.style.color = 'red';
    } else {
        confirmSpan.textContent = '';
        confirmSpan.style.color = '';
    }
});
// 重置密码
resetBtn.addEventListener('click', function () {
    const answer = document.getElementById('securityAnswer').value;
    const newPwd = document.getElementById('newPassword').value;
    const confirmPwd = document.getElementById('confirmPassword').value;
    const answerSpan = document.getElementById('answerSpan');
    if (!answer.trim()) {
        answerSpan.textContent = '请输入答案';
        answerSpan.style.color = 'red';
        return;
    }
    if (!validatePassword()) {
        return;
    }
    if (newPwd !== confirmPwd) {
        document.getElementById('confirmSpan').textContent = '两次密码输入不一致';
        document.getElementById('confirmSpan').style.color = 'red';
        return;
    }
    const formData = new URLSearchParams();
    formData.append('username', currentUsername);
    formData.append('security_answer', answer);
    formData.append('new_password', newPwd);
    formData.append('new_password2', confirmPwd);
    axios.post('/users/reset-password/', formData)
        .then(function (response) {
            if (response.data.code === 200) {
                step2.classList.add('hidden');
                step3.classList.remove('hidden');
            } else {
                alert(response.data.msg || '重置失败');
            }
        })
        .catch(function (error) {
            const msg = error.response?.data?.msg || '网络错误，请稍后再试';
            alert(msg);
        });
});
