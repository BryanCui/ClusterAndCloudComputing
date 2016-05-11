var myChart = echarts.init(document.getElementById(0));
var lastChart = echarts.init(document.getElementById(1));
myChart.showLoading();
lastChart.showLoading();
$.getJSON("http://115.146.89.147:8080/scenarios/5",function(result){
        var charts = result.charts;
        var value = parseInt(charts[4].data[0].value)*1.2
        charts[4].data[0].value = value
            option = {
                title: {
                    text: "0-200                                                    200-400                                                         400-600",
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
                    data: charts[0].names

                },
                series: [
                    {
                        name: charts[0].title,
                        type: charts[0].type,
                        roseType: "line",
                        radius: '60%',
                        center: ['20%', '60%'],
                        data: charts[0].data,
                        itemStyle: {
                            normal:{
                                color: function(params) {
                                    // build a color map as your need.
                                    var colorList = [
                                        '#E84640','#009999','#60C0DD'
                                    ];
                                    return colorList[params.dataIndex]
                                },
                                label:{
                                    show: true,
                                    formatter: '({b}: {d}%)'
                                },
                                labelLine :{show:true}
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    },
                    {
                        name: charts[1].title,
                        type: charts[1].type,
                        roseType: "line",
                        radius: '60%',
                        center: ['50%', '60%'],
                        data: charts[1].data,
                        itemStyle: {
                            normal:{
                                color: function(params) {
                                    // build a color map as your need.
                                    var colorList = [
                                        '#E84640','#009999','#60C0DD'
                                    ];
                                    return colorList[params.dataIndex]
                                },
                                label:{
                                    show: true,
                                    formatter: '({b}: {d}%)'
                                },
                                labelLine :{show:true}
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    },
                    {
                        name: charts[2].title,
                        type: charts[2].type,
                        roseType: "line",
                        radius: '60%',
                        center: ['80%', '60%'],
                        data: charts[2].data,
                        itemStyle: {
                            normal:{
                                color: function(params) {
                                    // build a color map as your need.
                                    var colorList = [
                                        '#E84640','#009999','#60C0DD'
                                    ];
                                    return colorList[params.dataIndex]
                                },
                                label:{
                                    show: true,
                                    formatter: '({b}: {d}%)'
                                },
                                labelLine :{show:true}
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    },
                ]
            }
            last_option = {
                title: {
                    text: "600-800                                                       800+                                                                    ",
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
                    data: charts[0].names

                },
                series: [
                    {
                        name: charts[3].title,
                        type: charts[3].type,
                        roseType: "line",
                        radius: '60%',
                        center: ['20%', '60%'],
                        data: charts[3].data,
                        itemStyle: {
                            normal:{
                                color: function(params) {
                                    // build a color map as your need.
                                    var colorList = [
                                        '#E84640','#009999','#60C0DD'
                                    ];
                                    return colorList[params.dataIndex]
                                },
                                label:{
                                    show: true,
                                    formatter: '({b}: {d}%)'
                                },
                                labelLine :{show:true}
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    },
                    {
                        name: charts[4].title,
                        type: charts[4].type,
                        roseType: "line",
                        radius: '60%',
                        center: ['50%', '60%'],
                        data: charts[4].data,
                        itemStyle: {
                            normal:{
                                color: function(params) {
                                    // build a color map as your need.
                                    var colorList = [
                                        '#E84640','#009999','#60C0DD'
                                    ];
                                    return colorList[params.dataIndex]
                                },
                                label:{
                                    show: true,
                                    formatter: '({b}: {d}%)'
                                },
                                labelLine :{show:true}
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    },
                ]
            }
            myChart.hideLoading();
            lastChart.hideLoading();
            myChart.setOption(option);
            lastChart.setOption(last_option);

    });