 $.getJSON("http://115.146.89.147:8080/scenarios/3",function(result){
        console.log(result);
        var charts = result.charts;
            // initialize the chart
        var myChart = echarts.init(document.getElementById("uncle"));
        myChart.showLoading();
        target = [];
        values = charts[0].values
        for (x in values){
            var j = {
                name:values[x].name,
                    type:'line',
                data:values[x].values,
                markPoint: {
                data: [
                    {type: 'max', name: 'max'},
                    {type: 'min', name: 'min'}
                ]
            },
                markLine: {
                    data: [
                        {type: 'average', name: 'average'}
                    ]
                }
            };
            target.push(j)
        };
        option = {
            title: {
                text: result.title,
            },
            tooltip: {
                trigger: 'axis'
            },

            toolbox: {
                show: true,
                feature: {
                    dataZoom: {
                        show: true,
                        title: {
                            dataZoom: 'zoom in',
                            dataZoomReset: 'zoom out'
                        }
                    },
                    dataView: {readOnly: false},
                    magicType: {type: ['line', 'bar']},
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis:  {
                type: 'category',
                boundaryGap: false,
                data: charts[0].x_label
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value}'
                }
            },
            legend: {
                data: ['Melbourne','Sydney']
            },
            series: target
        };
        myChart.hideLoading();
        myChart.setOption(option);
    });