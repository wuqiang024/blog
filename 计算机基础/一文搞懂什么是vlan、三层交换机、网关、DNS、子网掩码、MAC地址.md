# 一文搞懂什么是 vlan、三层交换机、网关、DNS、子网掩码、MAC地址
***
## 什么是VLAN
***
VLAN中文是“虚拟局域网”。LAN可以是由少数几台家用计算机构成的网络，也可以是数以百计的计算机构成的企业网络。VLAN所指的LAN特指使用路由器分割的网络---也就是广播域。

听上面的概念，肯定不少朋友一头雾水，什么是虚拟局域网？好好的，为什么要划分vlan?

这里举个例子: 通俗的了解
一所高中，新学期高一招了800个学生，这800个学生，如果放在一个班里，那肯定管理不过来，面对800个人，老师看了也头疼，这边在授课，那边完全听不到，老师布置什么任务，也会有些传达不到，老师要是想找到某个学生的信息，要从800份信息中去找，极其麻烦，浪费时间。

而实际中，也是一样，电脑A要想跟电脑B通信，于是电脑A就需要发送arp请求，而网络中电脑众多，最终ARP请求会被转发到同一网络中的所有电脑，才能找到电脑B，如此一来，为了找电脑B，消耗了网络整体的带宽，收到广播信息的计算机还要消耗一部分CPU来对他进行处理。造成了网络带宽和CPU运算能力的大量无谓消耗。

那怎么办？

学习就针对这800个学生，分成了10个班，每个班80人，分别命名为高一(1)班到高一(10)班，每个人都会获得一个班级编号。

1101代表一班01号学生
1102代表一班02号学生
1201代表二班01号学生

同一个班的学生编号尾数不同，其他都相同。

那么这样老师管理起来就轻松多了，可以把这一班80人管理的妥妥的，隔壁2班与3班乱成一锅粥也不管一班的事，我就要这一班80人好好上课就行。

这就是VLAN，每个班就相当于一个VLAN,而每个班的名称，就相当于VLAN的名称，而每个学生的编号就是IP地址，同班同学(同一个VLAN的ip)，因为同一个教室，朝夕相处，可以互相通信，而不同班的同学，若不做其他工作，很难往来通信。

所以同一个VLAN之间，可以互相通信，不同VLAN，若不做配置，不能互相通信。

那么不同VLAN之间如何通信呢？那就需要单臂路由与三层交换机。

## 单臂路由与三层交换机
***
我们知道要实现不同VLAN之间的通信，就必须要有路由功能，不同VLAN之间相互通信的方式有两种(单臂路由，三层交换机)

### 什么是单臂路由
***
单笔路由的实现方式，其实就是普通二层交换机加路由器，从而实现不同VLAN之间的可以互相通信。

![https://mmbiz.qpic.cn/mmbiz_png/p7nzJgwSeowBWBwJ0pnJRI9S9GD7FSV5lmx0O3zg0aX4JnExPYA1iaTy3aQ9nAzHcbxyfPb1Tict4h3Miaj4rJlPA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/p7nzJgwSeowBWBwJ0pnJRI9S9GD7FSV5lmx0O3zg0aX4JnExPYA1iaTy3aQ9nAzHcbxyfPb1Tict4h3Miaj4rJlPA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### 什么是三层交换机
***
对于小型的网络，单笔路由可以应付，但随着VLAN之间流量的不断增加，很可能导致路由器称为整个网络的瓶颈，出现掉包，或者通信堵塞。

为了解决上述问题，三层交换机应运而生。三层交换机，本质上就是带有路由功能的二层交换机。路由属于OSI参照模型中第三层网络层的功能，因此带有第三层路由功能的交换机才叫三层交换机。

关于三层交换机的内部结构可以参照下面的简图。

![https://mmbiz.qpic.cn/mmbiz_png/p7nzJgwSeowBWBwJ0pnJRI9S9GD7FSV58ykMEeR6woISbZh1TLt2sQy62iaJsFm4Dib10Q31yibCs6cS47Tu9C1zA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1](https://mmbiz.qpic.cn/mmbiz_png/p7nzJgwSeowBWBwJ0pnJRI9S9GD7FSV58ykMEeR6woISbZh1TLt2sQy62iaJsFm4Dib10Q31yibCs6cS47Tu9C1zA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

