//注册和登录界面的滑块设计
let login = document.getElementById('login');
let login_box = document.getElementsByClassName('login-box')[0];

// 去登录按钮点击事件
login.addEventListener('click', () => {
    form_box.style.transform = 'translateX(0%)';
    register_box.classList.add('hidden');
    login_box.classList.remove('hidden');
})
let register = document.getElementById('register');
let form_box = document.getElementsByClassName('form-box')[0];
let register_box = document.getElementsByClassName('register-box')[0];

// 去注册按钮点击事件
register.addEventListener('click', () => {
    form_box.style.transform = 'translateX(80%)';
    login_box.classList.add('hidden');
    register_box.classList.remove('hidden');
})

//账号密码格式的验证
let allFieldsValid = false;

document.getElementById('register_studentId').addEventListener('input', function () {
    var studentId = this.value;
    var registerStuIdSpan = document.getElementById('register_stuId');

    if (studentId.length !== 12 || !/^\d+$/.test(studentId)) {
        registerStuIdSpan.textContent = '学号必须为12位数字';
        registerStuIdSpan.style.color = 'red';
        registerStuIdSpan.style.fontSize = "12px";
    } else {
        registerStuIdSpan.textContent = '';
    }
    checkAllFieldsValid();
});

document.getElementById('login_studentId').addEventListener('input', function () {
    var studentId = this.value;
    var loginStuIdSpan = document.getElementById('login_stuId');

    if (studentId.length !== 12 || !/^\d+$/.test(studentId)) {
        loginStuIdSpan.textContent = '学号必须为12位数字';
        loginStuIdSpan.style.color = 'red';
        loginStuIdSpan.style.fontSize = "12px";
    } else {
        loginStuIdSpan.textContent = '';
    }
    checkAllFieldsValid();
});


document.getElementById('pwd1').addEventListener('input', function () {
    var pwd1 = this.value;
    var pwd1Span = document.getElementById('pwd1Span');

    if (pwd1.length < 8 || pwd1.length > 20) {
        pwd1Span.textContent = '密码长度必须在8到20位之间';
        pwd1Span.style.color = 'red';
        pwd1Span.style.fontSize = "12px";
    } else if (!/[a-zA-Z]/.test(pwd1) || !/\d/.test(pwd1)) {
        pwd1Span.textContent = '密码必须包含字母和数字';
        pwd1Span.style.color = 'red';
        pwd1Span.style.fontSize = "12px";
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
        pwd2Span.style.fontSize = "12px";
    } else {
        pwd2Span.textContent = '';
    }
    checkAllFieldsValid();
});

function checkAllFieldsValid() {
    allFieldsValid =
        document.getElementById('register_studentId').value.length === 12 &&
        /^\d+$/.test(document.getElementById('register_studentId').value) &&
        // 添加其他字段的验证条件...
        document.getElementById('pwd1').value.length >= 8 &&
        document.getElementById('pwd1').value.length <= 20 &&
        /[a-zA-Z]/.test(document.getElementById('pwd1').value) &&
        /\d/.test(document.getElementById('pwd1').value) &&
        document.getElementById('pwd2').value === document.getElementById('pwd1').value;

    // 根据验证状态启用/禁用提交按钮
    document.getElementById('submitButton1').disabled = !allFieldsValid;
}

// 注册账号，发送数据
document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault(); // 阻止表单默认提交行为
    var formData = new FormData(this); // 使用FormData收集表单数据

    formData.append('username', document.getElementById('register_studentId').value); // 获取表单中学号
    formData.append('password', document.getElementById('pwd1').value); // 获取表单中密码
    formData.append('password2', document.getElementById('pwd2').value); // 获取表单中密码

    // console.log(formData)
    axios.post('/users/register/', formData)
        .then(response => {
            alert('注册成功');
        })
        .catch(error => {
            // 错误处理逻辑
            alert('注册过程中发生错误，请稍后再试');
        });
});

// 登录时验证账号密码
document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault(); // 阻止表单默认提交行为
    var formData = new FormData(this); // 使用FormData收集表单数据

    formData.append('username', document.getElementById('login_studentId').value); // 获取注册中的学号
    formData.append('password', document.getElementById('login_pwd').value); // 获取注册中的密码

    // console.log(formData)
    axios.post('/users/login/', formData)
        .then(response => {
            alert('登录成功');
        })
        .catch(error => {
            // 错误处理逻辑
            alert('登录过程中出现了网络问题');
        });
});