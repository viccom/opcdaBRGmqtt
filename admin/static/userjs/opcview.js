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
    }else{
        $(".MQTTStatus").text("重连中");
        $("select.opcserverslist").empty();
        $("select.opcserverslist").append("<option value='点击上方查询按钮'></option>");
        $("#NewOPCItems").val('');
        connect();
    }

},2000);

/**
 *	周期获取opcdaBRG状态
 */
var opcdaBRG_status_ret= setInterval(function(){
    if(mqttc_connected){
        // console.log('查询opcdaBRG状态');
        var message = new Paho.Message(JSON.stringify({"id":'getConfig/' + Date.parse(new Date()).toString()}));
        message.destinationName = 'v1/opcdabrg/api/getConfig';
        message.qos = 0;
        mqtt_client.send(message);
        message = new Paho.Message(JSON.stringify({"id":'tunnelStatus/' + Date.parse(new Date()).toString()}));
        message.destinationName = 'v1/opcdabrg/api/tunnelStatus';
        message.qos = 0;
        mqtt_client.send(message);
    }

},2000);


$('span.reset').click(function(){
    $("#ClientID").val('');
    $("#OPCHost").val('');
    $("#OPCServer").val('');
    $("#OPCItems").val('');

});

$('span.opc-query').click(function(){
    var message = new Paho.Message(JSON.stringify({"id":'opcservers_list/' + Date.parse(new Date()).toString()}));
    message.destinationName = 'v1/opcdabrg/api/opcservers_list';
    message.qos = 0;
    mqtt_client.send(message);
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
        var message = new Paho.Message(JSON.stringify({"id":'opctags_list/' + Date.parse(new Date()).toString(), "opcserver":opcservername, "opchost":opchost}));
        message.destinationName = 'v1/opcdabrg/api/opctags_list';
        message.qos = 0;
        mqtt_client.send(message);
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
        var message = new Paho.Message(JSON.stringify({"id":'setConfig/' + Date.parse(new Date()).toString(),"config":opc_config}));
        message.destinationName = 'v1/opcdabrg/api/setConfig';
        message.qos = 0;
        mqtt_client.send(message);
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
        var message = new Paho.Message(JSON.stringify({"id":'setConfigForced/' + Date.parse(new Date()).toString(),"config":opc_config}));
        message.destinationName = 'v1/opcdabrg/api/setConfigForced';
        message.qos = 0;
        mqtt_client.send(message);
    }else{
        $("span.api-feed").text("未选择OPCServer或OPC标签为空");
    }
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
                orderable: false

            },
            {
                //   指定第第2列
                targets:  1,
                "width": '20%',
                searchable: false,
                orderable: false
            },
            {
                //   指定第第4列
                targets:  2,
                "width": '10%',
                searchable: true,
                orderable: false
            },
            {
                //   指定第第4列
                targets:  3,
                "width": '50%',
                searchable: false,
                orderable: false
            }
        ],
        "initComplete": function(settings, json) {
            console.log("data_table init over")
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

/**
 *	周期检测mqtt状态
 */
/*

var mqtt_status_ret= setInterval(function(){
    $(".log_nums").text(table_log.data().length);
    if(mqttc_connected){
        $(".appinfo-upload").text("停止");
        $(".appinfo-upload").addClass("btn-warning");
        $(".appinfo-upload").removeClass("btn-primary");
    }else{
        $(".appinfo-upload").text("连接");
        $(".appinfo-upload").addClass("btn-primary");
        $(".appinfo-upload").removeClass("btn-warning");
    }
    if(log_subscribed){
        $(".btn-log-subscribe").text("取消订阅");
        $(".btn-log-subscribe").addClass("btn-success");
    }else{
        $(".btn-log-subscribe").text("日志订阅");
        $(".btn-log-subscribe").removeClass("btn-success");
    }

},1000);
*/

/**
 *	周期上传日志报文
 */

/*

var mqtt_upload_ret= setInterval(function(){
    var lens=table_log.data().length;
    if(lens<1000){
        if(mqttc_connected){
            if(log_subscribed){
                var id = "sys_enable_log" + '/' + gate_sn + '/'+ Date.parse(new Date())
                var _act = {
                    "device": gate_sn,
                    "data": 60,
                    "id": id
                };
                gate_upload_mes("sys_enable_log", _act)
            }

        }
    }else{
        mqtt_client.unsubscribe(gate_sn + "/" + "log", {
            onSuccess: unsubscribeSuccess,
            onFailure: unsubscribeFailure,
            invocationContext: { topic: gate_sn + "/" + "log" }
        });

        log_subscribed = false;

        $.notify({
            title: "<strong>记录数超过接收队列:</strong><br><br> ",
            message: "日志和报文记录数已经超过1000，需清除后才可继续接收！"
        },{
            type: 'warning',
            delay: 29000
        });
    }

},30000);

*/

/**
 *	开启日志和报文上传功能
 */
/*
$(".btn-log-subscribe").click(function(){
    var lens=table_log.data().length;
    if(mqttc_connected){
        if(log_subscribed){
            mqtt_client.unsubscribe(gate_sn + "/" + "log", {
                onSuccess: unsubscribeSuccess,
                onFailure: unsubscribeFailure,
                invocationContext: { topic: gate_sn + "/" + "log" }
            });
            log_subscribed = false;
            $(".btn-log-subscribe").removeClass("btn-success");
        }else{
            try {
                if(lens<1000){
                    mqtt_client.subscribe(gate_sn + "/" + "log", {qos: 0});
                    log_subscribed = true;
                    $(".btn-log-subscribe").addClass("btn-success");
                    var id = "sys_enable_log" + '/' + gate_sn + '/'+ Date.parse(new Date())
                    var _act = {
                        "device": gate_sn,
                        "data": 60,
                        "id": id
                    };
                    gate_upload_mes("sys_enable_log", _act)
                }else{
                    $.notify({
                        title: "<strong>记录数超过接收队列:</strong><br><br> ",
                        message: "日志和报文记录数已经超过1000，需清除后才可继续接收！"
                    },{
                        delay: 5000
                    });
                }

            } catch (error) {
                console.log(error);
                mqttc_connected = false;
                log_subscribed = false;
                $(".btn-log-subscribe").removeClass("btn-success");
            }
        }

    }
});

$(".appinfo-clear").click(function(){
    table_log.clear().draw();
});
*/




/**
 *	过滤选择处理-start
 */
/*

$('div.log_filter li').on('click', function(){
    $('.search_log').text($(this).text());
    $('input.J_keyword').val("");
    table_log.columns( 1 ).search("").draw();
    table_log.columns( 2 ).search("").draw();
    table_log.columns( 3 ).search("").draw();
    table_log.search("").draw();

});
*/



/*

$("input.J_keyword").bind("input propertychange",function(event){
    var key = $('input.J_keyword').val();
    var colnum = 3;

    if($('.search_log').text()=="内容"){
        colnum = 3
    }
    if($('.search_log').text()=="ID"){
        colnum = 2
    }
    if($('.search_log').text()=="类型"){
        colnum = 1
    }

    console.log(colnum, key);
    if(key!=null){
        table_log.columns( colnum ).search(key).draw();
    }
});

$('button.J_keyword').on('keyup click', function () {
    var key = $('input.J_keyword').val();
    var colnum = 3;

    if ($('.search_log').text() == "内容") {
        colnum = 3
    }
    if ($('.search_log').text() == "ID") {
        colnum = 2
    }
    if ($('.search_log').text() == "类型") {
        colnum = 1
    }


    table_log.columns(colnum).search(key, false, true).draw();
});
*/
/**
 *	过滤选择处理-end
 */
