## mbed_final  
# 車子運作流程  
首先我先將我的車子放在已經劃記好的直線前面。開始之後會先沿著那條直線往前走，之後走到一個距離並偵測到前方障礙物之後會停下來，接下來會先向左轉90度並開始繞過前方障礙物(繞半圈繞過去到障礙物另一邊)。
繞完之後會面對一個木板，如果距離木板小於70公分(用ping量測)的話就繼續下一步，如果沒有小於70公分就直走直到小於70公分。接下來會再繞過第二個障礙物(一樣繞半圈到障礙物後方)。繞完之後會停下來並開始倒車入庫。
倒完車之後會偵測AprilTag以校正自己的位置，並完成整個流程。  

# UART之間的運作以及code實作方法  
在車子開始運作之前，連接到VMWare(電腦)的Xbee(python code)會傳一個RPC function call給我的mbed車子，這個RPC叫做xbee_start，是用來讓車子執行整趟流程的最初指令。這個最初的function其實並沒有做什麼事情，只有用UART傳指令(指令是"line"，意思是該開始偵測直線了)給OpemMV讓其開始偵測直線(有指令之後才會開始偵測)。  
![](https://i.imgur.com/eT6fIod.png)  
我沿著直線走的方法是一直讓OpenMV用UART傳RPC(這個RPC function叫做line_det)給我的車子，每一次RPC都會判斷該走直線還是校正，在正負5個像素的誤差容忍範圍內都會走直線，不然就要朝左或右校正，而判斷的基準是OpenMV那邊傳給mbed的參數(線段兩端點座標)。當走到一個定點之後沿著直線走的部分就結束了，這時OpenMV就不會再繼續偵測直線，所以就不會傳沿直線走的RPC給mbed(車子就不會繼續沿直線走)，取而代之的是OpenMV會傳一個叫做stop的RPC call給mbed讓車子先停一下，並且會偵測到前方障礙物。接著在這個stop的RPC function裡面會傳一組指令給連接電腦的Xbee(這個指令叫做"circle")，當電腦的Xbee收到這個指令之後連接電腦的Xbee(python code)就會回傳一個叫做circle的RPC function call給mbed以讓車子可以繞過障礙物。在我的cpp的code當中就是先左轉90度然後從障礙物左方繞半圈到障礙物後方，繞完之後繼續直走直到ping感測到距離木板小於70公分為止。此時車子會停下來並利用Xbee再傳一次指令給連接電腦的Xbee(指令一樣是"circle")，連接電腦的Xbee一樣會傳叫做circle的RPC給mbed以繞過另外一個障礙物。但要注意我這裡的circle跟第一次繞是一樣的RPC function，只是我用一個flag來判斷現在是要繞第一次還是第二次。繞過第二個障礙物是從它的右邊繞過去到它的後方，繞完之後一樣會停下來，並利用Xbee傳給電腦一個指令叫做"parking"，然後連接電腦的Xbee就會再回傳一個叫做parking的RPC call給mbed以讓車子可以倒車入庫。  
最後就來到了倒數第二個步驟，也就是倒車入庫，這裡的倒車入庫原則上跟作業4的part1差不多，一樣是可以自己設置停車格的位置以及方向再把這些加在parking這個RPC call的參數裡面，車子收到RPC之後就會開始倒車入庫了，倒完車停下來之後mbed一樣會傳一個指令給連接電腦的Xbee(指令叫做"stop")，這樣是要告訴Xbee可以不用再傳RPC給mbed了，同時mbed也會傳一組指令叫做"calib"給我的OpenMV，讓OpenMV開始偵測AprilTag。  
OpenMV偵測到AprilTag之後就會把角度以及距離等參數利用UART傳RPC call給mbed來做calibration的動作(垂直面對AprilTag)，會一直重複偵測直到垂直的程度有在可接受的誤差範圍內。  

# 車子外觀(接線)、場地外觀以及demo的雲端連結  
![](https://i.imgur.com/8H99bLU.jpg)  
![](https://i.imgur.com/Wvqw4p9.png)  
![](https://i.imgur.com/0GqSeCs.png)  
![image](https://user-images.githubusercontent.com/72603727/122420048-f3bdc180-cfbd-11eb-830b-ea52ca88fd08.png)  
![image](https://user-images.githubusercontent.com/72603727/122419824-ca9d3100-cfbd-11eb-9858-7dd57a60a4f2.png)  
https://drive.google.com/file/d/1-PIMn1-S9WkqdZT0N5rAAt8_HCK3cuUN/view?usp=sharing
