# unityautobuild
Auto build XCode Project or Android Project or APK with Unity

如果需要完美的解决错误，可以两种方式

### 第一种

1. 修改所有UI 界面上用到了 PokerItem 作为 GameObject 名字的部分，并且修改对应的脚本

1. 修改所有 UI 界面上用到了 ScrollView 座位 GameObject 名字的部分，并且修改对应的脚本

1. 将 ViewPay 这个文件夹改名，并修改对应的脚本

1. 之后开发，注意几点

    * 不要使用 Lua 脚本名称作为 GameObject 的名字
    * 不要使用 Lua 脚本的名字作为文件夹的名字
    * 所有的类均以 M 命名
    
### 第二种

1. 在 pack_majia.py 文件中的 ignore_files 数组中加入需要忽略的名字，可以参考已经填写好的字符串，已经填写好的部分是不能删除的
