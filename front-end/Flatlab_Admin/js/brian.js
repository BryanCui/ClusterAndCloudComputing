 $.getJSON("http://115.146.89.147:8080/scenarios/4",function(result){
        console.log(result);
        var charts = result.charts;
        var colors = ["#b37c57", "#0a7e8c", "#53802d", "#f6546a", "#00ff66","#ffff00"]
            // initialize the chart
        for (i in charts){
            var myChart = echarts.init(document.getElementById(i));
            myChart.showLoading();
            option = {
                title: {
                    text: charts[i].title,
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                        type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    }
                },
                toolbox: {
                    show: true,
                    feature: {
                        dataView: {readOnly: false},
                        magicType: {type: ['line', 'bar']},
                        restore: {},
                        saveAsImage: {}
                    }
                },
                legend: {
                    data: charts[i].x_label
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis : [
                    {
                        type : 'category',
                        data : charts[i].x_label
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    }
                ],
                series : [
                    {
                        itemStyle: {
                            normal: {
                                barBorderColor: 'rgba(0,0,0,0)',
                                color: function(params) {
                                    // build a color map as your need.
                                    var colorList = [
                                        '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                                        '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                                        '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
                                    ];
                                    return colorList[params.dataIndex]
                                },
                            },
                        },
                        name:charts[i].title,
                        type:'bar',
                        data:charts[i].values.values
                    },

                ]
            };
            myChart.hideLoading();
            myChart.setOption(option);
        };

    });