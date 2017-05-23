//@blog:http://blog.csdn.net/lxfhahaha/article/details/72638659
var interval = setInterval( function(){
var script = document.createElement("script")
 script.type = "text/javascript";
 script.src = "http://cdn.static.runoob.com/libs/jquery/1.10.2/jquery.min.js";
 document.getElementsByTagName("head")[0].appendChild(script);
var ifr=$('#iframeautoheight').contents(); //获取iframe
var num=[1,1,1,2,2];  //32比重，非常满意/满意
 ifr.find('#DataGrid1').find("select").each(function (index) {
        $(this).find("option").eq(num[parseInt(Math.random()*5)]).attr("selected",true);
    })
 ifr.find('#Button1').click()
 if(ifr.find('#pjkc').find('option:selected').index()+1 === ifr.find('#pjkc option').size())
     clearInterval(interval)
}, 1500);
