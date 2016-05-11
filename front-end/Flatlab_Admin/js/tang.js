 $.getJSON("http://115.146.89.147:8080/scenarios/2",function(result){
        var charts = result.charts
        for (i in charts){
            // initialize the chart
            var myChart = echarts.init(document.getElementById(i));
            option = {
                title: {
                    text: charts[i].title,
                    x: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                toolbox: {
                    show: true,
                    feature: {
                        mark: {show: true},
                        dataView: {show: true, readOnly: false},
                        magicType: {
                            show: true,
                            type: ['pie', 'funnel']
                        },
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    data: charts[i].names

                },
                series: [
                    {
                        name: charts[i].title,
                        type: charts[i].type,
                        radius: '60%',
                        center: ['50%', '60%'],
                        data: charts[i].data,
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    },
                ]
            }
            myChart.setOption(option);
        };

    });