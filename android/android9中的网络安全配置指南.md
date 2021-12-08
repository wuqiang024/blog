# 安卓9(P)中的网络安全配置指南(network-security-config)
***
随着数据隐私越来越重要，谷歌一直在试图增强移动操作系统的功能，用以保护Android移动设备和端点的所有数据。Android9.0(Pie)的网络通信默认为TLS.为了防止APP链接失败，安卓移动开发人员需要更新后端服务，以支持HTTPS或实现Android网络安全配置功能。

当Android6.0(Marshmallow)发布时，谷歌提出了把android:usesCleartextTraffic作为防止意外使用明文通信的手段，Android7.0(Nougat)通过引入Android网络安全配置特性来扩展这个属性，这使得开发人员进一步规范来安全通信。Android的网络安全配置被称为Network Security Configuration，他是开发人员为Android应用程序定制的一个XML文件。

ios也使用类似的客户端检查配置，就是我们所说的App Transport Security。

`实施优点`

1、防止回归到明文通信
Android Network Security Configuration功能提供来一个简单的层，用来保护应用程序在未加密的明文中意外传输的敏感数据。
它像是一个发送和接收的管理器，检查所有出入站的货物，并在设备进入未经审核的交付系统之前停止装运，它可以用来防止意外地使用不可信的，未加密的链接。

Android9最大的变化之一是在默认情况下，cleartextTrafficPermitted允许被设置为false。这意味着，如果你没有看到这个标志被明确设置为false,并且应用程序的API级别低于28，则该标志将被判断为true。

在Network Security Config中使用的cleartextTrafficPermitted标志的另一个能力，是在特定域和子域上执行真正的设置：

```xml
<network-security-config>
  <domain-config cleartextTrafficPermitted="true">
    <domain includeSubdomains="true">insecure.example.com</domain>
  </domain-config>
  <base-config cleartextTrafficPermitted="false" />
</network-security-config>
```

`cleartextTrafficPermitted = "true"` 代表允许明文发送
`basic-config`里头的`cleartextTrafficePermitted="false"`代表其他域不允许明文发送。

2、为安全连接设置可信证书办法机构
可信证书机构(Trusted Certificate Authorities, CA)可以充当信任中介。开发人员可以使用Android Network Security Configuration功能来指定她们信任哪些CA办法的证书，并确保通信的安全。

首先，Network Security Configuration给开发者提供了一些可选择的CA，默认情况下， Android7+(Nougat, Oreo, Pie)所使用的信任锚将是预先安装的系统CA证书，成为"system(系统)";

```xml
<network-security-config>
  <base-config>
    <trust-anchors>
      <certificates src="system">
    </trust-anchor>
  </base-config>
</network-security-config>

在Android6(Marshmallow)及其以下的版本，默认的信任锚还包括用户安装的证书，称为"user(用户)";

```xml
<network-security-config>
  <base-config>
    <trust-anchors>
      <certificates src="system" />
      <certificates src="user" />
    </trust-anchor>
  </base-config>
</network-security-config>
```

最后可以设置自定义信任锚: Trust Anchors: CustomShell

```xml
<network-security-config>
  <base-config>
    <trust-anchors>
      <certificates src="@raw/my_custom_ca"/>
    </trust-anchor>
  </base-config>
</network-security-config>
```

3、实施证书绑定
***
实施证书锁定又增加了一层安全性。让我们重新回顾一下货物运输的故事，如果可信的CA是诸如UPS、FedEx等的公司，那么证书锁定类似于指定你所信任公司的哪项服务来运送你的货物。Android Network Security Configuration特征可以用来限制仅由可信CA颁发的特定证书用以通信。

我们讨论了在以前所研究过的实现证书锁定的方法，在下面的示例中，我们可以针对特定域和子域，将引脚设置为备份，并设置有效日期。

Certificate Pinning with Network Security ConfigShell

```xml
<network-security-config>
    <domain-config>
        <domain includeSubdomains="true">example.com</domain>
        <pin-set expiration="2018-01-01">
            <pin digest="SHA-256">7HIpactkIAq2Y49orFOOQKurWxmmSFZhBCoQYcRhJ3Y=</pin>
            <!-- backup pin -->
            <pin digest="SHA-256">fwza0LRMXouZHRC8Ei+4PyuldPDcf3UKgO/04cDM1oE=</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

4、调试应用程序网络链接
***
Android Network Security Configuration中提供的另一个选项是调试重写。此特性允许你在Network Security Config中设置只有当android:debuggable为true时才可用。例如，你可以使用自定义CA，为质量保证/预生产环境配置自定义信任锚，这会简化封闭环境测试，因为应用商城不接受标记为可调试的应用程序。
Debug OverridesShell

```xml
<network-security-config>
    <debug-overrides>
        <trust-anchors>
            <certificates src="@raw/debug_cas"/>
        </trust-anchors>
    </debug-overrides>
</network-security-config>
```

## 实施建议
***
已经了解了部署network security configuration的好处，现在来看如何实现。

1、首先检查应用程序清单，看他是否有这个特性。查找`android:networkSecurityConfig`，类似于这样：

```xml
<manifest ...>
  <application android:networkSecurityConfig="@xml/network_security_config">
</manifest>
```

一旦找到了Network Security Config文件，就到了检查如何允许明文通信的时候了。

例如下面的反例代码(Bad Example)

```xml
<network-security-config>
  <domain-config cleartextTrafficPermitted="false">
    <domain includeSubdomains="true">example.com</domain>
    <domain includeSubdomains="true">cdn.example2.com</domain>
  </domain-config>
  <base-config cleartextTrafficPermitted="true" />
</network-security-config>
```

虽然这确保了所有到example.com和cdn.example2.com的通信都是通过HTTPS发送的，但是发送给其他域的所有通信都默认可以是明文，这完全违背了Network Security Config功能的预期目的 => 加强保护通过android设备传输的所有数据的隐私。

推荐写法如下(Good Example):
```xml
<network-security-config>
  <domain-config cleartextTrafficPermitted="true">
    <domain includeSubdomains="true">insecure.example.com</domain>
    <domain includeSubdomains="true">insecure.cdn.example.com</domain>
  </domain-config>
  <base-config cleartextTrafficPermitted="false" />
</network-security-config>
```

再看另一个反例(Bad Example):
```xml
<network-security-example>
  <base-config>
    <trust-anchors>
      <certificates src="system" />
      <certificates src="user" />
    </trust-anchors>
  </base-config>
</network-security-example>
```
在此示例中，我们看到应用程序正在接受其信任锚中的用户证书，这意味着应用程序将以与系统预置证书相同的方式，来信任用户安装的证书。`配置应用程序使用的信任锚时，最好仅限制对系统证书的信任，并在必要时限制应用程序内构建的自定义CA，这有助于防止攻击者能够在设备上安装证书来进行攻击(MITM)`。作为android7中引入的保护措施的一部分，默认情况下，用户安装的证书不像预先安装的证书那样受信任。如前所述，android6及更低版本默认接受用户证书，因此在必要时明确选择system或自定义CA并在所有应用中排除"user(用户)"非常重要。

推荐代码：
```xml
<network-security-config>
  <base-config>
    <trust-anchors>
      <certificates src="system" />
      <certificates src="@raw/CustomA">
    </trust-anchors>
  </base-config>
</network-security-config>
```
`未完待续`
https://blog.csdn.net/hehongdan/article/details/103168380