在jq方法体写逻辑：
    //模拟单页跳转
    $(document).ready(function(){
       $("dd>a").click(function (e) {
            e.preventDefault();
            $("iframeMain").attr("src",$(this).attr("href"));
        });
    });
逻辑：通过jq拿a的href值放到iframe的src属性上
解释： 
e.preventDefault();：设置a的点击事件不跳转到另一个页面
 $("iframeMain").attr("src",$(this).attr("href"));：给iframe添加src属性，值为a的href值
 
 
 
 element.on('tab(demo)', function(data){
        var src=$(".layui-tab-item.layui-show").find("iframe").attr("src");
        $(".layui-tab-item.layui-show").find("iframe").attr("src",src);
    });
    
 element.on('tab(demo)', function(data){
        var src=$(".layui-nav-child dd a").attr("herf");
        console.log(src)
        $(".layui-container.layui-show").find("iframe").attr("src",src);
    });

layui-container

<script>
    //JavaScript代码区域
    layui.use('element', function(){
        var element = layui.element;
        element.on('nav(hbkNavbar)',function(elem){
            /*使用DOM操作获取超链接的自定义data属性值*/
            var options = eval('('+elem.context.children[0].dataset.options+')');
            var url = options.url;
            var title = options.title;
            element.tabAdd('tabs',{
                title : title,
                content : '<iframe scrolling="auto" frameborder="0"  src="'+url+'" style="width:100%;height:100%;"></iframe>',
                id : '111'
            });
        });
        /*使用下面的方式需要引用jquery*/
       /* $('.layui-nav-child a').click(function () {
            var options = eval('('+$(this).data('options')+')');
            var url = options.url;
            var title = options.title;
            element.tabAdd('tabs',{
                title : title,
                content : '<iframe scrolling="auto" frameborder="0"  src="'+url+'" style="width:100%;height:100%;"></iframe>'
            });
        });*/
    });
</script>


<div name="details">
    <div>
        {% for depart in meminfos.departs %}
            <div>
            <span>{{ depart.name }}</span> <a href="" >添加成员</a>
            {% for member in meminfos.{{ dptname }} %}
                <li> {{ member.name }}--{{ member.id }}    <a href="" >编辑</a><a href="" >删除</a></li>
            {% endfor %}
            </div>
        {% endfor %}
</div>
