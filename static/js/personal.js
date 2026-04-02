// static/js/personal.js
// 个人中心页面脚本

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

// 配置 axios 默认携带 CSRF token
const csrftoken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

// 等待 DOM 加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('个人中心页面初始化开始...');

    // 模态框元素
    const editModal = document.getElementById('editModal');
    const passwordModal = document.getElementById('passwordModal');
    const changeSecurityModal = document.getElementById('changeSecurityModal');
    const verifySecurityModal = document.getElementById('verifySecurityModal');
    const editProfileBtn = document.getElementById('editProfileBtn');
    const changePasswordBtn = document.getElementById('changePasswordBtn');
    const changeSecurityBtn = document.getElementById('changeSecurityBtn');
    const verifySecurityBtn = document.getElementById('verifySecurityBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    // 确保所有必要元素都存在
    if (!editModal || !editProfileBtn || !changeSecurityBtn || !verifySecurityBtn) {
        console.error('缺少必要元素，请检查 HTML 代码');
        alert('页面加载不完整，请刷新页面');
        return;
    }

    // 检查用户是否登录
    if (!document.cookie.includes('username=')) {
        console.error('用户未登录');
        window.location.href = '/users/login/';
        return;
    }

    console.log('初始化完成，开始绑定事件...');

    // ========== 模态框操作 ==========

    // 打开编辑资料模态框
    editProfileBtn.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('打开编辑资料模态框');
        editModal.style.display = 'flex';
    });

    // 打开修改密码模态框
    changePasswordBtn.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('打开修改密码模态框');
        passwordModal.style.display = 'flex';
    });

    // 打开修改安全问题模态框
    changeSecurityBtn.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('打开修改安全问题模态框');
        changeSecurityModal.style.display = 'flex';
    });

    // 打开验证答案模态框
    verifySecurityBtn.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('打开验证答案模态框');
        verifySecurityModal.style.display = 'flex';
    });

    // 退出登录
    logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('确定要退出登录吗？')) {
            console.log('点击退出登录');
            window.location.href = '/users/logout/';
        }
    });

    // 关闭函数
    function closeModal(modal) {
        if (modal && typeof modal.style !== 'undefined') {
            modal.style.display = 'none';
        }
    }

    function clearPasswordForm() {
        const form = document.getElementById('passwordForm');
        if (form) {
            form.reset();
            const oldPwdSpan = document.getElementById('oldPwdSpan');
            const newPwdSpan = document.getElementById('newPwdSpan');
            const confirmSpan = document.getElementById('confirmSpan');
            if (oldPwdSpan) oldPwdSpan.textContent = '';
            if (newPwdSpan) newPwdSpan.textContent = '';
            if (confirmSpan) confirmSpan.textContent = '';
        }
    }
    function clearVerifySecurityForm() {
        const form = document.getElementById('verifySecurityForm');
        if (form) {
            form.reset();
            const span = document.getElementById('verifySecurityAnswerSpan');
            if (span) span.textContent = '';
        }
    }

    // 关闭按钮
    const closeEditModal = document.getElementById('closeEditModal');
    if (closeEditModal) {
        closeEditModal.addEventListener('click', function() {
            closeModal(editModal);
        });
    }

    const closePasswordModal = document.getElementById('closePasswordModal');
    if (closePasswordModal) {
        closePasswordModal.addEventListener('click', function() {
            closeModal(passwordModal);
            clearPasswordForm();
        });
    }

    const closeChangeSecurityModal = document.getElementById('closeChangeSecurityModal');
    if (closeChangeSecurityModal) {
        closeChangeSecurityModal.addEventListener('click', function() {
            closeModal(changeSecurityModal);
        });
    }

    const closeVerifySecurityModal = document.getElementById('closeVerifySecurityModal');
    if (closeVerifySecurityModal) {
        closeVerifySecurityModal.addEventListener('click', function() {
            closeModal(verifySecurityModal);
            clearVerifySecurityForm();
        });
    }

    // 取消按钮
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function() {
            closeModal(editModal);
        });
    }

    const cancelPasswordBtn = document.getElementById('cancelPasswordBtn');
    if (cancelPasswordBtn) {
        cancelPasswordBtn.addEventListener('click', function() {
            closeModal(passwordModal);
            clearPasswordForm();
        });
    }

    const cancelChangeSecurityBtn = document.getElementById('cancelChangeSecurityBtn');
    if (cancelChangeSecurityBtn) {
        cancelChangeSecurityBtn.addEventListener('click', function() {
            closeModal(changeSecurityModal);
        });
    }

    const cancelVerifySecurityBtn = document.getElementById('cancelVerifySecurityBtn');
    if (cancelVerifySecurityBtn) {
        cancelVerifySecurityBtn.addEventListener('click', function() {
            closeModal(verifySecurityModal);
            clearVerifySecurityForm();
        });
    }

    // 点击模态框外部关闭
    window.addEventListener('click', function(e) {
        if (e.target === editModal) closeModal(editModal);
        if (e.target === passwordModal) {
            closeModal(passwordModal);
            clearPasswordForm();
        }
        if (e.target === changeSecurityModal) closeModal(changeSecurityModal);
        if (e.target === verifySecurityModal) {
            closeModal(verifySecurityModal);
            clearVerifySecurityForm();
        }
    });

    // ========== 头像预览 ==========
    const avatarInput = document.getElementById('avatar');
    if (avatarInput) {
        avatarInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const preview = document.getElementById('avatarPreview');
            if (!preview) return;

            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.innerHTML = '<img src="' + e.target.result + '" alt="预览">';
                };
                reader.readAsDataURL(file);
            } else {
                preview.innerHTML = '';
            }
        });
    }

    // ========== 邮箱格式验证 ==========
    function validateEmail() {
        const emailInput = document.getElementById('email');
        const emailSpan = document.getElementById('emailSpan');
        if (!emailInput || !emailSpan) return true;

        const email = emailInput.value.trim();
        if (!email) {
            emailSpan.textContent = '';
            emailSpan.style.display = 'none';
            return true;
        }

        const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!pattern.test(email)) {
            emailSpan.textContent = '请输入有效的邮箱地址，格式应为 xxx@xxx.xxx';
            emailSpan.style.color = 'red';
            emailSpan.style.display = 'block';
            return false;
        }

        emailSpan.textContent = '';
        emailSpan.style.display = 'none';
        return true;
    }

    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('input', validateEmail);
        emailInput.addEventListener('blur', validateEmail);
    }

    // ========== 编辑资料表单提交 ==========
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!validateEmail()) {
                return;
            }

            const formData = new FormData(this);

            console.log('提交编辑资料');

            axios.post('/users/profile/', formData)
                .then(function(response) {
                    if (response.data.code === 200) {
                        alert('资料更新成功！');
                        window.location.reload();
                    } else {
                        alert(response.data.msg || '更新失败');
                    }
                })
                .catch(function(error) {
                    const msg = error.response?.data?.msg || '网络错误';
                    alert(msg);
                    console.error('编辑资料失败:', error);
                });
        });
    }

    // ========== 密码验证函数 ==========
    function validateNewPassword() {
        const pwd = document.getElementById('newPassword').value;
        const span = document.getElementById('newPwdSpan');
        if (!span) return false;

        if (pwd.length < 8 || pwd.length > 20) {
            span.textContent = '密码长度必须在8到20位之间';
            span.style.color = 'red';
            return false;
        }
        if (!/[a-zA-Z]/.test(pwd) || !/\d/.test(pwd)) {
            span.textContent = '密码必须包含字母和数字';
            span.style.color = 'red';
            return false;
        }

        span.textContent = '';
        span.style.color = '';
        return true;
    }

    const newPasswordInput = document.getElementById('newPassword');
    if (newPasswordInput) {
        newPasswordInput.addEventListener('input', validateNewPassword);
    }

    const confirmPasswordInput = document.getElementById('confirmPassword');
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', function() {
            const pwd = document.getElementById('newPassword').value;
            const confirm = this.value;
            const span = document.getElementById('confirmSpan');
            if (!span) return;

            if (confirm !== pwd) {
                span.textContent = '两次密码输入不一致';
                span.style.color = 'red';
            } else {
                span.textContent = '';
                span.style.color = '';
            }
        });
    }

    // ========== 修改密码表单提交 ==========
    const passwordForm = document.getElementById('passwordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!validateNewPassword()) return;

            const newPwd = document.getElementById('newPassword').value;
            const confirmPwd = document.getElementById('confirmPassword').value;

            if (newPwd !== confirmPwd) {
                const span = document.getElementById('confirmSpan');
                if (span) span.textContent = '两次密码输入不一致';
                return;
            }

            const formData = new FormData(this);

            axios.post('/users/change-password/', formData)
                .then(function(response) {
                    if (response.data.code === 200) {
                        alert(response.data.msg || '密码修改成功，请重新登录');
                        window.location.href = response.data.redirect_url || '/users/login/';
                    } else {
                        alert(response.data.msg || '修改失败');
                    }
                })
                .catch(function(error) {
                    const msg = error.response?.data?.msg || '网络错误';
                    alert(msg);
                    console.error('修改密码失败:', error);
                });
        });
    }

    // ========== 修改安全问题表单提交 ==========
    const changeSecurityForm = document.getElementById('changeSecurityForm');
    if (changeSecurityForm) {
        changeSecurityForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const securityAnswer = document.getElementById('securityAnswer').value.trim();
            const span = document.getElementById('securityAnswerSpan');

            if (!securityAnswer) {
                if (span) span.textContent = '请输入答案';
                return;
            }

            const formData = new FormData(this);

            axios.post('/users/update-security/', formData)
                .then(function(response) {
                    if (response.data.code === 200) {
                        alert('安全问题修改成功！');
                        closeModal(changeSecurityModal);
                        window.location.reload();
                    } else {
                        alert(response.data.msg || '修改失败');
                    }
                })
                .catch(function(error) {
                    const msg = error.response?.data?.msg || '网络错误';
                    alert(msg);
                    console.error('修改安全问题失败:', error);
                });
        });
    }

    // ========== 验证安全问题表单提交 ==========
    const verifySecurityForm = document.getElementById('verifySecurityForm');
    if (verifySecurityForm) {
        verifySecurityForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const securityAnswer = document.getElementById('verifySecurityAnswer').value.trim();
            const span = document.getElementById('verifySecurityAnswerSpan');

            if (!securityAnswer) {
                if (span) span.textContent = '请输入答案';
                return;
            }

            const formData = new FormData(this);

            axios.post('/users/verify-security/', formData)
                .then(function(response) {
                    if (response.data.code === 200) {
                        alert('答案验证成功！');
                        closeModal(verifySecurityModal);
                    } else {
                        alert(response.data.msg || '答案错误，请重试');
                    }
                })
                .catch(function(error) {
                    const msg = error.response?.data?.msg || '网络错误';
                    alert(msg);
                    console.error('验证安全问题失败:', error);
                });
        });
    }

    console.log('个人中心所有功能初始化完成');
});
