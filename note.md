# mFlaskProject

2016/12/4
重新爬- -
## 页面分析


1.首页或其他页面可以爬到省份信息:

    http://www.shiyebian.net/
    
![省份](./img/diqu.png)

    <div class="diqu">
    <a href="/beijing/">北京</a>
2.地区页面就可以爬到整个省招聘的信息：

    http://www.shiyebian.net/hebei/
1）数据存在无序列表里:

    <div class="listlie">
    <ul class="lie1">
    <li>
    <a href ="招聘信息url"
    </li>
汇总条目带<strong>标签
![具体招聘信息](./img/zhaopinxinxi.png)
2）翻页：

    /地区 或/地区/index.html 为首页
    /地区/index_页数.html 位置后页面
html标签如下:

    <div class="fanye">
    <a href="下n页url">第n页</a>
3.选择市：

    <div class="xdaohang">
![选择市](./img/xuanzeshi.png) 
如果是直辖市则显示:
![选择市](./img/quxian_1.png) 
4.具体区县页面（貌似没有翻页）:

    <div class="lie_qx">
![选择区县](./img/quxian_2.png)   
    
##思路分析

爬去的内容分为两种：

    1.省市的全部招聘信息 exp:
        http://www.shiyebian.net/hebei/
        http://www.shiyebian.net/hebei/shijiazhuang/
    2.区县的全部招聘信息 exp:
        http://www.shiyebian.net/hebei/shijiazhuangqiaodongqu/
        http://www.shiyebian.net/beijing/dongchengqu/
