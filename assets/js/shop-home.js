/*const { fill } = require("lodash");*/

$(document).ready(function() {
  $('#delivery').show();
  $('#takeaway').hide();


    $("#sidebarCollapse").on("click", function() {
      $("#sidebar").addClass("active");
    });
  
    $("#sidebarCollapseX").on("click", function() {
      $("#sidebar").removeClass("active");
    });
  
    $("#sidebarCollapse").on("click", function() {
      if ($("#sidebar").hasClass("active")) {
        $(".overlay").addClass("visible");
        console.log("it's working!");
      }
    });
  
    $("#sidebarCollapseX").on("click", function() {
      $(".overlay").removeClass("visible");
    });


    var btn = $('#button');

$(window).scroll(function() {
  if ($(window).scrollTop() > 50) {
    btn.addClass('show');
  } else {
    btn.removeClass('show');
  }
});

btn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:0}, '300');
});

  });
  

  var myVar;

function myFunction() {
  myVar = setTimeout(showPage, 3000);
}



function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
}





function Build(){
  var size=$("input[name='size']:checked").val();
  var flavor=$("input[name='flavor']:checked").val();
  var filling=$("input[name='filling']:checked").val();
  var icing=$("input[name='icing']:checked").val();
  var name=$("#name").val();
  var phone=$("#phone").val();
  var count=$('#phone').val().length;
  var msg="";
  var counter=1;
  if(!size || !flavor || !filling || !icing || name=="" || phone=="" || count!=8){
      if(!size){
        msg+="  <li> Please select size for the cake.</li>";
      }
      if(!flavor){
        msg+="  <li> Please select flavor for the cake.</li>";
      }
      if(!filling){
        msg+="  <li> Please select filling for the cake.<br>";
      }
      if(!icing){
        msg+="  <li> Please select icing for the cake.<br>";
      }
      if(name==""){
        msg+="  <li> Please enter your name.<br>";
      }
      if(phone==""){
        msg+="  <li> Please enter your phone number.<br>";
      }
      if(count!=8){
        msg+="  <li> Please enter a valid phone number.<br>";
      }
        $('#alert').addClass('alert');
        $('#alert').html("<ol>"+msg+"</ol>");
        $('html, body').animate({
            scrollTop: $("#main").offset().top
        },500);
  }else{

    var message=$("#message").val();
    var note=$("#note").val();
    var image=$('#image').val().replace(/C:\\fakepath\\/i, '');

    $.ajaxSetup({ //if method == post
      headers: {
          'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
      }
    });

    var order="<div class='text-center empty-cart'>"
    +"<img src='../images/tick.png' class='img-fluid' >"
    +"<h4>Your order has been placed</h4>"
    +"<p>You will get notification whenever your cake is done.<br>"
    +"Estimated time: 6 hours</p></div>";

    $.ajax ({
      url:"/shop/customize/build",
      method:'post',
      data:{
        name:name,
        phone:phone,
        size:size,
        flavor:flavor,
        filling:filling,
        icing:icing,
        message:message,
        note:note,
        image:image
      },
      
      success:function(output){
        if(output.alert=="success"){
          $("#main").html(order);
        }
      }
    });


        
  }
}


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


function Contact(){

  var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    var name=$("#name").val();
    var email=$("#email").val();
    var subject=$("#subject").val();
    var message=$("#message").val();

    if(name=="" || email=="" || subject=="" || message==""){
      if(name==""){
        $("#name").focus();
        return;
      }
      if(email==""){
        $("#email").focus();
        return;
      }
      if(!email.match(mailformat)){
        $("#email").focus();
        $('#emailalert').text('Enter a valid email address');
        return;
      }
      if(subject==""){
        $("#subject").focus();
        return;
      }
      if(message==""){
        $("#message").focus();
        return;
      }
    }else{
      
    }
}

function AddToCart(id){
 $('#btn'+id).html("<i class='fa fa-refresh fa-spin'></i> Adding");//add spinner icon to button

  $.ajaxSetup({ //if method == post
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
  });
  $.ajax ({
    url:"/shop/products/AddtoCart",
    method:'post',
    data:{
      id: id//set the selected value
    },
    
    success:function(output){
     //alert(output.res);
     
      $('#btn'+id).html("added");//change the value of button
       
     window.setTimeout(function(){
      $('#btn'+id).html("Add to Cart"); //wait and change the value of button
       }, 1000);
       $('.item-nb').html(output.count);//change the value of cart
       var popup = document.getElementById("myPopup");
       popup.classList.toggle("show");

       window.setTimeout(function(){
        popup.classList.toggle("show");
         }, 1500);
         
    }
  });
}





function get(){
    $('input[name="pick"]:checked').each(function() {
      var subtotal=parseInt(document.getElementById('subtotal').innerHTML);
          if(this.value=="takeaway"){

            $('#total').text(subtotal);
            $('#charge').text('0');
            $('#takeaway').show();
            $('#delivery').hide();
          }else if(this.value=="delivery"){
            
            $('#total').text(subtotal+20000);
            $('#charge').text('20000');
            $('#delivery').show();
            $('#takeaway').hide();
          }
    });
}
  


function PlaceOrder(){

  $.ajaxSetup({ //if method == post
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
  });
  var total=$('#total').text();
  
        var delivery="<img src='../images/deliv.png' class='img-fluid'>"
        +"<h4>Your order has been placed</h4>"
        +"<p>Estimated delivery Date: 24 hours</p>"
        +"<p>Payment: <span id=pay></span> L.L Cash on delivery</p>"
        +"<p class='text-danger'>NOTE: Orders on Sunday will be delivered on Monday.</p>";

        var takeaway=""
        +"<img src='../images/takaway.png'  class='img-fluid'>"
        +"<h4>Your order has been placed</h4>"
        +"<p>Estimated cake away Date:6 work hours</p>"
        +"<p>Payment method: Cash</p>"
        +"<p class='text-danger'>NOTE: We will notify whenever the cake is done.</p>";
  
  

      
      //! *******************************************************************
      //! **************default shipping address*****************************
      //! *******************************************************************
      if($('#Delivery').is(':checked') && $('#default').is(':checked')){

          $.ajax ({
            url:"/shop/checkout/place_deafult",
            method:'post',
            data:{
              total:total
            },
            success:function(output){
              if(output.success=='Order Placed'){
                $('#allpage').hide();
                $('#success').html(delivery);
                $('#pay').text(total);
                $('.cart_qty').text('0');
              }
            }
          });
      }


      //! *******************************************************************
      //! **************new shipping address loggedin************************
      //! *******************************************************************
      else if($('#Delivery').is(':checked') && $('#newaddress').is(':checked')){

              var street=$('#street_cus_d').val();
              var building=$('#building_cus_d').val();
              var city=$('#city_cus_d').val();
              if( city=="" || street=="" || building==""){
                if(city==""){$('#city_cus_d').focus();return;}
                if(street==""){$('#street_cus_d').focus();return;}
                if(building==""){$('#building_cus_d').focus();return;}
              }else{
                $.ajax ({   
                  url:"/shop/checkout/place-newaddress",
                  method:'post',
                  data:{
                    city:city,
                    street:street,
                    building:building,
                    note:$('#note_cus_d').val(),
                    total:total
                  },
                  success:function(output){
                    $('#allpage').hide();
                    $('#success').html(delivery);
                    $('#pay').text(total);
                    $('.cart_qty').text('0');
                  }
                });
              }
           
      }
      
      //! *******************************************************************
      //! **************Delivery temp customer*******************************
      //! *******************************************************************
      else if($('#Delivery').is(':checked') && !$('#newaddress').is(':checked')){
        

              var fn=$('#firstname').val();//get the values of inputs
              var ln=$('#lastname').val();
              var city=$('#city').val();
              var street=$('#street').val();
              var building=$('#building').val();
              var mobile=$('#mobile').val();
              var count=$('#mobile').val().length;//get mobile input length

        if(fn=="" || ln=="" || mobile=="" || count!=8 || isNaN(mobile) || city=="" || street=="" || building==""){
        
          if(fn==""){$('#firstname').focus();return;}
          if(ln==""){$('#lastname').focus();return;}
          if(city==""){$('#city').focus();return;}
          if(street==""){$('#street').focus();return;}
          if(building==""){$('#building').focus();return;}
          if(mobile==""){
            $('#mobile').focus();
            return;
          }
          if(isNaN(mobile)){//if entered value contain letters
            $('#alertmobile').html('Mobile field only digits');
            $('#mobile').focus();
            return;
          }
          if(count!=8){//if entered value not 8
            $('#alertmobile').html('Mobile field should be 8 digits only');
            $('#mobile').focus();
            return;
          } 
        }else{
          alert('ss');  
                $.ajax ({   
                  url:"/shop/checkout/place-delivery",
                  method:'post',
                  data:{
                    fn:fn,
                    ln:ln,
                    mobile:mobile,
                    city:city,
                    street:street,
                    building:building,
                    note:$('#note').val(),
                    total:total
                  },
                  success:function(output){
                    $('#allpage').hide();
                    $('#success').html(delivery);
                    $('#pay').text(total);
                    $('.cart_qty').text('0');
                  }
                });
              }
      }
//! ******************************************************************************************



  

      //! *******************************************************************
      //! **************takeaway temp customer*******************************
      //! *******************************************************************
      else if($('#Takeaway').is(':checked') && $('.123').val()==2){
          

               
              var fn=$('#fn_temp_t').val();//get the values of inputs
              var ln=$('#ln_temp_t').val();

              var mobile=$('#mobile_temp_t').val();
              var count=$('#mobile_temp_t').val().length;//get mobile input length

        if(fn=="" || ln=="" || mobile=="" || count!=8 || isNaN(mobile)){
        
          if(fn==""){$('#firstname').focus();return;}
          if(ln==""){$('#lastname').focus();return;}
          if(mobile==""){
            $('#mobile').focus();
            return;
          }
          if(isNaN(mobile)){//if entered value contain letters
            $('#alertmobile_t').html('Mobile field only digits');
            $('#mobile_temp_t').focus();
            return;
          }
          if(count!=8){//if entered value not 8
            $('#alertmobile_t').html('Mobile field should be 8 digits only');
            $('#mobile_temp_t').focus();
            return;
          } 
        }else{
          
                $.ajax ({   
                  url:"/shop/checkout/place-take",
                  method:'post',
                  data:{
                    fn:fn,
                    ln:ln,
                    mobile:mobile,
                    note:$('#note_temp_t').val(),
                    total:total
                  },
                  success:function(output){
                    $('#allpage').hide();
                    $('#success').html(takeaway);
                    $('#pay').text(total);
                    $('.cart_qty').text('0');
                  }
                });
              }
        


      }

      //! *******************************************************************
      //! **************takeaway loggedin customer***************************
      //! *******************************************************************
      else if($('#Takeaway').is(':checked') && $('.123').val()==1){
        $.ajax ({   
          url:"/shop/checkout/place-takeaway-customer",
          method:'post',
          data:{
            total:total
          },
          success:function(output){
            $('#allpage').hide();
            $('#success').html(takeaway);
            $('#pay').text(total);
            $('.cart_qty').text('0');
          }
        });
    }
    
}



