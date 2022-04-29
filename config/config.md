# config item 字段及说明
```json
  {
    //必填，item标识 用于跳转时的标识 应全局唯一
    "example": {
      //是否debug (false,true) 默认为false
      "debug": false, 
      //图像识别配置
      "match": {   
        //是否兼容截图 默认为false
        "compatible": false,
        //识别方法
        "method": "TM_SQDIFF_NORMED", 
        //需匹配的图像url 如果为数组 则只需其中一个匹配 
        "sample": "样品url",
        //识别个数
        "targetNum": 1, 
        //相识概率
        "rate": 0.9,
        //当sample为数组时 各项匹配结果之间的关系 （and 且，or 或）判定后为match的True/False结果
        "relation": "and",
        //匹配结果标识(false,true)保存到全局指定字段
        "saveAs": "property"
      },
      //执行判定 如果有此项 则判定后的逻辑会和match结果并起来
      "judge": { 
        //触发判定的时机 (after,before) 在匹配后触发还是匹配前触发
        "time": "after", 
        //匹配完成后获取全局自定字段
        "getProperty": ["property"],  
        //判定值
        "judgeValue": [0], 
        //操作符 (>, <, >=, <=, =, is, in )
        "operator": ["is"], 
        //各判定之间的关系 （and 且，or 或）
        "relation": "and"
      },
      //match结果[且judge结果]为false时执行
      "reject": { 
        //失败后且重试完后跳转到哪个tag
        "jump": "example", 
        //大于0则开启随机sleep
        "sleepRandom": 0.5,
        //睡眠秒数
        "sleep": 0,
        //如果匹配失败重试次数
        "retry": 0  
      },
      //match结果[且judge结果]为true时执行
      "resolve": {
        //成功后跳转到哪个tag
        "jump": "example", 
        //匹配完执行 （click点击, jump 跳转）
        "do": "click", 
        //成功时执行设置值操作
        "setProperty": ["property"], 
        //当为关键词 (sum,sub)，分别对应累加和累减
        "propertyValue": [1] 
      },
      //点击配置
      "click": {
        //如果提供了position 且没有图像识别， 则使用这个坐标
        "position": [0,0],
        //如果match的targetNum大于1 则targetClick生效 却点击输入的索引,如果此索引没有匹配到则不执行点击,不配置则点击全部
        "targetClick": [0],
        //识别后点击坐标位于识别区域的那里 默认center 可以输入 （leftTop, rightTop, leftBottom, rightBottom, center）
        "positionBase": "center", 
        //基于positionBase 再偏移 [x,y]像素
        "offset": [0, 0],
        // 基于positionBase和offset计算后的点为圆心 random为半径画圆 点击随机落在圆形区域内
        "random": 10,
        //实现拖拽
        "movePath": [["+100", "-100"],[0,0]],
      },
      //暂定指定秒数之后执行next
      "sleep": 4,
      //大于0则开启随机sleep
      "sleepRandom": 0.5,
      //指定除了执行jump外正常的流程下一个tag
      "next": "tag" 
    }
  }
```