$(document).ready(function() {

    $('body').iealert({support: "ie7",overlayClose: false});

    //根据浏览器宽度给相应的组件加上class
    //isbrowserSize('start');

    //关闭AJAX相应的缓存
    $.ajaxSetup ({ cache: false });

    //系统选择
    var isSystemMenu = false;
    $(".b-select-system .bss-btn").click(function() {
        var bssmenu = $(this).next();
        var bss = $(this).parent();
        if (bssmenu.is(":visible")) {
            bss.removeClass("open");
            bssmenu.slideUp(200);
            isSystemMenu = false;
        }else{
            bss.addClass("open");
            bssmenu.slideDown(200);
            isSystemMenu = true;
        }
        return false;
        //event.stopPropagation();
    });

    //导航 (二级菜单的显示与隐藏)
    $(".b-sidebar-menu .bsm-item > a.bsmi-btn").click(function() {
        //关闭所有已打开的下级菜单
        $(".b-sidebar-menu .bsm-item.open").removeClass("open");
        $(".b-sidebar-menu .bsm-item .bsmi-sub").slideUp(200);
        //打开已点击栏目的下级菜单
        var sub = $(this).next();
        if (sub.is(":visible")) {
            $(this).parent().removeClass("open");
            sub.slideUp(200);
        }else{
            $(this).parent().addClass("open");
            sub.slideDown(500);
        }
        return false;
    });

    //点击空白处执行
    $(document).click(function() {
        //收起系统选择菜单
        if (isSystemMenu){
            $(".b-select-system").removeClass("open");
            $(".b-select-system .bss-menu").slideUp(100);
            //alert("2") 
        }
    });

    //m-cbox缩放内容
    $(".m-cbox .mcht-zoom-btn").click(function() {
        //var mczoombtn = $(this);
        var mczoomicon = $(this).find("i");
        var mcbody = $(this).parent().parent().next();
        if (mcbody.is(":visible")) {
            mcbody.slideUp(200);
            mczoomicon.attr("class","icon-chevron-up");
        }else{
            mcbody.slideDown(200);
            mczoomicon.attr("class","icon-chevron-down");
        }
        return false;
    });

    //m-cbox 删除
    $(".m-cbox .mcht-del-cbox-btn").click(function() {
        var cbox = $(this).parent().parent().parent();
        var isurl = $(this).attr("href");
        if (isurl=== "" || isurl === "#") {
            cbox.fadeOut("fast",function() {
                cbox.remove();
            });
            //cbox.remove();
        }else{
            alert("ajax 访问url地址，处理返回数据,删除href里的URL地址,再点击删除会直接删除这个CBox");
            /*$.ajax({
                url: isurl,
                type: 'GET',
                //dataType: 'default: Intelligent Guess (Other values: xml, json, script, or html)',
                //data: {param1: 'value1'},
            })
            .done(function() {
                console.log("success");
            })
            .fail(function() {
                console.log("error");
            })
            .always(function() {
                console.log("complete");
            });*/
        }
        return false;
    });


    // custom scrollbar {, autohidemode: false}
    $(".b-sidebar-scroll, .b-select-system .bss-menu").niceScroll({styler:"fb",cursorcolor:"#0066cc", cursorwidth: '0', background: '#f0f0f0', cursorborderradius: '5', cursorborder: ''});

    $("html, .js-scrooll").niceScroll({styler:"fb",cursorcolor:"#FC4C03", cursorwidth: '10', cursorborderradius: '0', background: '#f0f0f0', cursorborder: '', zindex: '1031'});

    //star rating 
    $(".m-rating .star").click(function() {
        var numstar = $(this).attr("data-star");
        var srurl = $(this).parent().attr("data-geturl")+numstar;
        alert(srurl);
        /*$.ajax({
            url: srurl,
            type: 'GET',
            //dataType: 'default: Intelligent Guess (Other values: xml, json, script, or html)',
            //data: {param1: 'value1'},
        })
        .done(function() {
            console.log("success");
        })
        .fail(function() {
            console.log("error");
        })
        .always(function() {
            console.log("complete");
        });*/
    });

    //tool tips
    $('.m-element').tooltip();
    $('.m-tooltips').tooltip();

    //popovers
    $('.m-popovers').popover();


    //checkbox all select
    $('.js-all-select').on("click", function() {
        var rangeName = $(this).attr("data-range-name");
        if (rangeName) {
            $(rangeName+" input[type='checkbox']:not(:disabled)").prop("checked",this.checked);
        }else{
            $("input[type='checkbox']:not(:disabled)").prop("checked",this.checked);
        }
    });


    //raty
    if ($('.js-raty').length > 0){
        $('.js-raty').raty({
            path:'stylelib/plugins/raty/img/',
            score: function() {
                return $(this).attr('data-score');
            },
            click: function(score, evt) {
                alert($(this).attr('date-url') + "\nscore: " + score);
            }
        });
    }


    //Open and hidden main-menu
    if ($('.mch-smenu-btn').length > 0) {
        $('.mch-smenu-btn').on('click', function(){
            if ($("body").width() > 960){
                var sidebar = $("#main-menu");
                var maincontent = $("#main-content");
                var paggeactions = $(".b-page-actions")
                if (sidebar.is(":visible")) {
                    sidebar.css("display","none");
                    maincontent.css("margin-left","0");
                    paggeactions.css("margin-left","0");
                }else{
                    sidebar.css("display","");
                    maincontent.css("margin-left","");
                    paggeactions.css("margin-left","");
                }
            }
        });
    }


    //Custom iFrame modal
    if ($('[data-atype=modal]').length > 0){
        var modalgroup = [];
        $('[data-atype=modal]').each(function(index) {
            modalgroup[index] = {
                'url' : $(this).attr('href'),
                'title' : $(this).attr('data-title'), 
                'width' : $(this).attr('data-width')? $(this).attr('data-width'): '',
                'height' : $(this).attr('data-height')? 'style="height:'+ $(this).attr('data-height') +';"' : ''
                // 'fnfex' : $(this).attr('data-fnfex'),
                // 'fnbex' : $(this).attr('data-fnbex')
            };
            if ($(this).attr('data-height') == 'auto') {
                modalgroup[index]['height'] = $(window).height() - ($(window).height()*0.1*3);
                modalgroup[index]['height'] = 'style="height:'+ modalgroup[index]['height'] +'px;"';
            }

            $(this).on('click',function() {
                //var aaaa = eval(modalgroup[index]['fnfex']+"()");
                
                if ( $('#iframe-modal-'+index).length <=0 ){
                    $('body').append('<div id=\"iframe-modal-'+ index + '\" class="modal hide fade '+modalgroup[index]['width']+'" tabindex="-1" role="dialog" aria-hidden="true"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3>'+ modalgroup[index]['title'] +'</h3></div><iframe frameborder="0" scrolling="no" src="'+ modalgroup[index]['url'] + '" name="modal_iframe_' + index + '" id="modal_iframe_' + index + '" class="m-modal-iframe" '+ modalgroup[index]['height'] +'></iframe></div>');
                }

                $('#iframe-modal-'+ index + ' iframe').attr('src', modalgroup[index]['url']);
                $('#iframe-modal-'+index).modal('show');
                return false;
            });
        });
    }

    //open senior search
    $('.mcb-senior-search .mcbsc-showmore').click(function(event) {
        var ssobj = $(this).closest('.mcb-senior-search');
        if (ssobj.hasClass('open')){
            ssobj.removeClass('open');
            $(this).html('高级 <i class="icon-angle-down"></i>');
        }else{
            ssobj.addClass('open');
            $(this).html('收缩 <i class="icon-angle-up"></i>');
        }
        return false;
    });


    //table col float
    if ($('.m-swtable').length > 0) {
        pratable = [];
        $('.m-swtable').each(function(index) {
            var iDataTableHeight = $(this).find('.ms-datatable tr:first th').height()+17;
            pratable[index] = $(this).find('.ms-pratable');
            pratable[index].css('top', iDataTableHeight);
            pratable[index].width('auto');
            $(this).scroll(function(){
                if ($(this).scrollLeft() <= 0) {
                    pratable[index].css('left', '-9999px');
                }else{
                    pratable[index].css('left', $(this).scrollLeft());
                }
            })

        });
    }

});


/*-------------------------------------------------------0
* Resize Action
*/
$(window).on("resize", function(){
       //function
       //isbrowserSize("size");
});

/*-------------------------------------------------------0
* loading alert
*/

var la_open = function() {
    var la = $("#loading-alert");
    if (la.length <= 0){
        $("body").append('<div id="loading-alert">请稍等...</div>');
    }
}

var la_msg = function(str) {
    $("#loading-alert").html(str).fadeOut(2500,function(){ la_close(); });
}

var la_close = function() {
    $("#loading-alert").remove();
}

/*-------------------------------------------------------
* Modal Action
*/

/*
* sMname string  // windos.name
* iAction int // 取消还是删除，0以上整数为[取消]。0及负数为[删除]。区别在于是否删除html里的生成的代码。
* bIsReload boolean  // 关闭后是否刷新父框架页面, true 刷新，false 不刷新(默认)
*/
var IframeModalCC = function(sMname,iAction,bIsReload) {
    var iModalId = sMname.split('_')[2];
    if (iAction){
        var ifmbox = $('#iframe-modal-' + iModalId);
        ifmbox.modal('hide');
        setTimeout(function() {
            ifmbox.remove();
        },800);
    }else{
        $('#iframe-modal-' + iModalId).modal('hide');
    }

    if (bIsReload){
        location.reload();
    }
}


/*-------------------------------------------------------
* Custom Function
*/
// var isbrowserSize = function() {
//     var pageWidth = $("body").width();
//     if ( pageWidth <= 767 ) {
//         $(".b-top-nav .top-menu .dropdown-menu").addClass('m-max767');
//         //.niceScroll({styler:"fb",cursorcolor:"#0066cc", cursorwidth: '5', cursorborderradius: '0', cursorborder: ''});
//     }
//     if (pageWidth >= 980) {
//         var zoombtn = $(".mch-smenu-btn");
//         var sidebar = $("#main-menu");
//         var maincontent = $("#main-content");
//         var paggeactions = $(".b-page-actions")
//         zoombtn.on('click', function() {
            
//             if (sidebar.is(":visible")) {
//                 alert(1);
//                 sidebar.css("display","none");
//                 maincontent.css("margin-left","0");
//                 paggeactions.css("margin-left","0");
//             }else{
//                 alert(2);     
//                 sidebar.css("display","");
//                 maincontent.css("margin-left","");
//                 paggeactions.css("margin-left","");
//             }
//         });
//     }
// }

