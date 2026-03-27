function createNewPoetContainer() {
    // 创建poet_container
    var newContainer = document.createElement('div');
    newContainer.className = 'poet_container';

    // 创建poet_title
    var newTitle = document.createElement('p');
    newTitle.className = 'poet_title';
    newTitle.textContent = '新的诗歌标题'; // 这里可以随机生成或从服务器获取
    newContainer.appendChild(newTitle);

    // 创建poet_name
    var newName = document.createElement('p');
    newName.className = 'poet_name';
    newName.textContent = '新的诗人名字'; // 这里可以随机生成或从服务器获取
    newContainer.appendChild(newName);

    // 创建并添加新的诗歌内容
    var newPoem = document.createElement('div');
    newPoem.className = 'poem';

    // 假设我们有三行诗歌
    // for (var i = 1; i <= 3; i++) {
    //     var newPoemLine = document.createElement('p');
    //     newPoemLine.textContent = '新的诗歌行 ' + i; // 这里可以随机生成或从服务器获取
    //     newPoem.appendChild(newPoemLine);
    // }

    var newPoemLine = document.createElement('p');
    newPoemLine.textContent = '诗歌内容 '; // 这里可以随机生成或从服务器获取
    newPoem.appendChild(newPoemLine);

    newContainer.appendChild(newPoem);

    document.body.appendChild(newContainer);
}

// 监听滚动事件
window.addEventListener('scroll', function () {
    // 当用户滚动到接近页面底部时（设置了一个阈值）
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {

        createNewPoetContainer();
    }
});