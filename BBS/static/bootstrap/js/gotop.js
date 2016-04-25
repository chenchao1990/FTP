
function GoTop(){
//        返回顶部
    $(window).scrollTop(0);
}


$(function () {
    $(window).scroll(function () {
    //当滚动滑轮时，执行函数体

    var top = $(window).scrollTop();
    if(top>0){
//                显示出返回顶部
        $('.back').removeClass('hide');
    }else{
//                隐藏返回顶部
        $('.back').addClass('hide');
    }
    });
});
