var socket = io();

socket.on("stats", (data) => {

    $.each(jQuery.parseJSON(data), (key, value) => {

        let selector_start = "#" + value["sensor_id"];

        $(selector_start + "_timestamp").text(value["timestamp"]);
        $(selector_start + "_measurements").text(value["measurements"]);
        $(selector_start + "_relative_humidity").text(value["relative_humidity"]);
        $(selector_start + "_average_humidity").text(value["average_humidity"]);
        $(selector_start + "_min_humidity").text(value["min_humidity"]);
        $(selector_start + "_max_humidity").text(value["max_humidity"]);
        $(selector_start + "_relative_temperature").text(value["relative_temperature"]);
        $(selector_start + "_average_temperature").text(value["average_temperature"]);
        $(selector_start + "_min_temperature").text(value["min_temperature"]);
        $(selector_start + "_max_temperature").text(value["max_temperature"]);
        $(selector_start + "_relative_brightness").text(value["relative_brightness"]);
        $(selector_start + "_average_brightness").text(value["average_brightness"]);
        $(selector_start + "_min_brightness").text(value["min_brightness"]);
        $(selector_start + "_max_brightness").text(value["max_brightness"]);
    });
});