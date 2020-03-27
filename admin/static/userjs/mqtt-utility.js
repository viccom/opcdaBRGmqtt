/*******************************************************************************
 * Copyright (c) 2015 IBM Corp.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * and Eclipse Distribution License v1.0 which accompany this distribution.
 *
 * The Eclipse Public License is available at
 *    http://www.eclipse.org/legal/epl-v10.html
 * and the Eclipse Distribution License is available at
 *   http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * Contributors:
 *    James Sutton - Initial Contribution
 *******************************************************************************/

/*
Eclipse Paho MQTT-JS Utility
This utility can be used to test the Eclipse Paho MQTT Javascript client.
*/

// Create a client instance
mqtt_client =null;
mqttc_connected = false;
var current_opcconfig = new Object();
var mqtt_host = window.location.hostname;
var mqtt_port = 3884;
var received_logs_num = 0;


/**
 *	临时兼容IE，去掉可变参数
 */
function logMessage(type, content) {
    if (type === "INFO") {
        console.info(content);
    } else if (type === "ERROR") {
        console.error(content);
    } else {
        console.log(content);
    }
}

/**
 *	日志处理
 */
// function logMessage(type, ...content) {
//     if (type === "INFO") {
//         console.info(...content);
//     } else if (type === "ERROR") {
//         console.error(...content);
//     } else {
//         console.log(...content);
//     }
// }

function isEmpty(obj){
    if(typeof obj == "undefined" || obj == null || obj == ""){
        return true;
    }else{
        return false;
    }
}

function isInteger(obj) {
    return obj%1 === 0
}

function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 8; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

// logMessage("INFO", "Starting Eclipse Paho JavaScript Utility.");

// Things to do as soon as the page loads
// document.getElementById("clientIdInput").value = "js-utility-" + makeid();

var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var base64DecodeChars = new Array(
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,
    -1,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,
    -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);

function base64encode(str) {
    var out, i, len;
    var c1, c2, c3;

    len = str.length;
    i = 0;
    out = "";
    while(i < len) {
        c1 = str.charCodeAt(i++) & 0xff;
        if(i == len)
        {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt((c1 & 0x3) << 4);
            out += "==";
            break;
        }
        c2 = str.charCodeAt(i++);
        if(i == len)
        {
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
            out += base64EncodeChars.charAt((c2 & 0xF) << 2);
            out += "=";
            break;
        }
        c3 = str.charCodeAt(i++);
        out += base64EncodeChars.charAt(c1 >> 2);
        out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
        out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6));
        out += base64EncodeChars.charAt(c3 & 0x3F);
    }
    return out;
}

function base64decode(str) {
    var c1, c2, c3, c4;
    var i, len, out;

    len = str.length;
    i = 0;
    out = "";
    while(i < len) {
        /* c1 */
        do {
            c1 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
        } while(i < len && c1 == -1);
        if(c1 == -1)
            break;

        /* c2 */
        do {
            c2 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
        } while(i < len && c2 == -1);
        if(c2 == -1)
            break;

        out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));

        /* c3 */
        do {
            c3 = str.charCodeAt(i++) & 0xff;
            if(c3 == 61)
                return out;
            c3 = base64DecodeChars[c3];
        } while(i < len && c3 == -1);
        if(c3 == -1)
            break;

        out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));

        /* c4 */
        do {
            c4 = str.charCodeAt(i++) & 0xff;
            if(c4 == 61)
                return out;
            c4 = base64DecodeChars[c4];
        } while(i < len && c4 == -1);
        if(c4 == -1)
            break;
        out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
    }
    return out;
}

function utf16to8(str) {
    var out, i, len, c;

    out = "";
    len = str.length;
    for(i = 0; i < len; i++) {
        c = str.charCodeAt(i);
        if ((c >= 0x0001) && (c <= 0x007F)) {
            out += str.charAt(i);
        } else if (c > 0x07FF) {
            out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
            out += String.fromCharCode(0x80 | ((c >>  6) & 0x3F));
            out += String.fromCharCode(0x80 | ((c >>  0) & 0x3F));
        } else {
            out += String.fromCharCode(0xC0 | ((c >>  6) & 0x1F));
            out += String.fromCharCode(0x80 | ((c >>  0) & 0x3F));
        }
    }
    return out;
}

function utf8to16(str) {
    var out, i, len, c;
    var char2, char3;

    out = "";
    len = str.length;
    i = 0;
    while(i < len) {
        c = str.charCodeAt(i++);
        switch(c >> 4)
        {
            case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
            // 0xxxxxxx
            out += str.charAt(i-1);
            break;
            case 12: case 13:
            // 110x xxxx   10xx xxxx
            char2 = str.charCodeAt(i++);
            out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
            break;
            case 14:
                // 1110 xxxx  10xx xxxx  10xx xxxx
                char2 = str.charCodeAt(i++);
                char3 = str.charCodeAt(i++);
                out += String.fromCharCode(((c & 0x0F) << 12) |
                    ((char2 & 0x3F) << 6) |
                    ((char3 & 0x3F) << 0));
                break;
        }
    }

    return out;
}

function CharToHex(str) {
    var out, i, len, c, h;

    out = "";
    len = str.length;
    i = 0;
    while(i < len)
    {
        c = str.charCodeAt(i++);
        h = c.toString(16);
        if(h.length < 2)
            h = "0" + h;
        out += h + " ";
        /*                out += "\\x" + h + " ";
                        if(i > 0 && i % 8 == 0)
                            out += "\r\n";*/
    }

    return out;
}


// called when the client connects
function onConnect(context) {
  // Once a connection has been made, make a subscription and send a message.
  var connectionString = context.invocationContext.host + ":" + context.invocationContext.port + context.invocationContext.path;
  console.log("Connection Success ", "URI: ", connectionString, ", ID: ", context.invocationContext.clientId);
  // logMessage("INFO", "Connection Success ", "[URI: ", connectionString, ", ID: ", context.invocationContext.clientId, "]");
  // var statusSpan = document.getElementById("connectionStatus");
  // statusSpan.innerHTML = "Connected to: " + connectionString + " as " + context.invocationContext.clientId;
  mqttc_connected = true;

}


function onConnected(reconnect=true, uri) {
  // Once a connection has been made, make a subscription and send a message.
  //   logMessage("INFO", "Client Has now connected: [Reconnected: ", reconnect, ", URI: ", uri, "]");
    console.log("Client Has now connected. Reconnected: ", reconnect, ", URI: ", uri);
    mqttc_connected = true;
    mqtt_client.subscribe(['v1/opcdabrg/api/RESULT','v1/opcdabrg/OPCDABRG_STATUS/#',  'v1/opcdabrg/OPCDABRG_DATAS/#', 'v1/opcdabrg/OPCDABRG_LOGS/#']);
    var message = new Paho.Message(JSON.stringify({"id":'getConfig/' + $("#newClientID").val() + '/' + Date.parse(new Date()).toString()}));
    message.destinationName = 'v1/opcdabrg/api/getConfig';
    message.qos = 0;
    mqtt_client.send(message);

}

function onFail(context) {
    console.log("Failed to connect. [Error Message: ", context.errorMessage);
  // logMessage("ERROR", "Failed to connect. [Error Message: ", context.errorMessage, "]");
  // var statusSpan = document.getElementById("connectionStatus");
  // statusSpan.innerHTML = "Failed to connect: " + context.errorMessage;
  mqttc_connected = false;
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
      console.log("Connection Lost. Error Message: ", responseObject.errorMessage);
    // logMessage("INFO", "Connection Lost. [Error Message: ", responseObject.errorMessage, "]");
  }
  mqttc_connected = false;
}

// called when a message arrives
function onMessageArrived(message) {
    // console.log("topic: ",message.destinationName);
    var arr_topic = message.destinationName.split("/");
    // console.log(arr_topic[3]);
    // logMessage("INFO", "Message Recieved: [Topic: ", message.destinationName, ", Payload: ", message.payloadString, ", QoS: ", message.qos, ", Retained: ", message.retained, ", Duplicate: ", message.duplicate, "]");
    if(arr_topic[2]==="OPCDABRG_STATUS"){
        // console.log(message.payloadString);
        var status_message = JSON.parse(message.payloadString);
        $(".OPCServerStatus").text(status_message[2]);
        if(status_message[2]=="online"){
            $(".OPCServerStatus").addClass('label-success')
        }else{
            $(".OPCServerStatus").removeClass('label-success')
        }
    }

    if(arr_topic[2]==="OPCDABRG_LOGS"){
        console.log(message.payloadString);
        var log_message = JSON.parse(message.payloadString);
        // console.log(log_message);
        var local_datetime = new Date(parseInt(log_message[0]) * 1000).toLocaleString('chinese', { hour12: false });
        // console.log(bj_datetime)
        var new_log_message = [local_datetime, log_message[1], log_message[2]];
        log_table.row.add(new_log_message).draw();
    }
    if(arr_topic[2]==="OPCDABRG_DATAS") {
        // console.log(message.payloadString);
        var data_message = JSON.parse(message.payloadString);
        var opcdata = new Array() ;
        if(data_message.length>0){
            $.each(data_message, function (i, v) {
                var html_str = '<button type=\"button\" class=\"btn btn-default writeItem\" data-toggle=\"modal\" data-target=\"#writeItemModal\" data-id=\"' + v[0] + '\">下置</button>';
                // var local_datetime = new Date(parseInt(1585298533.4069197).toLocaleString('chinese', { hour12: false }));
                var local_datetime = new Date(parseInt(v.slice(-1) * 1000)).toLocaleString('chinese', { hour12: false });
                // console.log(local_datetime);
                v.pop();
                v.push(local_datetime, html_str);
                opcdata.push(v)
            });
        }
        //var opcdata = data_message;
        var currentPage = data_table.page();
        // console.log(currentPage);
        data_table.clear();
        data_table.rows.add(opcdata).draw(false);
        data_table.page(currentPage).draw(false);

    }
    if(arr_topic[3]==="RESULT"){
        // console.log(message.payloadString);
        var apiResult_message = JSON.parse(message.payloadString);
        if(apiResult_message.result){
            var local_datetime = new Date(parseInt(new Date().getTime())).toLocaleString('chinese', { hour12: false });
            var max_str = JSON.stringify(apiResult_message.data);
            if(JSON.stringify(apiResult_message.data).length > 64){
                max_str = JSON.stringify(apiResult_message.data).slice(0,64) + ' ...';
            }
            var new_log_message = [local_datetime, 'api', apiResult_message['id'] + ":" + max_str];
            if(apiResult_message['id'].indexOf("getConfig") != -1 ){
                // console.log(received_logs_num/60, isInteger(received_logs_num/60), apiResult_message);
                if(isInteger(received_logs_num/60)){
                    log_table.row.add(new_log_message).draw();
                }
                received_logs_num = received_logs_num + 1;
            }else{
                log_table.row.add(new_log_message).draw();
            }

        }else{
            var local_datetime = new Date(parseInt(new Date().getTime())).toLocaleString('chinese', { hour12: false });
            var max_str = JSON.stringify(apiResult_message.error);
            if(JSON.stringify(apiResult_message.error).length > 64){
                max_str = JSON.stringify(apiResult_message.error).slice(0,64) + ' ...';
            }
            var new_log_message = [local_datetime, 'api', apiResult_message['id'] + ":" + max_str];
            if(apiResult_message['id'].indexOf("getConfig") != -1 ){
                // console.log(received_logs_num/60, isInteger(received_logs_num/60), apiResult_message);
                if(isInteger(received_logs_num/60)){
                    log_table.row.add(new_log_message).draw();
                }
                received_logs_num = received_logs_num + 1;
            }else{
                log_table.row.add(new_log_message).draw();
            }
        }

        // console.log(apiResult_message['id']);

        if(apiResult_message['id'].indexOf("setConfig") != -1 ){
            $("span.api-feed").text(apiResult_message.id + ":" + JSON.stringify(apiResult_message.data));
            console.log(apiResult_message);
        }

        if(apiResult_message['id'].indexOf("getConfig") != -1 ){
            // console.log(apiResult_message);

            if(apiResult_message.result){
                current_opcconfig = apiResult_message['data'];
                $(".OPCServerName").text(apiResult_message['data']['opcname']);
                $(".OPCServerHost").text(apiResult_message['data']['opchost']);
                $("#ClientID").val(apiResult_message['data']['clientid']);
                $("#OPCServer").val(apiResult_message['data']['opcname']);
                $("#OPCHost").val(apiResult_message['data']['opchost']);
                if(isEmpty($("#OPCServerHost").val())){
                    $("#OPCServerHost").val(apiResult_message['data']['opchost']);
                }
                var opcitems = apiResult_message['data']['opcitems'];
                // console.log(opcitems[0]);
                $("#OPCItems").val('');
                var content_str = $("#OPCItems").val();
                $.each(opcitems, function (i, v) {
                    // console.log(v);
                    content_str = content_str + v + "\n";
                });
                $("#OPCItems").val(content_str);
            }



        }

        if(apiResult_message['id'].indexOf("opctags_list") != -1 ){
            $("span.api-feed").text(apiResult_message.id + ":" + apiResult_message.result);
            if(apiResult_message.result){
                var opcitems = apiResult_message.data;
                // console.log(opcitems);
                var content_str = '';
                $("#NewOPCItems").val(content_str);
                $.each(opcitems, function (i, v) {
                    // console.log(v);
                    content_str = content_str + v + "\n";
                });
                $("#NewOPCItems").val(content_str);
            }

        }

        if(apiResult_message['id'].indexOf("tunnelStatus") != -1 ){
            if(apiResult_message.result) {
                $(".OPCServerStatus").text(apiResult_message['data']);
            }
        }

        if(apiResult_message['id'].indexOf("tunnelClean") != -1 ){
            if(apiResult_message.result) {
                $(".OPCServerStatus").text(apiResult_message.result);
            }
        }

        if(apiResult_message['id'].indexOf("opcservers_list") != -1 ){
            $("span.api-feed").text(apiResult_message.id + ":" + apiResult_message.result);
            // console.log(message.destinationName);
            if(apiResult_message.result){
                console.log(apiResult_message);
                $("select.opcserverslist").empty();
                var opcservers_data = apiResult_message['data'];
                if(opcservers_data.length>0){
                    $.each(opcservers_data, function (i, v) {
                        // console.log(v);
                        $("select.opcserverslist").append("<option value='" + v + "'>" + v +"</option>");
                    });
                    $("select.opcserverslist").get(0).selectedIndex = 0;
                    var opcservername = $("select.opcserverslist").val();
                    var opchost = $("#OPCServerHost").val();
                    var message = new Paho.Message(JSON.stringify({"id":'opctags_list/' + $("#newClientID").val() + '/' + Date.parse(new Date()).toString(), "opcserver":opcservername,  "opchost":opchost}));
                    message.destinationName = 'v1/opcdabrg/api/opctags_list';
                    message.qos = 0;

                    mqtt_client.send(message);
                }

            }
        }

        if(apiResult_message['id'].indexOf("deviceWrite") != -1 ){
            $("span.write-feed").text(apiResult_message.id + ":" + apiResult_message.data);
            // console.log(message.destinationName);
        }
        // $(".MQTTStatus").text(apiResult_message['data']['clientid']);

    }

}

function connectionToggle() {

  if (connected) {
    disconnect();
  } else {
    connect();
  }

}


function connect() {
  var hostname = mqtt_host;
  var port = mqtt_port;
  var clientId = "webclient-"+makeid();
  $("#newClientID").val(clientId);
  var path = "/mqtt";
  var user = '';
  var pass = '';
  // var pass = "Pa88word";
  var keepAlive = 60;
  var timeout = 3;
  var tls = false;
  var automaticReconnect = true;
  var cleanSession = true;
    var lastWillTopic = null;
    var lastWillQos = 0;
    var lastWillRetain = false;
    var lastWillMessage = null;


  if (path.length > 0) {
    mqtt_client =new Paho.Client(hostname, Number(port), path, clientId);
  } else {
    mqtt_client =new Paho.Client(hostname, Number(port), clientId);
  }
  // logMessage("INFO", "Connecting to Server: [Host: ", hostname, ", Port: ", port, ", Path: ", mqtt_client.path, ", ID: ", clientId, ", USER: ", user,", PASS: ", pass,"]");

  // set callback handlers
  mqtt_client.onConnectionLost = onConnectionLost;
  mqtt_client.onMessageArrived = onMessageArrived;
  mqtt_client.onConnected = onConnected;


  var options = {
    invocationContext: { host: hostname, port: port, path: mqtt_client.path, clientId: clientId },
    timeout: timeout,
    keepAliveInterval: keepAlive,
    cleanSession: cleanSession,
    useSSL: tls,
    reconnect: true,
    onSuccess: onConnect,
    onFailure: onFail
  };



  if (user.length > 0) {
    options.userName = user;
  }

  if (pass.length > 0) {
    options.password = pass;
  }

  if (lastWillTopic) {
    var lastWillMessage = new Paho.Message(lastWillMessage);
    lastWillMessage.destinationName = lastWillTopic;
    lastWillMessage.qos = lastWillQos;
    lastWillMessage.retained = lastWillRetain;
    options.willMessage = lastWillMessage;
  }

  // connect the client
    try {
        mqtt_client.connect(options);
    } catch (error) {
        mqttc_connected = false;
        console.log(error);
    }

  console.log();


  // var statusSpan = document.getElementById("connectionStatus");
  // statusSpan.innerHTML = "Connecting...";
}

function disconnect() {
  // logMessage("INFO", "Disconnecting from Server.");
    console.log( "Disconnecting from Server.");
  mqtt_client.disconnect();
  // var statusSpan = document.getElementById("connectionStatus");
  // statusSpan.innerHTML = "Connection - Disconnected.";
  mqttc_connected = false;
}


function publish() {
  var topic = document.getElementById("publishTopicInput").value;
  var qos = document.getElementById("publishQosInput").value;
  var message = document.getElementById("publishMessageInput").value;
  var retain = document.getElementById("publishRetainInput").checked;
  // logMessage("INFO", "Publishing Message: [Topic: ", topic, ", Payload: ", message, ", QoS: ", qos, ", Retain: ", retain, "]");
  message = new Paho.Message(message);
  message.destinationName = topic;
  message.qos = Number(qos);
  message.retained = retain;
  mqtt_client.send(message);
}


function subscribe() {
  var topic = document.getElementById("subscribeTopicInput").value;
  var qos = document.getElementById("subscribeQosInput").value;
  logMessage("INFO", "Subscribing to: [Topic: ", topic, ", QoS: ", qos, "]");
  mqtt_client.subscribe(topic, { qos: Number(qos) });
}

function unsubscribe() {
  var topic = document.getElementById("subscribeTopicInput").value;
  // logMessage("INFO", "Unsubscribing: [Topic: ", topic, "]");
  mqtt_client.unsubscribe(topic, {
    onSuccess: unsubscribeSuccess,
    onFailure: unsubscribeFailure,
    invocationContext: { topic: topic }
  });
}


function unsubscribeSuccess(context) {
  // logMessage("INFO", "Unsubscribed. [Topic: ", context.invocationContext.topic, "]");
}

function unsubscribeFailure(context) {
  // logMessage("ERROR", "Failed to unsubscribe. [Topic: ", context.invocationContext.topic, ", Error: ", context.errorMessage, "]");
}

function clearHistory() {
  var table = document.getElementById("incomingMessageTable");
  //or use :  var table = document.all.tableid;
  for (var i = table.rows.length - 1; i > 0; i--) {
    table.deleteRow(i);
  }

}

