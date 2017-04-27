/**
 * Created by vinay raj on 4/13/2017.
 */
$(document).ready(function () {

    "use strict";
    var room_number = $('#roomnumber').text(), day, eventData;
    $('#squarespaceModal').find("#room_number").val(room_number);
    document.getElementById("room_number").readOnly = true;
    document.getElementById("startDateTime").readOnly = true;
    document.getElementById("endDateTime").readOnly = true;

    var calendar = $('#calendar').fullCalendar(
        {
            header: {
                center: '',
                right: '',
                left: ''
            },
            defaultView: 'agendaWeek',
            columnFormat: 'dddd',
            slotDuration: '00:15:00',
            minTime: "09:00:00",
            maxTime: "19:00:00",
            selectable: true,
            selectHelper: true,
            select: function (start, end) {
                var startTime, endTime;
                startTime = convert(start);
                endTime = convert(end);
                $('#squarespaceModal').find("#startDateTime").val(startTime);
                $('#squarespaceModal').find("#endDateTime").val(endTime);
                $('#squarespaceModal').find('#dow').val(day);
                $('#squarespaceModal').modal({
                    show: true
                });
                console.log(day);
                calendar.fullCalendar('unselect');

            },

            currentTimezone: 'Asia/Kolkata',
            editable: true,
            allDaySlot: false,
            eventLimit: true,
            events: function (start, end,timezone, callback) {
                $.ajax({
                    url: "/timeTableEvents",
                    type: 'Get',
                    data: "&rm=" + room_number + "&_rand=" + Math.floor(Math.random() * 100),
                    datatype: "json",
                    contentType: "application/json",
                    success: function (data) {
                        if (callback) {
                            console.log(data);
                            callback(data);
                        } else {
                            console.log("callback is not defined");
                        }
                    }
                });
            }
        });
    $('#saveEvent').on('click', function (e) {
        // We don't want this to act as a link so cancel the link action
        e.preventDefault();
        doSubmit();
    });
    function convert(str) {
        var mnths = {
                Jan: "01", Feb: "02", Mar: "03", Apr: "04", May: "05", Jun: "06",
                Jul: "07", Aug: "08", Sep: "09", Oct: "10", Nov: "11", Dec: "12"
            },
            date = str.toString().split(" ");
        day = getDayOfWeek([date[3], mnths[date[1]], date[2]].join("-"));
        console.log('reached here too');
        return (date[4]);
    }

    function getDayOfWeek(date) {
        var dayOfWeek = new Date(date).getDay();
        return dayOfWeek;
    }

    function doSubmit() {
        var startTime, endTime, course, lecturer;
        course = $("#squarespaceModal").find("#course").val();
        lecturer = $("#squarespaceModal").find("#lecturer option:selected").val();
        startTime = $('#squarespaceModal').find("#startDateTime").val();
        endTime = $('#squarespaceModal').find("#endDateTime").val();
        if (course) {
            $("#calendar").fullCalendar('renderEvent',
                {
                    title: $('#squarespaceModal').find('#course').val(),
                    start: startTime,
                    end: endTime,
                    lecturer: lecturer,
                    dow:[day],
                    allDay: false,
                    overlap: false
                },
                false
            );
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
            var today = new Date();
            var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
            var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            var dateTime = date + ' ' + time;
            var data = {
                "startTime": startTime,
                "endTime": endTime,
                "room_number": room_number,
                "lecturer": lecturer,
                "course": course,
                "dayOfWeek": day
            };
            console.log(data);
            $.ajax({
                url: '/saveTimeTableEvents',
                data: data,
                type: "POST",
                success: function (json) {
                    console.log(json);
                    $("#squarespaceModal").modal('hide');
                }
            });
        }
    }

    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

