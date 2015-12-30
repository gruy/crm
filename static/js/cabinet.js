/**
 * Created by alexy on 28.05.15.
 */
$(function() {

  var current_url = '/'+location.href.split('/')[3]+'/' + location.href.split('/')[4] + '/';
  $('header ul li a').each(function () {
    if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  });

  $.validator.messages.required = "* поле обязательно для заполнения";

  $.datepicker.setDefaults(
        $.extend($.datepicker.regional["ru"])
  );
  $("#js-surface-photo-add-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $(".start_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $(".end_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-surface-add-client-form #id_date_start").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-surface-add-client-form #id_date_end").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-add-maket-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-add-surface-form #date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-client-add-surface-form #date_end").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-city-form #id_contract_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-adjuster-client_task-add-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-adjuster-client_task-update-form #id_date").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  $("#js-adjuster-task-add-form #id_date_at").datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });

  // валидация формы добавления города
  $( '#js-city-form' ).validate({
    rules: {
      name: {
        required: true
      }
    }
  });

  // валидация формы добавления администратора
  $( '.js-form-administrator-add' ).validate({
    rules: {
      email: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      }
    }
  });
  // валидация формы изменения администратора
  $( '.js-form-administrator-change' ).validate({
    rules: {
      email: {
        required: true
      }
    }
  });
  // открытие модального окна подтверждения удаления администратора
  $('.js-remove-item-btn').click(function(){
    $('#js-modal-item-remove-id').val($(this).data('id'))
    $('#js-modal-item-remove-name').text($(this).data('email'))
  });
  $('.js-remove-item-btn').fancybox({
    afterClose: function () {
      $('.js-modal-remove-item-form').resetForm();
    }
  });
  $('.js-modal-remove-item-form input[type="reset"]').click(function(){
    $.fancybox.close();
  });
  $('.js-modal-remove-item-form input[type="submit"]').click(function(){
    $.fancybox.close();
  });
  $('.js-modal-remove-item-form').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Объект был удалён', 'success');
        console.log(data.success);
        $('tr[data-id='+data.success+']').remove();
      } else {
        $.notify('Произошла ошибка. Объект не удалён', 'error');
      }
      $('.js-modal-remove-item-form').resetForm();
    }
  });


  // валидация формы на странице
  $( '.js-form-password-change' ).validate({
    rules: {
      user_id: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      },
    },
    submitHandler: function(e) {
      $('.js-form-password-change').ajaxSubmit({
          success: function(data){
            if (data.success) {
              $.notify(data.success, 'success');
            } else {
              $.notify(data.error, 'error');
            }
            $('.js-form-password-change').trigger('reset');
          }
      });
    }
  });

  // валидация формы добавления клиента
  $( '.js-form-client-add' ).validate({
    rules: {
      city: {
        required: true
      },
      email: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      }
    }
  });
  // валидация формы добавления монтажника
  $( '.js-form-adjuster-add' ).validate({
    rules: {
      city: {
        required: true
      },
      email: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      }
    }
  });
  // валидация формы добавления монтажника
  $( '.js-form-adjuster-update' ).validate({
    rules: {
      city: {
        required: true
      },
      email: {
        required: true
      }
    }
  });

  $(".js-gallery").fancybox();

//  фильтрация по городам на странице поверхностей
  var get_url = '/'+location.href.split('/');
  //$('header ul li a').each(function () {
  //  if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  //});

  //$('#client_city_filter').change(function(){
  //  $('.client-search-form__city').val($(this).val());
  //  $('.client-search-form').submit();
  //});


  $('#city_filter').change(function(){
    $('.search-form__city').val($(this).val());
    $('.search-form__area').val(0);
    $('.search-form__street').val(0);
    $('.search-form').submit();
  });
  $('#area_filter').change(function(){
    $('.search-form__area').val($(this).val());
    $('.search-form__street').val(0);
    $('.search-form').submit();
  });
  $('#street_filter').change(function(){
    $('.search-form__street').val($(this).val());
    $('.search-form').submit();
  });
  //$('#house_number_filter').change(function(){
  //  $('.search-form__house_number').val($(this).val())
  //  console.log($(this).val());
  //});


  // валидация формы добвления поверхности
  $( '#js-surface-add-form' ).validate({
    rules: {
      city: {
        required: true
      },
      street: {
        required: true
      },
      house_number: {
        required: true
      }
    }
  });

  var surface_add_form = $('#js-surface-add-form');
  var surface_city = surface_add_form.find('select#id_city');
  var surface_street = surface_add_form.find('select#id_street');
  surface_city.change(function(){
    if($(this).val() == ''){
      var city = 0
    } else {
      var city = $(this).val();
    }

    $.ajax({
      type: "GET",
      url: surface_add_form.data('ajax-url'),
      data: {
        city: city
      }
    }).done(function( msg ) {
      var street_list = msg.street_list;
      surface_street.find('option').remove();
      surface_street.append($("<option value selected='selected'>---------</option>"));
      for (var i = 0; i < street_list.length; i++) {
        surface_street.append($("<option/>", {
            value: street_list[i]['id'],
            text: street_list[i]['name']
        }));
      }
    });
  });

  $('.js-show-map').click(function(){
    $('.js-map').slideToggle();
  });
  $('.js-calendar-heading').click(function(){
    $('.js-calendar-body').slideToggle();
  });


    // валидация формы добвления фотографии поверхности
  $( '#js-surface-photo-add-form' ).validate({
    rules: {
      porch: {
        required: true
      },
      date: {
        required: true
      },
      image: {
        required: true
      }
    }
  });


  $('#cas_area').change(function(){
    if ($(this).val() != 0){
      $.ajax({
        type: "GET",
        url: $(this).data('ajax-url'),
        data: {
          area: $(this).val(),
          client: $('#hidden_client').val()
        }
      }).done(function( data ) {
        if (data.surface_list) {
          var surface_list = data.surface_list;
          $('.js-surface-list tr.result').remove();
          var surface_table = $('.js-surface-list thead');
          for (var i = 0; i < surface_list.length; i++){
            surface_table.append(
              '<tr class="result">'+
              '<td><input type="checkbox" name="chk_group[]" value="' +surface_list[i]['id'] +'"></td>'+
              '<td>'+surface_list[i]['street']+'</td>'+
              '<td>'+surface_list[i]['number']+'</td>'+
              '</tr>'
            )
          }
        }
        //var street_list = msg.surfa;
        //surface_street.find('option').remove();
        //surface_street.append($("<option value selected='selected'>---------</option>"));
        //for (var i = 0; i < street_list.length; i++) {
        //  surface_street.append($("<option/>", {
        //      value: street_list[i]['id'],
        //      text: street_list[i]['name']
        //  }));
        //}
      });
    }

  });
  //удаление поверхности клиента
  function removeClientSurface(){
    $('.js-remove-client-surface').submit(function() {
      $(this).ajaxSubmit({
        success: function (data) {
          if (data.success) {
            $.notify('Поверхность удалена', 'success');
          } else {
            $.notify('Произошла ошибка!', 'error');
          }
        }
      });
      $(this).parents('tr').remove();
      return false;
    });
  }
  removeClientSurface();
     //валидация формы добвления поверхности к клиенту

  $('#js-client-add-surface-form').validate({
    rules: {
      area: {
        required: true
      },
      date_start: {
        required: true
      }
    },
    submitHandler: function(e) {
      $('#js-client-add-surface-form').ajaxSubmit({
          success: function(data){
            if (data.success) {
              $.notify(data.success, 'success');
              $('#cas_area').val(0);
              $('.js-surface-list tr.result').remove();
              //$('#js-client-add-surface-form').trigger('reset');
              if (data.surface_list){
                //$.notify(data.surface_list, 'success');
                $('tr.empty').remove();
                var surface_list = data.surface_list;
                for (var i = 0; i < surface_list.length; i++) {
                  $('.js-surface-list-tbody').prepend(
                    '<tr>' +
                    '<td>' + surface_list[i]['id'] + '</td>' +
                    '<td>' + surface_list[i]['area'] + '</td>' +
                    '<td><a href="/city/surface/' + surface_list[i]['surface_id'] + '">' + surface_list[i]['surface'] + '</a></td>' +
                    '<td>' + surface_list[i]['date_start'] + '</td>' +
                    '<td>' + surface_list[i]['date_end'] + '</td>' +
                    '<td>' +
                      '<form action="/client/surface-remove/" method="post" class="js-remove-client-surface" role="form">' +
                      '<input type="hidden" name="client_surface_id" value="' + surface_list[i]['id'] + '">' +
                      '<button type="submit" class="btn btn-warning"><span class="glyphicon glyphicon-remove"></span> Удалить</button>' +
                      '</form>' +
                    '</td>' +
                    '</tr>'
                  );
                }
                //hz
                removeClientSurface();
              //  hz

              }
            } else {
              $.notify(data.error, 'error');
            }

          }
      });
    }
  });


    // валидация формы добвления клиента к поверхности
  $( '#js-surface-add-client-form' ).validate({
    rules: {
      client: {
        required: true
      },
      date_start: {
        required: true
      }
    }
  });

  // валидация формы добвления клиента к поверхности
  $('#js-client-add-maket-form').validate({
    rules: {
      name: {
        required: true
      },
      file: {
        required: true
      },
      date: {
        required: true
      }
    }
  });
  // валидация формы добавления задачи по клиенту
  $('#js-adjuster-client_task-add-form').validate({
    rules: {
      adjuster: {
        required: true
      },
      surface: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      },
      client: {
        required: true
      }
    }
  });
  var adjuster_ctask_aform = $('#js-adjuster-client_task-add-form');
  adjuster_ctask_aform.find('#id_client').change(function(){
    $('.js-task-surface-list tr.result').remove();
    console.log($(this).val())
    $.ajax({
      type: "GET",
      url: adjuster_ctask_aform.data('client-ajax-url'),
      data: {
        adjster: adjuster_ctask_aform.find('#id_adjuster').val(),
        client: $(this).val()
      }
    }).done(function( data ) {
      if (data.surface_list) {
        var surface_list = data.surface_list;
        console.log(surface_list);

        var surface_table = $('.js-task-surface-list');
        console.log(surface_table)
        for (var i = 0; i < surface_list.length; i++){
          surface_table.append(
            '<tr class="result">'+
            '<td><input type="checkbox" name="chk_group[]" value="' +surface_list[i]['id'] +'"></td>'+
            '<td>'+surface_list[i]['id']+'</td>'+
            '<td>'+surface_list[i]['area']+'</td>'+
            '<td>'+surface_list[i]['street']+'</td>'+
            '<td>'+surface_list[i]['number']+'</td>'+
            '</tr>'
          )
        }
      }
    });
  });
  // валидация формы редактирования задачи по клиенту
  $('#js-adjuster-client_task-udate-form').validate({
    rules: {
      adjuster: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      }
    }
  });

  // валидация формы добавления задачи по району
  $('#js-adjuster-task-add-form').validate({
    rules: {
      adjuster: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      },
      area: {
        required: true
      }
    }
  });
  var adjuster_task_form = $('#js-adjuster-task-add-form');
  adjuster_task_form.find('#id_area').change(function(){
    $('.js-task-surface-second-list tr.result').remove();
    console.log($(this).val())
    $.ajax({
      type: "GET",
      url: adjuster_task_form.data('area-ajax-url'),
      data: {
        area: $(this).val()
      }
    }).done(function( data ) {
      if (data.surface_list) {
        var surface_list = data.surface_list;
        console.log(surface_list);

        var surface_table = $('.js-task-surface-second-list');
        console.log(surface_table)
        for (var i = 0; i < surface_list.length; i++){
          surface_table.append(
            '<tr class="result">'+
            '<td><input type="checkbox" name="chk_group_1[]" value="' +surface_list[i]['id'] +'"></td>'+
            '<td>'+surface_list[i]['id']+'</td>'+
            '<td>'+surface_list[i]['street']+'</td>'+
            '<td>'+surface_list[i]['number']+'</td>'+
            '</tr>'
          )
        }
      }
    });
  });



});