#!/bin/bash

if [ $# != 1 ]
then
    echo "USAGE: $0 filename"
    exit 1
fi

# 先按搜索引擎排序 然后按照记录时间 排序 观看引擎随时间的变化 响应时间的变化
cat $1 | grep networkTest | awk '{print $7,$5,$8}' | sort -k1,1 -k2,2 > $1.time.log

#按照请求的响应时间排序 观看响应时间最大的在什么时间点和发生在哪一个引擎
cat $1 | grep networkTest | awk '{print $8,$7,$5}' | sort -k1r > $1.max.log

#计算总的平均响应时间
echo "总体平均响应时间"
cat $1 | grep networkTest | awk '{sum+=$8}END{print "sum=",sum," Averge=",sum/NR}'

#计算每个引擎的总时间
echo "引擎 总时间"
cat $1 | grep networkTest | awk '{sum[$7]+=$8} END{for(i in sum) print i,sum[i]}'

#计算每个引擎的请求数目
echo "引擎 次数"
cat $1 | grep networkTest | awk '{print $7}'| sort -k1 | uniq -c | awk '{print $2,$1}'

echo "引擎 平均"
cat $1 | grep networkTest | awk '{sum[$7]+=$8;count[$7]+=1} END{for(i in sum) print i,sum[i]/count[i]}'
