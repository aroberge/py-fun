$(document).ready(
  function(){
    $(".panel .header .tab").click(
      function(){
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');
        var tabId = $(this).attr("id");
        var contentId = tabId.slice(0, tabId.length-4);
        $("#"+contentId).siblings(".tab-content").hide();
        $("#"+contentId).show();
      });

    $(".upper_tab").click(
      function(){
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');
        var tabId = $(this).attr("id");
        var contentId = tabId.slice(0, tabId.length-4);
        $("#"+contentId).siblings(".view").hide();
        $("#"+contentId).show();
      });

/*
$(document).ready(function() {
    $(".tab_content").hide();
    $("ul.tabs li:first").addClass("active").show();
    $(".tab_content:first").show();
    $("ul.tabs li").click(function() {
        $("ul.tabs li").removeClass("active");
        $(this).addClass("active");
        $(".tab_content").hide();
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).show(); //Fade in the active ID content
        return false;
    });
});
*/


  });
