// Update navigation buttons based on login status
// 检查登录状态并更新首页按钮显示

(function() {
  // 检查是否有 username cookie，表示已登录
  function isUserLoggedIn() {
    return document.cookie && document.cookie.includes('username=');
  }

  // 更新按钮显示状态
  function updateButtonStates() {
    const loginBtn = document.getElementById('loginBtn');
    const personalBtn = document.getElementById('personalBtn');

    if (loginBtn && personalBtn) {
      if (isUserLoggedIn()) {
        // 已登录：隐藏登录按钮，显示个人中心按钮
        loginBtn.style.display = 'none';
        personalBtn.style.display = 'block';
        personalBtn.style.opacity = '1';
      } else {
        // 未登录：显示登录按钮，隐藏个人中心按钮
        loginBtn.style.display = 'block';
        personalBtn.style.display = 'none';
      }
    }
  }

  // 页面加载时检查一次
  document.addEventListener('DOMContentLoaded', updateButtonStates);

  // 定期检查（每5秒），防止用户状态变化
  setInterval(updateButtonStates, 5000);
})();
