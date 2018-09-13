/*
* 功能: 检查登录状态
* 如果有登录信息的话,登录位置处显示: 欢迎xxx退出
* 如果没有登录信息的话,登录位置处显示: [登录][注册有惊喜]
*/
function check_login(){
    $.get('/check_login/', function(data){
        var html = '';
        if(data.status == 0){
            html += "<a href='/login'>[登录]</a>,";
            html += "<a href='/register/'>[注册有惊喜]</a>";
        }else if(data.status == 1){
            // 用户已经处于登录状态
            // data.user 为字符串,解析成json对象
            user = JSON.parse(data.user);
            html += "欢迎:" + user.uname + "&nbsp;&nbsp;";
            html += "<a href='/logout/'>退出</a>";
        }
        $("#list>li:first").html(html);
    },'json');
}

// 异步加载商品类型以及商品列表
function loadGoods(){
    $.get('/type_goods/',function(data){
        var show = '';
        $.each(data,function(i,obj){
            var html = '';
            // 将obj.type转换为json对象
            jsonType = JSON.parse(obj.type);
            html = "<div class='item'>";
                html += "<p class='title'>";
                  html += "<a href='#'>更多</a>";
                  html += "<img src='/"+jsonType.picture+"'>";
                html += "</p>";
                html += "<ul>";
                // 将obj.goods由字符串转换为json数组
                jsonGoods = JSON.parse(obj.goods);
                // 循环遍历jsonGoods中的每一项内容,构建<li></li>
                $.each(jsonGoods,function(j,good){
                    html += "<li ";
                    if((j+1)%5 ==0){
                        html += "class='no-margin'";
                    }
                    html += ">";
                    // 加载li 中的内容
                        html += "<p>";
                            html += "<img src='/" + good.fields.picture + "'>";
                        html += "</p>";
                        html += "<div class='content'>";
                            html += "<a href='javascript:add_cart("+good.pk+");' class='cart'>";
                                html += "<img src='/static/images/cart.png'>";
                            html += "</a>";
                            html += "<p>"+good.fields.title+"</p>";
                            html += "<span>&yen;"+good.fields.price
                                +"/"+good.fields.spec+"</span>";
                        html += "</div>";
                    html += "</li>";
                });

                html += "</ul>";
            html += "</div>";
            show += html;
        });
        // 将拼好的show的内容填充到#main元素中
        $("#main").html(show);
    },'json');
}

/*
* 添加商品至购物车(异步)
* 参数 good_id: 需要添加至购物车的商品的id
* */
function add_cart(good_id){
    /*验证是否有用户处于登录状态
    * 如果未处于登录状态,则给出提示
    * 否则将信息传递给服务器
    * */
    $.get('/check_login/', function(data){
        if(data.status==0){
            alert("请先登录...");
        }else{
            // 向 /add_cart/ 发送异步请求.并将good_id作为参数传递过去
            $.post('/add_cart/', {
                'good_id': good_id,
                'csrfmiddlewaretoken': $.cookie('csrftoken'),
            }, function(data){
                if(data.status==1){
                    alert('添加购物车成功');
                    // 加载当前用户的购物车内商品的数量
                    load_count();
                }else{
                    alert('添加购物车失败');
                }
            },'json');
        }
    },'json');
}

/*
* 加载当前用户的购物车中的商品数量
* */
function load_count(){
    $.get('/cart_count/',function(data){
        $("#myCart>a").html("我的购物车("+data.count+")");
    },'json');
}

/*
* 功能: 网页加载时要执行的操作
*/
$(function(){
    // 检查登录状态 - check_login()
    check_login();
    // 加载所有的商品类别以及对应的商品信息
    loadGoods();
    // 加载当前用户的购物车内的商品数量
    load_count();

});