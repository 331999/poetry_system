//
//
//
//主界面瀑布流设计
// 页面加载时
window.onload = function () {

    fWaterFall();
    // 滚动界面时
    window.onscroll = function () {

        if (fScrollTop()) {
            //获取container
            var container = document.getElementById("container");

            //创建item
            var oItem = document.createElement("div");
            oItem.className = "item";
            //创建pic
            var oPic = document.createElement("div");
            oPic.className = "pic";
            //创建a,里面放img
            var oA = document.createElement("a");
            var oImg = document.createElement("img");
            oImg.src = "../../static/img/水银.jpg";
            //创建br和span
            var oBr = document.createElement("br");
            var oSpan = document.createElement("span");
            oSpan.textContent = "藏药名：111"; // 设置span的文本内容
            //增加操作
            container.appendChild(oItem);
            oItem.appendChild(oPic);
            oPic.appendChild(oA);
            oA.appendChild(oImg);
            oA.appendChild(oBr);
            oA.appendChild(oSpan);
        }
        fWaterFall();
    }
}

// 盒子合理摆放
function fWaterFall() {

    var container = document.getElementById("container");

    //获取可视区域的宽度
    var clientWidth = document.documentElement.clientWidth;

    //获取到页面所有class为item的元素
    var oItem = document.getElementsByClassName("item");

    //获取其中一个item的宽度
    var itemWidth = oItem[0].offsetWidth;

    //计算一行有几个盒子
    var num = Math.floor(clientWidth / itemWidth);

    //设置container的宽度
    // container.style.width = num * itemWidth + "px";

    //承载盒子高度的数组
    var hrr = [];

    for (var i = 0; i < oItem.length; i++) {
        if (i < num) {
            //第一排
            hrr.push(oItem[i].offsetHeight);

        } else {
            //得到第一行图片高度的最小值
            var minHeight = Math.min(...hrr);
            //得到最小值的索引
            var index = fInArray(minHeight, hrr);
            //设置样式
            oItem[i].style.position = "absolute";
            oItem[i].style.left = index * itemWidth + "px";
            oItem[i].style.top = minHeight + "px";
            //改变数组最小值
            hrr[index] = hrr[index] + oItem[i].offsetHeight;
        }
    }
}

//计算数组最小值的位置
function fInArray(min, hrr) {
    for (var i = 0; i < hrr.length; i++) {
        if (hrr[i] == min) {
            return i;
        }
    }
}

//判断什么条件加载图片
function fScrollTop() {
    //所有的item
    var item = document.getElementsByClassName("item");
    //最后一个item
    var lastItem = item[item.length - 1];
    //可视区域高度
    var clientHeight = document.documentElement.clientHeight;
    //滚动距离
    var scrollTop = document.documentElement.scrollTop;

    if (lastItem.offsetTop < (clientHeight + scrollTop)) {
        //开始加载
        return true;
    } else {
        //不加载
        return false;
    }

}

//
//
//
// 点击主界面的“登录”按钮，跳转到登录注册界面
document.getElementById('loginBtn').addEventListener('click', function () {
    window.location.href = "loginRegister.html";
});

//
//
//
//主界面导航栏滑块
$(document).ready(function () {
    $("#nav a").on("click", function () {
        var position = $(this).parent().position();
        var width = $(this).parent().width();
        $("#nav .slide1").css({ opacity: 1, left: +position.left, width: width });
    });
    $("#nav a").on("mouseover", function () {
        var position = $(this).parent().position();
        var width = $(this).parent().width();
        $("#nav .slide2").css({ opacity: 1, left: +position.left, width: width }).addClass("squeeze");
    });
    $("#nav a").on("mouseout", function () {
        $("#nav .slide2").css({ opacity: 0 }).removeClass("squeeze");
    });
    var currentWidth = $("#nav li:nth-of-type(3) a").parent("li").width();
    var current = $("li:nth-of-type(3) a").position();
    $("#nav .slide1").css({ left: +current.left, width: currentWidth });
});