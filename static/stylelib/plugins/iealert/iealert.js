/*
 * IE Alert! jQuery plugin
 * Version 2.1
 * Author: David Nemes | @nmsdvid
 * http://nmsdvid.com/iealert/
 */

(function ($) {
    function initialize($obj, support) {
    
    
        var panel = "<div class='ie-c'>"
            + "     <span class='ie-logo'></span>"
            + "     <span class='ie-title'>为了更好的浏览和操作体验，我们建议您进行如下操作!</span>"
            + "     <div class='ie-p'>"
            + "            <ul>"
            + "                <li class=\"ie-updata\">"
            + "                    <p>如果您的IE版本为IE7及以下，请您进行高版本的 <strong>下载与安装</strong>。</p>"
            + "                    <div class=\"ie-down-item\">"
            + "                        <div class=\"iedi-k\">Windows XP</div>"
            + "                        <div class=\"iedi-v\">"
            + "                            <a href=\"http://www.microsoft.com/zh-cn/download/internet-explorer-8-details.aspx\">下载(IE8)</a>"
            + "                        </div>"
            + "                    </div>"
            + "                </li>"
            + "                <li class=\"ie-setup\">"
            + "                    <p>如果您的IE版本为IE8、IE9、IE10、IE11 <a href=\"http://sep.ucas.ac.cn/help/browser/ie_help\">请按此步骤进行设置</a></p>"
            + "                </li>"
            + "            </ul>"
            + "            <div class=\"ie-thank\">给您带来的不便请谅解。</div>"
            + "     </div>"
            + " </div>";

        var overlay = $("<div id='ie-alert-overlay'></div>");
        var iepanel = $("<div id='ie-alert-panel'>" + panel + "</div>");

        var docHeight = $(document).height()+17;

        overlay.css("height", docHeight);

        function active() {
            $obj.prepend(iepanel);
            $obj.prepend(overlay);

            var uWidth = $('.ie-down-item').width();
            var iePanel = $('#ie-alert-panel');
            var ieOverlay = $('#ie-alert-overlay');

            if (overlayClose === true) {
                ieOverlay.click(function () {
                    iePanel.fadeOut(100);
                    $(this).fadeOut("slow");
                });
            }

            if (ie === 6) {
                iepanel.addClass("ie6-style");
                overlay.css("background", "#fff");
                $obj.css("margin", "0");
            }
        }

        if (support === "ie9") {            // the modal box will appear on IE9, IE8, IE7, IE6
            if (ie < 10) {
                active();
            }
        } else if (support === "ie8") {     // the modal box will appear on IE8, IE7, IE6
            if (ie < 9) {
                active();
            }
        } else if (support === "ie7") {     // the modal box will appear on IE7, IE6
            if (ie < 8) {
                active();
            }
        } else if (support === "ie6") {     // the modal box will appear only on IE6 and below
            if (ie < 7) {
                active();
            }
        }

    }

    ; //end initialize function

    $.fn.iealert = function (options) {
        var defaults = {
            support:"ie8"
            // title:"Did you know that your Internet Explorer is out of date?",
            // text:"To get the best possible experience using our site we recommend that you upgrade to a modern web browser. To download a newer web browser click on the Upgrade button.",
            // upgradeTitle:"Upgrade",
            // upgradeLink:"http://browsehappy.com/",
            // overlayClose: false
            // closeBtn: true
        };

        var option = $.extend(defaults, options);

        return this.each(function () {
        	
	    	ie = (function(){
	 
			    var undef,
			        v = 3,
			        div = document.createElement('div'),
			        all = div.getElementsByTagName('i');
			    
			    while (
			        div.innerHTML = '<!--[if gt IE ' + (++v) + ']><i></i><![endif]-->',
			        all[0]
			    );
			    
			    return v > 4 ? v : undef;
	    
	    	 }());

	    	 // If browser is Internet Explorer
             if (ie >= 5) {
                var $this = $(this);
                initialize($this, option.support);
                //initialize($this, option.support, option.title, option.text, option.upgradeTitle, option.upgradeLink, option.overlayClose, option.closeBtn);
             }

        });

    };
})(jQuery);
