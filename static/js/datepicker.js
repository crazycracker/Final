/**
 * Created by vinay raj on 3/22/2017.
 */

$(function () {
    $('#calendar').datepicker({
                inline: true,
                firstDay: 1,
                showOtherMonths: true,
                dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            });
    $( "#datepicker" ).datepicker();
    var settings = {
        rows: 5,
        cols: 15,
        rowCssPrefix: 'row-',
        colCssPrefix: 'col-',
        seatWidth:35,
        seatHeight:35,
        seatCss: 'seat',
        selectedSeatCss: 'selectedSeat',
        selectingSeatCss: 'selectingSeat'
    };

    var init = function (reservedSeat) {
        var str = [], seatNo, className;
        for (i = 0; i < settings.rows; i++) {
            for (j = 0; j < settings.cols; j++) {
                seatNo = (i + j * settings.rows + 1);
                className = settings.seatCss + ' ' + settings.rowCssPrefix + i.toString() + ' ' + settings.colCssPrefix + j.toString();
                if ($.isArray(reservedSeat) && $.inArray(seatNo, reservedSeat) != -1) {
                    className += ' ' + settings.selectedSeatCss;
                }
                str.push('<li class="' + className + '"' +
                          'style="top:' + (i * settings.seatHeight).toString() + 'px;left:' + (j * settings.seatWidth).toString() + 'px">' +
                          '<a title="' + seatNo + '">' + seatNo + '</a>' +
                          '</li>');
            }
        }
        $('#place').html(str.join(''));
    };

    //case I: Show from starting
    //init();

    //Case II: If already booked
    var bookedSeats = [5, 10, 25];
    init(bookedSeats);


    $('.' + settings.seatCss).click(function () {
    if ($(this).hasClass(settings.selectedSeatCss)){
        alert('This seat is already reserved');
    }
    else{
        $(this).toggleClass(settings.selectingSeatCss);
        }
    });

    $('#btnShow').click(function () {
        var str = [];
        $.each($('#place').find('li.' + settings.selectedSeatCss + ' a, #place li.'+ settings.selectingSeatCss + ' a'), function (index, value) {
            str.push($(this).attr('title'));
        });
        alert(str.join(','));
    });

    $('#btnShowNew').click(function () {
        var str = [], item;
        $.each($('#place').find('li.' + settings.selectingSeatCss + ' a'), function (index, value) {
            item = $(this).attr('title');
            str.push(item);
        });
        alert(str.join(','));
    })
});
