/**
 * Created by vinay raj on 4/24/2017.
 */
/**
 * Created by vinay raj on 4/10/2017.
 */
$(document).ready(function () {
    "use strict";
    var x = document.getElementById('rowId').value;
    console.log(x);
    var eventDate;
    eventDate = document.getElementById('date').value;
    eventDate = eventDate.toString().split(' ');
    console.log(eventDate);
    var calendar = $('#calendar').fullCalendar(
        {
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            defaultView: 'agendaWeek',
            defaultDate: eventDate[0],
            overlap:false,
            editable: false,
            allDaySlot: true,
            eventLimit: true,
            events: function (start, end, timezone, callback) {
                $.ajax({
                    url: "/getEvents",
                    type: 'Get',
                    data: "id=" + x,
                    datatype: "json",
                    contentType: "application/json",
                    success: function (data) {
                        var eventsToShow = [];
                        for (var i = 0; i < data.length; i++) {
                            eventsToShow.push(data[i]);
                        }
                        if (callback) {
                            console.log(eventsToShow);
                            callback(eventsToShow);
                        } else {
                            console.log("callback is not defined");
                        }
                    }
                });
            },
            eventRender: function (event, element) {
                if (event.booking_status == '1') {
                    element.children('.fc-event-inner').css({'background-color': 'green'});
                    element.children('.fc-event-inner').css({'border-color': 'black'});
                    element.children('.fc-event-inner').css({'color': 'red'});
                }
            }
        });


    function convert(str) {
        var mnths = {
                Jan: "01", Feb: "02", Mar: "03", Apr: "04", May: "05", Jun: "06",
                Jul: "07", Aug: "08", Sep: "09", Oct: "10", Nov: "11", Dec: "12"
            },
            date = str.toString().split(" ");

        return ([date[3], mnths[date[1]], date[2]].join("-") + " " + date[4]);
    }
});
