 $.getJSON("http://127.0.0.1:8080/scenarios/1",function(result){
        var charts = result.charts;
        var tw_ins=0;
        var tw_web=0;
        var tw_android=0;
        var tw_ios=0;

        for (i in charts){
            // Ins Total
            if (charts[i].title == "Instagram"){
                for (x in charts[i].data){
                    tw_ins = tw_ins+charts[i].data[x].value;
                };

                $("#tw_ins").text(tw_ins)
            };

            // Android
            if (charts[i].title == "Twitter for Android"){
                for (x in charts[i].data){
                    tw_android = tw_android+charts[i].data[x].value;
                };
                $("#tw_android").text(tw_android)
            };

            // IOS
            if (charts[i].title == "Twitter for iPad"||charts[i].title == "Twitter for iPhone"){
                for (x in charts[i].data){
                    tw_ios = tw_ios+charts[i].data[x].value;
                };
                $("#tw_ios").text(tw_ios)
            };

            // Web
            if (charts[i].title == "Twitter Web Client"){
                for (x in charts[i].data){
                    tw_web = tw_web+charts[i].data[x].value;
                };
                $("#tw_web").text(tw_web)
            };
            // initialize the chart
            var myChart = echarts.init(document.getElementById(i));
            option = {
                title : {
                    text: charts[i].title,
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                toolbox: {
                    show : true,
                    feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {
                    show: true,
                    type: ['pie', 'funnel']
                },
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    data: charts[i].names

                },
                series : [
                    {
                        name: charts[i].title,
                        type: "pie",
                        radius : '60%',
                        
                        center: ['50%', '60%'],
                        data:charts[i].data,
                        itemStyle:{
                            normal:{
                                label:{
                                    show: true,
                                    formatter: '({d}%)'
                                },
                                labelLine :{show:true}
                            }
                        }
                    }
                ]
            };
            myChart.setOption(option);
        };
            // initialize the last chart
            var total_data = [{"name":"Instagram","value":tw_ins},{"name":"IOS","value":tw_ios},{"name":"WEB","value":tw_web},{"name":"Android","value":tw_android}];
            console.log(total_data)
            var lastChart = echarts.init(document.getElementById(5));
            option = {
             title : {
                 text: "Tweets From Deivices",
                 x:'center'
             },
             tooltip : {
                 trigger: 'item',
                 formatter: "{a} <br/>{b} : {c} ({d}%)"
             },
             toolbox: {
                 show : true,
                 feature : {
                     mark : {show: true},
                     dataView : {show: true, readOnly: false},
                     magicType : {
                         show: true,
                         type: ['pie', 'funnel']
                     },
                     restore : {show: true},
                     saveAsImage : {show: true}
                 }
             },
             legend: {
                 orient: 'vertical',
                 left: 'left',
                 data: ["Instagram","IOS","WEB","Android"]

             },
             series : [
                 {
                     name: "Tweets Source",
                     type: "pie",
                     radius : ['30%', '60%'],
                     center: ['50%', '60%'],
                     data: total_data,
                     itemStyle:{
                         normal:{
                             label:{
                                 show: true,
                                 formatter: '({d}%)'
                             },
                             labelLine :{show:true}
                         }
                     }
                 }
             ]
            };
            lastChart.setOption(option);
    });