# android studio安装时设置了代理导致无法联网
***

一般会在左上角preference里头system settings里将proxy设置为proxy，但是发现还是没用，需要找到项目文件中的全局属性，在gradle scripts的gradle.properties里头，将代理删掉。