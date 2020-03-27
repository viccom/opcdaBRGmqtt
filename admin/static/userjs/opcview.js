var opcdata = [];

setTimeout(function () {
    connect();
},600);

/**
 *	周期检测mqtt状态
 */
var mqtt_status_ret= setInterval(function(){
    if(mqttc_connected){
        $(".MQTTStatus").text("已连接");
        $(".MQTTStatus").addClass('label-success');
    }else{
        $(".MQTTStatus").text("重连中");
        $(".MQTTStatus").removeClass('label-success');
        $(".OPCServerStatus").text('unknown');
        $(".OPCServerStatus").removeClass('label-success');
        // $("select.opcserverslist").empty();
        // $("select.opcserverslist").append("<option value='点击上方查询按钮'></option>");
        // $("#NewOPCItems").val('');
        connect();
    }

},2000);

/**
 *	周期获取opcdaBRG状态
 */

var opcdaBRG_status_ret= setInterval(function(){
    if(mqttc_connected){
        // console.log('查询opcdaBRG状态');
        var message = new Paho.Message(JSON.stringify({"id":'getConfig/' + $("#newClientID").val() + '/' + Date.parse(new Date()).toString()}));
        message.destinationName = 'v1/opcdabrg/api/getConfig';
        message.qos = 0;
        mqtt_client.send(message);
    }
},5000);


$('span.reset').click(function(){
    $("#ClientID").val('');
    $("#OPCHost").val('');
    $("#OPCServer").val('');
    $("#OPCItems").val('');

});

$('span.opc-query').click(function(){
    if(mqttc_connected) {
        var message = new Paho.Message(JSON.stringify({"id": 'opcservers_list/' + $("#newClientID").val() + '/' + Date.parse(new Date()).toString()}));
        message.destinationName = 'v1/opcdabrg/api/opcservers_list';
        message.qos = 0;
        mqtt_client.send(message);
    }
    // console.log(2)
});

$('span.select-to-left').click(function(){
    if($("select.opcserverslist option:selected").val()=="点击上方查询按钮"){
        $("span.api-feed").text("点击上方查询按钮获取OPCServer列表");
    }else{
        $("select.opcserverslist").trigger('change');
        //  $("select.opcserverslist").attr("size",2);
    }

    // var opcservername = $("select.opcserverslist").val();
    // $("#OPCServer").val(opcservername);
});

$("select.opcserverslist").change(function() {
    // var options=$("select.opcserverslist option:selected");
    // console.log(options.val());
    if($("select.opcserverslist option:selected").val()!="点击上方查询按钮"){
        var opcservername = $(this).val();
        var opchost = $("#OPCServerHost").val();
        if(mqttc_connected) {
            var message = new Paho.Message(JSON.stringify({
                "id": 'opctags_list/' + $("#newClientID").val() + '/' + Date.parse(new Date()).toString(),
                "opcserver": opcservername,
                "opchost": opchost
            }));
            message.destinationName = 'v1/opcdabrg/api/opctags_list';
            message.qos = 0;
            mqtt_client.send(message);
        }
    }else{
        $("span.api-feed").text("点击上方查询按钮获取OPCServer列表");
    }

});

$('button.postconfig').click(function(){
    console.log("normal psotconfig");
    var opc_config = new Object();
    opc_config.clientid = $("#newClientID").val();
    opc_config.opcname = $("select.opcserverslist option:selected").val();
    opc_config.opchost = $("#OPCServerHost").val();
    var opcitems = $("#NewOPCItems").val().trim();
    if(opcitems.length>0){
        opcitems = opcitems.split(/[\n]/)
        opc_config.opcitems = opcitems;
    }
    // console.log(opc_config);
    var opctags = [];
    $.each(opcitems, function (i, v) {
        // console.log(v);
        opctags.push([v.replace(/\./, "_") ,'float' ,v]);
    });
    opc_config.opctags = opctags;

    if(opc_config.opcname!=="点击上方查询按钮" && opcitems.length>0){
        // console.log(opc_config);
        if(mqttc_connected) {
            var message = new Paho.Message(JSON.stringify({
                "id": 'setConfig/' + $("#newClientID").val() + '/' + Date.parse(new Date()).toString(),
                "config": opc_config
            }));
            message.destinationName = 'v1/opcdabrg/api/setConfig';
            message.qos = 0;
            mqtt_client.send(message);
        }
    }else{
        $("span.api-feed").text("未选择OPCServer或OPC标签为空");
    }

});

$('button.postconfigForced').click(function(){
    console.log("force psotconfig");
    var opc_config = new Object();
    opc_config.clientid = $("#newClientID").val();
    opc_config.opcname = $("select.opcserverslist option:selected").val();
    opc_config.opchost = $("#OPCServerHost").val();
    var opcitems = $("#NewOPCItems").val().trim();
    if(opcitems.length>0){
        opcitems = opcitems.split(/[\n]/)
        opc_config.opcitems = opcitems;
    }
    // console.log(opc_config);
    var opctags = [];
    $.each(opcitems, function (i, v) {
        // console.log(v);
        opctags.push([v.replace(/\./, "_") ,'float' ,v]);
    });
    opc_config.opctags = opctags;

    if(opc_config.opcname!=="点击上方查询按钮" && opcitems.length>0){
        console.log(opc_config);
        if(mqttc_connected) {
            var message = new Paho.Message(JSON.stringify({
                "id": 'setConfigForced/' + $("#newClientID").val() + '/' + Date.parse(new Date()).toString(),
                "config": opc_config
            }));
            message.destinationName = 'v1/opcdabrg/api/setConfigForced';
            message.qos = 0;
            mqtt_client.send(message);
        }
    }else{
        $("span.api-feed").text("未选择OPCServer或OPC标签为空");
    }
});


$('span.log-clean').click(function(){
    log_table.clear().draw();
});

$('span.cleanTunnel').click(function(){
    if(mqttc_connected) {
        var message = new Paho.Message(JSON.stringify({"id": 'tunnelClean/' + $("#newClientID").val() + '/' + Date.parse(new Date()).toString()}));
        message.destinationName = 'v1/opcdabrg/api/tunnelClean';
        message.qos = 0;
        mqtt_client.send(message);
    }
});


$('button.postValue').click(function(){
    var itemid = $("span.itemId").text();
    var itemvalue = $("input.itemValue").val();
    if(!$.isEmptyObject(current_opcconfig)){
        var opctags = current_opcconfig['opctags'];
        // console.log(current_opcconfig);
        $.each(opctags, function (i, v) {
            // console.log(v[2]);
            if(v[2]==itemid){

                if(v[1]=="float"){
                    itemvalue = parseFloat(itemvalue);
                }
                if(v[1]=="int"){
                    itemvalue = parseInt(itemvalue);
                }
                if(v[1]=="boolean"){
                    itemvalue = parseInt(itemvalue);
                }
            }
        });

        var tags_values = [itemid, itemvalue];
        console.log(tags_values);

        if(mqttc_connected) {
            var message = new Paho.Message(JSON.stringify({"id": 'deviceWrite/' + $("#newClientID").val() + '/' + Date.parse(new Date()).toString(), "tags_values": tags_values}));
            message.destinationName = 'v1/opcdabrg/api/deviceWrite';
            message.qos = 0;
            mqtt_client.send(message);
        }
    }



});


$("body").on("click", "button.writeItem", function() {
    var opcitem =$(this).data('id');
    // console.log(opcitem);
    $("span.itemId").text(opcitem);
    $("span.write-feed").text('');

});

$(function () {
    /**
     *	初始化数据表格
     */
    data_table = $('#data_table').DataTable({
        // "dom": '',
        "filter": true,
        "info": true,
        "scrollY":        "400px",
        "scrollCollapse": true,
        "paging":         true,
        "processing": true,
        "bStateSave": true,
        "order": [[ 0, "asc" ]],
        "language": {
            "sProcessing": "处理中...",
            "sLengthMenu": "显示 _MENU_ 项结果",
            "sZeroRecords": "没有匹配结果",
            "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
            "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
            "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
            "sInfoPostFix": "",
            "sSearch": "搜索:",
            "sUrl": "",
            "sEmptyTable": "消息为空",
            "sLoadingRecords": "载入中...",
            "sInfoThousands": ",",
            "oPaginate": {
                "sFirst": "首页",
                "sPrevious": "上页",
                "sNext": "下页",
                "sLast": "末页"
            },
            "oAria": {
                "sSortAscending": ": 以升序排列此列",
                "sSortDescending": ": 以降序排列此列"
            }
        },
        data: opcdata,
        columnDefs: [
            {
                //   指定第第1列
                targets:  0,
                "width": '20%',
                searchable: true,
                orderable: true

            },
            {
                //   指定第第2列
                targets:  1,
                "width": '20%',
                searchable: false,
                orderable: false
            },
            {
                //   指定第第3列
                targets:  2,
                "width": '10%',
                searchable: true,
                orderable: false
            },
            {
                //   指定第第4列
                targets:  3,
                "width": '40%',
                searchable: false,
                orderable: false
            },
            {
                //   指定第第5列
                targets:  4,
                "width": '10%',
                searchable: false,
                orderable: false
            }
        ],
        "initComplete": function(settings, json) {
            console.log("data_table init over");
        }
    });


    /**
     *	初始化日志表格
     */
    log_table = $('#log_table').DataTable({
        // "dom": '',
        "filter": true,
        "info": false,
        // "scrollY":        "50px",
        // "scrollCollapse": true,
        "paging":         false,
        "processing": true,
        "bStateSave": false,
        "order": [[ 0, "asc" ]],
        "language": {
            "sProcessing": "处理中...",
            "sLengthMenu": "显示 _MENU_ 项结果",
            "sZeroRecords": "没有匹配结果",
            "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
            "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
            "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
            "sInfoPostFix": "",
            "sSearch": "搜索:",
            "sUrl": "",
            "sEmptyTable": "消息为空",
            "sLoadingRecords": "载入中...",
            "sInfoThousands": ",",
            "oPaginate": {
                "sFirst": "首页",
                "sPrevious": "上页",
                "sNext": "下页",
                "sLast": "末页"
            },
            "oAria": {
                "sSortAscending": ": 以升序排列此列",
                "sSortDescending": ": 以降序排列此列"
            }
        },
        columnDefs: [
            {
                //   指定第第1列
                targets:  0,
                "width": '15%',
                searchable: false,
                orderable: false

            },
            {
                //   指定第第2列
                targets:  1,
                "width": '10%',
                searchable: true,
                orderable: false
            },
            {
                //   指定第第4列
                targets:  2,
                "width": '75%',
                searchable: true,
                orderable: false
            }
        ],
        "initComplete": function(settings, json) {
            console.log("log_table init over")
        }
    });

})


