$(document).ready(function() {

  $('#id_cantidad').attr('placeholder', 'Cantidad de productos a agregar');

  var select = document.querySelector('select[name="categoria"]');
    if (select) {
      var defaultOption = select.querySelector('option[value=""]');
      if (defaultOption) {
          defaultOption.text = "Seleccione una categoría";
      }
  }

  var select = document.querySelector('select[name="producto"]');
  if (select) {
      var defaultOption = select.querySelector('option[value=""]');
      if (defaultOption) {
          defaultOption.text = "Seleccione un producto";
      }
  }

  $('#form').validate({ 
    rules: {
        'categoria': {
            required: true,
            min: 1,
        },
        'producto': {
            required: true,
            min: 1,
        },
        'cantidad': {
            required: true,
            digits: true,
            number: true,
            min: 1
        },
    },
    messages: {
        'categoria': {
            required: 'Debe seleccionar la categoría del producto',
            min: 'Debe seleccionar la categoría del producto',
        },
        'producto': {
            required: 'Debe seleccionar el nombre del producto',
            min: 'Debe seleccionar el nombre del producto',
        },
        'cantidad': {
            required: 'Debe ingresar la cantidad',
            number: 'Debe ingresar un número',
            digits: 'Debe ingresar un número entero',
            min: 'Debe ingresar un número mayor que cero',
        },
    },
    errorPlacement: function(error, element) {
        error.insertAfter(element); 
        error.addClass('error-message'); 
    },
  });

  var sin_imagen = '/static/core/img/sin-imagen.png';


  $("#id_categoria").change(function() {
    var categoriaId = $(this).val();
    if (categoriaId) {
      $.ajax({
        url: $('#url_obtener_productos').val(),
        data: {
          'categoria_id': categoriaId
        },
        dataType: 'json',
        success: function(data) {
          $("#id_producto").empty();
          $('#cuadro-imagen').attr('src', sin_imagen);
          if (data.length === 0) {
            $("#id_producto").append(`<option value="-1" data-imagen="${sin_imagen}">No hay productos disponibles</option>`);
          } else {
            $("#id_producto").append(`<option value="-1" selected="" data-imagen="${sin_imagen}">Seleccione un producto</option>`);
            $.each(data, function(key, value) {
              $("#id_producto").append(`<option value="${value.id}" data-imagen="${value.imagen}"> ${value.nombre} </option>`);
            });
          }
          $("#id_producto").prop('disabled', false);
        }
      });
    } else {
      $("#id_producto").empty();
      $("#id_producto").prop('disabled', true);
    }
  });


  $("#id_producto").change(function() {
    var opcionSeleccionada = $(this).find(':selected');
    var imagen = opcionSeleccionada.data('imagen');
    $('#cuadro-imagen').attr('src', imagen);
  });

});
