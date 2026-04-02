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
const backBtn = document.getElementById('backBtn');
const dot1 = document.getElementById('dot1');
const dot2 = document.getElementById('dot2');
const dot3 = document.getElementById('dot3');

let currentUsername = '';

// 显示错误信息
function showError(spanId, message) {
    const span = document.getElementById(spanId);
    if (span) {
        span.textContent = message;
        span.style.color = 'red';
        span.style.display = 'block';
    }
}

// 清除错误信息
function clearError(spanId) {
    const span = document.getElementById(spanId);
    if (span) {
        span.textContent = '';
        span.style.display = 'none';
    }
}

// 设置按钮加载状态
function setButtonLoading(btn, loading) {
    if (loading) {
        btn.disabled = true;
        btn.dataset.originalText = btn.textContent;
        btn.textContent = '处理中...';
    } else {
        btn.disabled = false;
        btn.textContent = btn.dataset.originalText;
    }
}

// 更新步骤指示器
function updateStepIndicator(step) {
    dot1.classList.remove('active', 'completed');
    dot2.classList.remove('active', 'completed');
    dot3.classList.remove('active', 'completed');
    
    if (step === 1) {
        dot1.classList.add('active');
    } else if (step === 2) {
        dot1.classList.add('completed');
        dot2.classList.add('active');
    } else if (step === 3) {
        dot1.classList.add('completed');
        dot2.classList.add('completed');
        dot3.classList.add('active');
    }
}

// 验证学号
function validateUsername(username) {
    if (!username) {
        return '请输入学号';
    }
    if (username.length !== 12) {
        return '学号必须为12位';
    }
    if (!/^\d+$/.test(username)) {
        return '学号必须为数字';
    }
    return null;
}

// 获取安全问题
getQuestionBtn.addEventListener('click', function () {
    const username = document.getElementById('username').value.trim();
    
    clearError('usernameSpan');
    
    const error = validateUsername(username);
    if (error) {
        showError('usernameSpan', error);
        return;
    }
    
    currentUsername = username;
    setButtonLoading(getQuestionBtn, true);
    
    axios.get(`/users/reset-password/?username=${username}`)
        .then(function (response) {
            setButtonLoading(getQuestionBtn, false);
            if (response.data.code === 200) {
                document.getElementById('securityQuestion').textContent = response.data.question;
                step1.classList.add('hidden');
                step2.classList.remove('hidden');
                updateStepIndicator(2);
            } else {
                showError('usernameSpan', response.data.msg || '获取安全问题失败');
            }
        })
        .catch(function (error) {
            setButtonLoading(getQuestionBtn, false);
            showError('usernameSpan', error.response?.data?.msg || '网络错误，请稍后再试');
        });
});

// 返回上一步
backBtn.addEventListener('click', function () {
    step2.classList.add('hidden');
    step1.classList.remove('hidden');
    updateStepIndicator(1);
    
    // 清空第二步的输入
    document.getElementById('securityAnswer').value = '';
    document.getElementById('newPassword').value = '';
    document.getElementById('confirmPassword').value = '';
    clearError('answerSpan');
    clearError('pwdSpan');
    clearError('confirmSpan');
});

// 验证密码
function validatePassword() {
    const pwd = document.getElementById('newPassword').value;
    
    if (!pwd) {
        showError('pwdSpan', '请输入新密码');
        return false;
    }
    if (pwd.length < 8 || pwd.length > 20) {
        showError('pwdSpan', '密码长度必须在8到20位之间');
        return false;
    }
    if (!/[a-zA-Z]/.test(pwd) || !/\d/.test(pwd)) {
        showError('pwdSpan', '密码必须包含字母和数字');
        return false;
    }
    
    clearError('pwdSpan');
    return true;
}

// 验证确认密码
function validateConfirmPassword() {
    const pwd = document.getElementById('newPassword').value;
    const confirm = document.getElementById('confirmPassword').value;
    
    if (confirm && confirm !== pwd) {
        showError('confirmSpan', '两次密码输入不一致');
        return false;
    }
    
    clearError('confirmSpan');
    return true;
}

document.getElementById('newPassword').addEventListener('input', function() {
    validatePassword();
    validateConfirmPassword();
});

document.getElementById('confirmPassword').addEventListener('input', validateConfirmPassword);

// 重置密码
resetBtn.addEventListener('click', function () {
    const answer = document.getElementById('securityAnswer').value.trim();
    const newPwd = document.getElementById('newPassword').value;
    const confirmPwd = document.getElementById('confirmPassword').value;
    
    clearError('answerSpan');
    clearError('pwdSpan');
    clearError('confirmSpan');
    
    if (!answer) {
        showError('answerSpan', '请输入答案');
        return;
    }
    
    if (!validatePassword()) {
        return;
    }
    
    if (newPwd !== confirmPwd) {
        showError('confirmSpan', '两次密码输入不一致');
        return;
    }
    
    setButtonLoading(resetBtn, true);
    
    const formData = new URLSearchParams();
    formData.append('username', currentUsername);
    formData.append('security_answer', answer);
    formData.append('new_password', newPwd);
    formData.append('new_password2', confirmPwd);
    
    axios.post('/users/reset-password/', formData)
        .then(function (response) {
            setButtonLoading(resetBtn, false);
            if (response.data.code === 200) {
                step2.classList.add('hidden');
                step3.classList.remove('hidden');
                updateStepIndicator(3);
            } else {
                showError('answerSpan', response.data.msg || '重置失败');
            }
        })
        .catch(function (error) {
            setButtonLoading(resetBtn, false);
            const msg = error.response?.data?.msg || '网络错误，请稍后再试';
            showError('answerSpan', msg);
        });
});

// 回车键提交
document.getElementById('username').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        getQuestionBtn.click();
    }
});

document.getElementById('securityAnswer').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('newPassword').focus();
    }
});

document.getElementById('confirmPassword').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        resetBtn.click();
    }
});
