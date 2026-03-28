// static/js/personal.js

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

// 模态框操作
const editModal = document.getElementById('editModal');
const passwordModal = document.getElementById('passwordModal');
const editProfileBtn = document.getElementById('editProfileBtn');
const changePasswordBtn = document.getElementById('changePasswordBtn');
const logoutBtn = document.getElementById('logoutBtn');

// 打开编辑资料模态框
editProfileBtn.addEventListener('click', () => {
    editModal.style.display = 'flex';
});

// 打开修改密码模态框
changePasswordBtn.addEventListener('click', () => {
    passwordModal.style.display = 'flex';
});

// 关闭模态框
document.getElementById('closeEditModal').addEventListener('click', () => {
    editModal.style.display = 'none';
});

document.getElementById('closePasswordModal').addEventListener('click', () => {
    passwordModal.style.display = 'none';
    clearPasswordForm();
});

document.getElementById('cancelEditBtn').addEventListener('click', () => {
    editModal.style.display = 'none';
});

document.getElementById('cancelPasswordBtn').addEventListener('click', () => {
    passwordModal.style.display = 'none';
    clearPasswordForm();
});

// 点击模态框外部关闭
window.addEventListener('click', (e) => {
    if (e.target === editModal) {
        editModal.style.display = 'none';
    }
    if (e.target === passwordModal) {
        passwordModal.style.display = 'none';
        clearPasswordForm();
    }
});

// 头像预览
document.getElementById('avatar').addEventListener('change', function (e) {
    const file = e.target.files[0];
    const preview = document.getElementById('avatarPreview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.innerHTML = '<img src="' + e.target.result + '" alt="预览">';
        };
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '';
    }
});

// 编辑资料表单提交
document.getElementById('profileForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    axios.post('/users/profile/', formData)
        .then(function (response) {
            if (response.data.code === 200) {
                alert('资料更新成功！');
                window.location.reload();
            } else {
                alert(response.data.msg || '更新失败');
            }
        })
        .catch(function (error) {
            const msg = error.response?.data?.msg || '网络错误';
            alert(msg);
        });
});

// 密码验证
function validateNewPassword() {
    const pwd = document.getElementById('newPassword').value;
    const span = document.getElementById('newPwdSpan');

    if (pwd.length < 8 || pwd.length > 20) {
        span.textContent = '密码长度必须在8到20位之间';
        return false;
    }
    if (!/[a-zA-Z]/.test(pwd) || !/\d/.test(pwd)) {
        span.textContent = '密码必须包含字母和数字';
        return false;
    }

    span.textContent = '';
    return true;
}

document.getElementById('newPassword').addEventListener('input', validateNewPassword);

document.getElementById('confirmPassword').addEventListener('input', function () {
    const pwd = document.getElementById('newPassword').value;
    const confirm = this.value;
    const span = document.getElementById('confirmSpan');

    span.textContent = confirm !== pwd ? '两次密码输入不一致' : '';
});

// 修改密码表单提交
document.getElementById('passwordForm').addEventListener('submit', function (e) {
    e.preventDefault();

    if (!validateNewPassword()) {
        return;
    }

    const newPwd = document.getElementById('newPassword').value;
    const confirmPwd = document.getElementById('confirmPassword').value;

    if (newPwd !== confirmPwd) {
        document.getElementById('confirmSpan').textContent = '两次密码输入不一致';
        return;
    }

    const formData = new FormData(this);

    axios.post('/users/change-password/', formData)
        .then(function (response) {
            if (response.data.code === 200) {
                alert(response.data.msg || '密码修改成功，请重新登录');
                window.location.href = response.data.redirect_url || '/users/login/';
            } else {
                alert(response.data.msg || '修改失败');
            }
        })
        .catch(function (error) {
            const msg = error.response?.data?.msg || '网络错误';
            alert(msg);
        });
});

// 清空密码表单
function clearPasswordForm() {
    document.getElementById('passwordForm').reset();
    document.getElementById('oldPwdSpan').textContent = '';
    document.getElementById('newPwdSpan').textContent = '';
    document.getElementById('confirmSpan').textContent = '';
}

// 退出登录
logoutBtn.addEventListener('click', function () {
    if (confirm('确定要退出登录吗？')) {
        axios.post('/users/logout/')
            .then(function (response) {
                window.location.href = response.data.redirect_url || '/';
            })
            .catch(function (error) {
                // 如果 POST 失败，尝试 GET
                window.location.href = '/users/logout/';
            });
    }
});
