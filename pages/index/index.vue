<template>
  <view class="container">
    <view class="header">语音MOS打分</view>
	
    <view style="padding: 20px; background-color: aliceblue;">
			<view>
				<view>1. 模型介绍：</view>
			</view>
			<view>
				<view>2. 打分规则</view>
				<view>
					流畅度打分： 根据合成语音的韵律从1-5分打出一个认为合理的分数。
				</view>
				<view></view>
			</view>
		
	</view>
	<view style="padding: 20px; background-color: aliceblue;">
		<view style="font-size: 40px; text-align: center; font-family: 'Times New Roman', Times, serif;">模型图</view>
		<view style="width: 100%; text-align: center;">
			<img src="@/static/main.jpg" alt="" style="width: 77%;">
		</view>
		
	</view>
    <view class="table">
	  <view v-for="(data, tableIndex) in tableDatas" :key="tableIndex" style="background-color: #f5f5f5; margin-bottom: 10px;">
		  
		  <view style="text-align: center; display: flex; background-color: #aaafdd; font-weight: 700; font-size: 20px;" class="cell">
		  		  <view style="width: 20%;">文本{{tableIndex + 1}}：</view>
		  		  <view style="width: 80%; text-align: left; " v-html="formatText(data.text, data.boldWords)"></view>
		  </view>
		  <view class="row header-row">
		  		<text class="cell">model</text>
		  		<text class="cell">audio</text>
		    <text class="cell">流畅度分数</text>
		    <text class="cell">xxx感知分数</text>
		  </view>
		  <view v-for="(row, rowIndex) in data.tableData" :key="rowIndex" class="row">
		  	<text class="cell">{{row.model}}</text>
		    <audio :src="row.audio" controls></audio>
		    <input class="cell" @focus="clearInput(row, 'scores1')" style="background-color: antiquewhite;" v-model="row.scores1" type="number" placeholder="流畅度" />
		    <input class="cell" @focus="clearInput(row, 'scores2')" style="background-color: #c8efd4;" v-model="row.scores2" type="number" placeholder="重音" />
		  </view>
		  
		  
	  </view>
		
	  <audio src="@/audio/ground_truth/val/0_0_d2202.wav">11</audio>
	  
	  
	  
    </view>
    <!-- <view class="export-btn" @tap="exportToExcel()">导出EXCEL</view> -->
    <view class="export-btn" @tap="exportToJson()">导出JSON</view>
  </view>
</template>

<script>
	import * as XLSX from 'xlsx';
export default {
	
  data() {
    return {
     tableDatas: [
		 //  --------------   一句话的打分-------------------------------
		 {
		 			"text": "That'd be great. What kind of camera do you have?",
		 					'boldWords': ['great', 'camera'],
		 			 "tableData": [
		 				{model: '语音标签		', audio: require('@/audio/ground_truth/val/9_0_d467.wav'), scores1: 0, scores2: 0},
		 				{model: 'fastspeech2', audio: require('@/audio/fastspeech2/val/9_0_d467.wav'), scores1: 0, scores2: 0},
		 				{model: 'DailyTalk', audio: require('@/audio/dailytalk/val/9_0_d467.wav'), scores1: 0, scores2: 0},
		 				//  ---------增加更多模型的语音------------------
		 			 ],
		 },
		
	 ] ,
    };
  },
  mounted() {
      this.detectDevice();
    },
  methods: {
	  formatText(text, boldWords) {
	        // 定义要加粗显示的单词列表
	        // 构建正则表达式，用于匹配多个单词
	        const regex = new RegExp(`\\b(${boldWords.join('|')})\\b`, 'gi');
	  
	        // 使用正则表达式替换文本中匹配的单词，用 <span> 标签包裹
	        return text.replace(regex, '<span style="font-weight: bold; color: red;">$1</span>');
	      },
    exportToExcel() {
       const wb = XLSX.utils.book_new();

       this.tableDatas.forEach((table, index) => {
         const ws = XLSX.utils.json_to_sheet(table.tableData);
         XLSX.utils.book_append_sheet(wb, ws, `Sheet${index + 1}`);
       });

       XLSX.writeFile(wb, 'ER-CTTS打分.xlsx');
     },
	 
	 exportToJson() {
	       const jsonData = JSON.stringify(this.tableDatas, null, 2);
	       const blob = new Blob([jsonData], { type: 'application/json' });
	       const url = URL.createObjectURL(blob);
	 
	       const a = document.createElement('a');
	       a.href = url;
	       a.download = 'output.json';
	       a.click();
	 
	       URL.revokeObjectURL(url);
	     },
		 
	clearInput(row, key) {
	      // This function clears the input when it is focused
	      row[key] = '';
	    },
		
	detectDevice() {
	      uni.getSystemInfo({
	        success: (res) => {
	          // 判断设备类型，如果屏幕宽度小于某个阈值，认为是手机端
	          if (res.screenWidth <= 768) {
	            this.isMobile = true;
	            uni.showModal({
	              title: 's2lab小提示',
	              content: '请使用pc网页访问,点击进入小游戏',
	              showCancel: false,
	              success: (res) => {
	                if (res.confirm) {
	                  // 用户点击确定后的操作，例如跳转到网页端链接
	                  uni.navigateTo({ url: '/pages/index/game' });
	                }
	              },
	            });
	          }
	        },
	      });
	    },
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.header {
  font-size: 24px;
  text-align: center;
  margin-bottom: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.row {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ddd;
}

.header-row {
  font-weight: bold;
}

.cell {
  flex: 1;
  padding: 10px;
  text-align: center;
}

.export-btn {
  background-color: #4caf50;
  color: white;
  text-align: center;
  padding: 10px;
  margin-top: 20px;
  cursor: pointer;
}
</style>
