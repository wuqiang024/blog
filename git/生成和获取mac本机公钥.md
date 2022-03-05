<!--
 * @Author: your name
 * @Date: 2022-03-05 14:08:45
 * @LastEditTime: 2022-03-05 14:10:07
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /blog/git/生成和获取mac本机公钥.md
-->
# 生成和获取mac本机公钥
***
`ssh-keygen -t rsa`
`cat ~/.ssh/id_rsa.pub`

一路回车~
如果想复制文件到相关文件夹，就：
`cp ~/.ssh/id_rsa.pub + 相应路径`