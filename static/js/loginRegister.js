// static/js/loginRegister.js

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

// 配置 axios 默认携带 CSRF token
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

// 界面切换动画
let login = document.getElementById('login');
let login_box = document.getElementsByClassName('login-box')[0];
let register = document.getElementById('register');
let form_box = document.getElementsByClassName('form-box')[0];
let register_box = document.getElementsByClassName('register-box')[0];

login.addEventListener('click', () => {
    form_box.style.transform = 'translateX(0%)';
    register_box.classList.add('hidden');
    login_box.classList.remove('hidden');
});

register.addEventListener('click', () => {
    form_box.style.transform = 'translateX(80%)';
    login_box.classList.add('hidden');
    register_box.classList.remove('hidden');
});

// 注册表单验证
let allFieldsValid = false;

document.getElementById('register_studentId').addEventListener('input', function () {
    var studentId = this.value;
    var registerStuIdSpan = document.getElementById('register_stuId');

    if (studentId.length !== 12 || !/^\d+$/.test(studentId)) {
        registerStuIdSpan.textContent = '学号必须为12位数字';
        registerStuIdSpan.style.color = 'red';
        registerStuIdSpan.style.fontSize = '12px';
    } else {
        registerStuIdSpan.textContent = '';
    }
    checkAllFieldsValid();
});

document.getElementById('pwd1').addEventListener('input', function () {
    var pwd1 = this.value;
    var pwd1Span = document.getElementById('pwd1Span');

    if (pwd1.length < 8 || pwd1.length > 20) {
        pwd1Span.textContent = '密码长度必须在8到20位之间';
        pwd1Span.style.color = 'red';
        pwd1Span.style.fontSize = '12px';
    } else if (!/[a-zA-Z]/.test(pwd1) || !/\d/.test(pwd1)) {
        pwd1Span.textContent = '密码必须包含字母和数字';
        pwd1Span.style.color = 'red';
        pwd1Span.style.fontSize = '12px';
    } else {
        pwd1Span.textContent = '';
    }
    checkAllFieldsValid();
});

document.getElementById('pwd2').addEventListener('input', function () {
    var pwd1 = document.getElementById('pwd1').value;
    var pwd2 = this.value;
    var pwd2Span = document.getElementById('pwd2Span');

    if (pwd2 !== pwd1) {
        pwd2Span.textContent = '两次密码输入不匹配';
        pwd2Span.style.color = 'red';
        pwd2Span.style.fontSize = '12px';
    } else {
        pwd2Span.textContent = '';
    }
    checkAllFieldsValid();
});

document.getElementById('securityQuestion').addEventListener('change', function () {
    var questionSpan = document.getElementById('questionSpan');
    if (!this.value) {
        questionSpan.textContent = '请选择安全问题';
        questionSpan.style.color = 'red';
        questionSpan.style.fontSize = '12px';
    } else {
        questionSpan.textContent = '';
    }
    checkAllFieldsValid();
});

document.getElementById('securityAnswer').addEventListener('input', function () {
    var answerSpan = document.getElementById('answerSpan');
    if (!this.value.trim()) {
        answerSpan.textContent = '请填写安全问题答案';
        answerSpan.style.color = 'red';
        answerSpan.style.fontSize = '12px';
    } else {
        answerSpan.textContent = '';
    }
    checkAllFieldsValid();
});

function checkAllFieldsValid() {
    const studentId = document.getElementById('register_studentId').value;
    const pwd1 = document.getElementById('pwd1').value;
    const pwd2 = document.getElementById('pwd2').value;
    const question = document.getElementById('securityQuestion').value;
    const answer = document.getElementById('securityAnswer').value;

    allFieldsValid =
        studentId.length === 12 &&
        /^\d+$/.test(studentId) &&
        pwd1.length >= 8 &&
        pwd1.length <= 20 &&
        /[a-zA-Z]/.test(pwd1) &&
        /\d/.test(pwd1) &&
        pwd2 === pwd1 &&
        question !== '' &&
        answer.trim() !== '';

    document.getElementById('submitButton1').disabled = !allFieldsValid;
}

// 注册表单提交
document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('username', document.getElementById('register_studentId').value);
    formData.append('password', document.getElementById('pwd1').value);
    formData.append('password2', document.getElementById('pwd2').value);
    formData.append('security_question', document.getElementById('securityQuestion').value);
    formData.append('security_answer', document.getElementById('securityAnswer').value);

    axios.post('/users/register/', formData)
        .then(response => {
            if (response.data.code === 200) {
                alert('注册成功！');
                window.location.href = response.data.redirect_url || '/users/login/';
            } else {
                alert(response.data.msg || '注册失败');
            }
        })
        .catch(error => {
            const msg = error.response?.data?.msg || '注册过程中发生错误，请稍后再试';
            alert(msg);
        });
});

// 登录表单验证
document.getElementById('login_studentId').addEventListener('input', function () {
    var studentId = this.value;
    var loginStuIdSpan = document.getElementById('login_stuId');

    if (studentId.length !== 12 || !/^\d+$/.test(studentId)) {
        loginStuIdSpan.textContent = '学号必须为12位数字';
        loginStuIdSpan.style.color = 'red';
        loginStuIdSpan.style.fontSize = '12px';
    } else {
        loginStuIdSpan.textContent = '';
    }
});

// 登录表单提交
document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('username', document.getElementById('login_studentId').value);
    formData.append('password', document.getElementById('login_pwd').value);
    formData.append('remembered', document.getElementById('remembered').checked);

    axios.post('/users/login/', formData)
        .then(response => {
            if (response.data.code === 200) {
                alert('登录成功！');
                window.location.href = response.data.redirect_url || '/';
            } else {
                alert(response.data.msg || '登录失败');
            }
        })
        .catch(error => {
            const msg = error.response?.data?.msg || '登录过程中发生错误';
            alert(msg);
        });
});
