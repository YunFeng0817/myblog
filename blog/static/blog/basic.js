/**
 * Created by Fitz on 2017/8/17.
 */
//这一段负责导航栏的active动态效果  lt（6）表示序号小于6的全部li
$(document).ready(function () {
          $('ul.nav:first>li').click(function (e) {
              e.preventDefault();
              $('ul.nav:first>li').removeClass('active');
              $(this).addClass('active');

          })
});