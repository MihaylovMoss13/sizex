(function() {
    $(document).on('click', '.change-resolution', function (ev) {
      $.get($(ev.target).data('url'), function () {
        location.reload()
      })
    })

    $('select').niceSelect();

    // Related links
    $(function() {
        var links = $('.rp-link-list>li'),
            moreBtn = $('.rp-related-links__more-button'),
            hidedLinks;

        links.each(function(index, el) {
            if (index > 17) {
                $(el).addClass('_hided');
            }
        });

        if (links.length > 18) {
            moreBtn.show();
        } else {
            moreBtn.hide();
        }

        moreBtn.click(function(e) {
            e.preventDefault();

            $(this).hide();
            $(this).closest('.rp-related-links').addClass('_showed');
            $('.rp-link-list>li._hided').removeClass('_hided');
        });
    });

    // Detect ios
    if (navigator.userAgent.match(/(iPod|iPhone|iPad)/)) {
        $('body').addClass('is-ios-browser');
    }

    // Feedback
    $.fn.serializeObject = function() { var o = {}; var a = this.serializeArray(); $.each(a, function() { if (o[this.name] !== undefined) { if (!o[this.name].push) { o[this.name] = [o[this.name]]; } o[this.name].push(this.value || ''); } else { o[this.name] = this.value || ''; } }); return o; };

    var Model = Backbone.Model.extend({
        url: '/feedback/',
    });

    var View = Backbone.View.extend({
        initialize: function() {
            this.$el.validate();
        },

        el: $('body'),

        events: {
            'submit': 'submit',
        },

        submit: function(ev) {
          ev.preventDefault();
          if ($(ev.target).valid()) {
            var data = $(ev.target).serializeObject();
            var model = new Model(data);
            model.save()
                .done(function(data) {
                    if (data.success) {
                        $(ev.target)[0].reset();
                        swal({
                            title: "Форма отправлена!", 
                            text: "Мы свяжемся с Вами в ближайшее время", 
                            confirmButtonColor: "#1ab394",
                            type: "success"
                        });
                        UIkit.modal('#feedback-modal').hide();
                    } else 
                        swal({
                            title: "Ошибка при заполнении формы", 
                            confirmButtonColor: "#1ab394",
                            type: "error"
                        });
                })
                .fail(function() {
                    swal({
                        title: "Ошибка при отправке формы", 
                        confirmButtonColor: "#1ab394",
                        type: "error"
                    });
                });
          }
        },
    });

    new View({el: '.feedback'});
    new View({el: '.feedback_modal'});

    // Calculator

    var Calculator = Backbone.View.extend({
        initialize: function() {
            $('form#calculator').validate({
                ignore: [],
                errorPlacement: function(error, element) {         
                error.insertBefore(element);
                }
            });
        },

        prices: {
            polyplast: [499, 469, 434, 399, 379, 339],
            pongs: [599, 569, 534, 499, 479, 439],
            descor: [959, 929, 894, 859, 839, 799],
        },

        el: $('body'),

        events: {
            'submit #calculator': 'submit', 
        },

        submit: function(ev) {
            ev.preventDefault();
            var data = $(ev.target).serializeObject();

            calc_area = Number(data.calc_long) * Number(data.calc_width);				// площадь
            perimeter = 2 * Number(data.calc_long) + 2 * Number(data.calc_width);		// периметр
            
            // получим цену полотна в зависимости от площади
            
            switch (true) {
                case (calc_area < 20):
                    price = this.prices[data.material][0]
                    break;
                case (calc_area < 30):
                    price = this.prices[data.material][1]
                    break;
                case (calc_area < 40):
                    price = this.prices[data.material][2]
                    break;
                case (calc_area < 50):
                    price = this.prices[data.material][3]
                    break;
                case (calc_area < 100):
                    price = this.prices[data.material][4]
                    break;
                default:
                    price = this.prices[data.material][5]
                    break;
            }

            shape_price = 50;
            lamps_price = 400;
            lightings_price = 480;
            pipes_price = 200;
            corners_price = 140;
            tape_price = 100;
            tape_total = 0;		// итоговая стоимость ленты
            if ( data.calc_tape ) tape_total = tape_price * perimeter;
            
            total = price * calc_area + shape_price * perimeter + Number(data.calc_lamps) * lamps_price + Number(data.calc_lightings) * lightings_price + Number(data.calc_pipes) * pipes_price + Math.max(0, Number(data.calc_corners) - 4) * corners_price + tape_total;
            discount = total - 0.1 * total;
            $('#total').html(total.toLocaleString());
            $('#discount').html(discount.toLocaleString());
            $('.result').slideDown();
        }
    });

    new Calculator();
})();
