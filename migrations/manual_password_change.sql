-- ============================================================
-- 手动修改密码
-- 学号: 202231101199
-- 新密码: tangao123
-- ============================================================

USE poetry_system;

-- 查看当前密码哈希（用于验证）
SELECT
    id,
    username,
    nickname,
    LEFT(password, 50) as password_hash_preview
FROM `user`
WHERE username = '202231101199';

-- 修改密码
-- Django 密码哈希格式: pbkdf2_sha256$870000$SALT$HASH
-- 我们需要先创建新的密码哈希，然后更新

-- 先验证新密码
-- Python 命令生成密码哈希: python -c "from django.contrib.auth import get_user_model; print(get_user_model().make_password('tangao123'))"

-- 运行下面这个查询来生成新的密码哈希
-- 请在 MySQL 中执行以下命令（先运行生成哈希的 Python 命令，然后把结果替换到 UPDATE 语句中）

-- 示例 UPDATE 语句（需要先生成正确的密码哈希）：
-- UPDATE `user`
-- SET password = '生成的密码哈希'
-- WHERE username = '202231101199';

-- ============================================================
-- 步骤 1: 生成密码哈希
-- ============================================================

-- 在命令行中运行这个命令生成密码哈希：
-- python -c "from django.contrib.auth import get_user_model; print(get_user_model().make_password('tangao123'))"

-- ============================================================
-- 步骤 2: 更新密码
-- ============================================================

-- 一旦生成好密码哈希，运行这个命令来更新密码：
-- UPDATE `user`
-- SET password = '生成的哈希值'
-- WHERE username = '202231101199';

-- ============================================================
-- 步骤 3: 验证更新
-- ============================================================

-- 查看更新后的密码
-- SELECT
--     id,
--     username,
--     nickname,
--     LEFT(password, 50) as password_hash_preview
-- FROM `user`
-- WHERE username = '202231101199';

-- ============================================================
-- 说明
-- ============================================================

-- Python 生成密码哈希的方法：
-- 1. 激活虚拟环境: .venv/Scripts/activate
-- 2. 进入项目目录: cd D:/PycharmProjects/poetry_system
-- 3. 运行命令: python -c "from django.contrib.auth import get_user_model; print(get_user_model().make_password('tangao123'))"
-- 4. 复制输出的哈希值
-- 5. 替换上面的 UPDATE 语句中的密码哈希

-- 示例输出应该是这样的格式：
-- pbkdf2_sha256$870000$SALT123$HASH456...

-- 更新后就可以用以下账号登录：
-- 学号: 202231101199
-- 密码: tangao123
