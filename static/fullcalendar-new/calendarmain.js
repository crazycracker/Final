/**
 * Created by vinay raj on 4/22/2017.
 */
$(document).ready(function () {
    /*
     date store today date.
     d store today date.
     m store current month.
     y store current year.
     */
    "use strict";
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();
    var deleteEvent;
    /*
     Initialize fullCalendar and store into variable.
     Why in variable?
     Because doing so we can use it inside other function.
     In order to modify its option later.
     */
    var startTime, endTime, room_number, block, set, unset;
    set = '1';
    unset = '0';


    var x = document.getElementById("myInput").value;
    var x1 = document.getElementById("myInput1").value;
    var x2 = document.getElementById("myInput2").value;
    room_number = $('#roomnumber').text();
    block = $('#blockname').text();
    $('#squarespaceModal').find("#room_number").val(room_number);
    $('#squarespaceModal').find("#block_name").val(block);
    $('#squarespaceModal').find("#sender").val(x);
    $('#squarespaceModal').find("#sender_id").val(x1);
    document.getElementById("block_name").readOnly = true;
    document.getElementById("sender").readOnly = true;
    document.getElementById("room_number").readOnly = true;
    document.getElementById("sender_id").readOnly = true;
    document.getElementById("startDateTime").readOnly = true;
    document.getElementById("endDateTime").readOnly = true;

    function isOverlapping(eventStartDay, eventEndDay) {
        var events = $('#calendar').fullCalendar('clientEvents');

        for (var i in events) {
            if (events[i].booking_status == set || events[i].entry_timetable == true) {
                if (eventStartDay > events[i].start && eventStartDay < events[i].end) {
                    return true;
                }
                //end-time in between any of the events
                if (eventEndDay > events[i].start && eventEndDay < events[i].end) {
                    return true;
                }
                //any of the events in between/on the start-time and end-time
                if (eventStartDay <= events[i].start && eventEndDay >= events[i].end) {
                    return true;
                }
            }
        }
        return false;
    }

    function getDate(d) {
        return (d.getDate() + '-' + (d.getMonth() + 1) + '-' + d.getFullYear());
    }

    var calendar = $('#calendar').fullCalendar(
        {
            /*
             header option will define our calendar header.
             left define what will be at left position in calendar
             center define what will be at center position in calendar
             right define what will be at right position in calendar
             */
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay,listMonth'
            },
            /*
             defaultView option used to define which view to show by default,
             for example we have used agendaWeek.
             */
            defaultView: 'agendaWeek',
            /*
             selectable:true will enable user to select datetime slot
             selectHelper will add helpers for selectable.
             */
            selectable: true,
            selectHelper: true,
            /*
             when user select timeslot this option code will execute.
             It has three arguments. Start,end and allDay.
             Start means starting time of event.
             End means ending time of event.
             allDay means if events is for entire day or not.
             */
            eventDurationEditable: false,
            eventStartEditable: false,
            select: function (start, end, allDay) {
                /*
                 if title is enterd calendar will add title and event into fullCalendar.
                 */

                var check = new Date(start);
                var today = new Date();
                check = formatDate(check);
                today = formatDate(today);

                if (check < today) {
                    bootbox.alert({
                        message: "You cannot do this",
                        className: 'bb-alternate-modal'
                    });
                } else {
                    startTime = convert(start);
                    endTime = convert(end);
                    if (isOverlapping(start, end)) {
                        bootbox.alert({
                            message: "Slot is not Available",
                            className: 'bb-alternate-modal'
                        });
                    } else {
                        $('#squarespaceModal').find('#description').val('');
                        $('#squarespaceModal').find("#startDateTime").val(startTime);
                        $('#squarespaceModal').find("#endDateTime").val(endTime);
                        $('#squarespaceModal').modal({
                            show: true
                        });
                    }

                    calendar.fullCalendar('unselect');
                }
            },
            /*
             editable: true allow user to edit events.
             */
            currentTimezone: 'Asia/Kolkata',
            editable: true,
            allDaySlot: false,
            eventLimit: true,
            /*
             events is the main option for calendar.
             for demo we have added predefined events in json object.
             */
            events: function (start, end, timezone, callback) {
                start = new Date(start);
                end = new Date(end);
                $.ajax({
                    url: "/eventlist",
                    type: 'Get',
                    data: "start=" + Math.round(start.getTime() / 1000) + "&end=" + Math.round(end.getTime() / 1000) + "&rm=" + room_number + "&_rand=" + Math.floor(Math.random() * 100),
                    datatype: "json",
                    contentType: "application/json",
                    success: function (data) {
                        if (callback) {
                            callback(data);
                        } else {
                            console.log("callback is not defined");
                        }
                    }
                });
            },
            eventClick: function (event) {
                var start = convert(event.start._d);
                start = start.toString().split(" ");
                var end = convert(event.end._d);
                end = end.toString().split(" ");
                $('#modalTitle').html(event.title);
                deleteEvent = event;
                if (event.sender)
                    $('#modalBody').html(event.sender + " " + event.sender_id);
                else
                    $('#modalBody').html(start[1] + " " + end[1] + " " + event.lecturer);
                $('#fullCalModal').modal();
            },
            eventRender: function (event, element) {
                if (x2 == 'faculty' && event.sender_id == x1) {
                    event.booking_status = set;
                }
                console.log(event.sender_id + " " + event.booking_status + " " + x + " " + x1);

                if (event.entry_timetable == true) {
                    element.children('.fc-bg').css({'background-color': 'blue'});
                    element.children('.fc-event-inner').css({'border-color': 'black'});
                    element.children('.fc-event-inner').css({'color': 'red'});
                }
                if (event.booking_status === set) {
                    element.children('.fc-bg').css({'background-color': 'green'});
                    element.children('.fc-event-inner').css({'border-color': 'black'});
                    element.children('.fc-event-inner').css({'color': 'red'});
                }
            }
        });

    $('#saveEvent').on('click', function (e) {
        // We don't want this to act as a link so cancel the link action
        e.preventDefault();
        doSubmit();
    });

    $('#delete').on('click', function (e) {
        var start = formatDate(deleteEvent.start._d);
        var today = formatDate(date);
        console.log(deleteEvent);
        if (start >= today) {
            $.ajax({
                url: "/deleteEvents",
                type: 'Get',
                data: "id=" + deleteEvent.event_id + "&sender_id=" + deleteEvent.sender_id,
                datatype: "json",
                contentType: "application/json",
                success: function (data) {
                    if(data == 'success'){
                        $('#calendar').fullCalendar('removeEvents', deleteEvent._id);
                    }
                }
            });
        }
    });
    function formatDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2) {
            month = '0' + month;
        }
        if (day.length < 2) {
            day = '0' + day;
        }

        return [year, month, day].join('-');
    }

    function convert(str) {
        var mnths = {
                Jan: "01", Feb: "02", Mar: "03", Apr: "04", May: "05", Jun: "06",
                Jul: "07", Aug: "08", Sep: "09", Oct: "10", Nov: "11", Dec: "12"
            },
            date = str.toString().split(" ");

        return ([date[3], mnths[date[1]], date[2]].join("-") + " " + date[4]);
    }

    function doSubmit() {

        console.log("this ");
        var title = $('#squarespaceModal').find('#description').val(), granter, reserved_by;

        granter = $("#squarespaceModal").find("#granter").val();

        reserved_by = $("#squarespaceModal").find("#reserved_by").val();
        startTime = $('#squarespaceModal').find("#startDateTime").val();
        endTime = $('#squarespaceModal').find("#endDateTime").val();
        if (x2 == "student") {
            console.log("student " + granter);
            $("#calendar").fullCalendar('renderEvent',
                {
                    title: $('#squarespaceModal').find('#description').val(),
                    start: startTime,
                    end: endTime,
                    allDay: false,
                    overlap: false,
                    editable: false
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
                "booking_status": unset,
                "block": block,
                "description": title,
                "startDateTime": startTime,
                "endDateTime": endTime,
                "room_number": room_number,
                "granter": granter,
                "sender": x,
                "sender_id": x1
            };
            console.log(data);
            $.ajax({
                url: '/saveEvents',
                data: data,
                type: "POST",
                success: function (json) {
                    $("#squarespaceModal").modal('hide');
                }
            });
        }
        else {
            $("#calendar").fullCalendar('renderEvent',
                {
                    title: $('#squarespaceModal').find('#description').val(),
                    start: startTime,
                    end: endTime,
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
                "booking_status": set,
                "block": block,
                "description": title,
                "startDateTime": startTime,
                "endDateTime": endTime,
                "room_number": room_number,
                "sender": x,
                "sender_id": x1
            };
            $.ajax({
                url: '/saveEvents',
                data: data,
                type: "POST",
                success: function (json) {
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
        // these HTTP methods do not require CSRF protection
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
