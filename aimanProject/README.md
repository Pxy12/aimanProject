# 中国指数网数据获取与解密项目

## 项目简介

本项目是一个用于从中国指数网获取娱乐频道数据并进行解密的Python应用程序。通过调用JavaScript函数生成签名并解密返回的数据，实现了对不同频道（如电影、综艺、爱情等）数据的获取与处理。

## 功能特点

1. **多频道数据获取**：支持通过配置不同的`word`变量获取不同频道的数据
2. **动态签名生成**：使用Node.js执行JavaScript代码调用`signDecrypt.js`中的`Ny`函数生成请求签名
3. **自动数据解密**：检测响应数据是否加密，如需要则调用`dataDecrypt.js`中的`dataFilter`函数进行解密
4. **结果保存**：将解密后的数据保存为JSON文件，方便后续分析
5. **异常处理**：包含完善的错误处理和备用签名机制，确保程序稳定运行

## 项目结构

```
├── decrypt.py           # 主程序文件，实现数据获取与解密流程
├── signDecrypt.js       # 包含签名生成函数Ny的JavaScript文件
├── dataDecrypt.js       # 包含数据解密函数dataFilter的JavaScript文件
├── requirements.txt     # Python依赖文件
├── decrypted_result_*.json # 解密结果保存文件
```

## 环境要求

- **Python 3.6+**
- **Node.js**：用于执行JavaScript代码生成签名和解密数据
- **Python依赖**：requests库

## 安装说明

1. 确保已安装Python 3.6+和Node.js
2. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 确保`signDecrypt.js`和`dataDecrypt.js`文件存在于项目根目录

## 使用方法

1. 修改`decrypt.py`文件中的`word`变量，设置需要获取的频道：
   ```python
   # 支持的值：'movielist', 'varietylist', '爱情'等
   word = '爱情'
   ```

2. 运行程序：
   ```bash
   python decrypt.py
   ```

3. 程序执行流程：
   - 调用JavaScript获取签名
   - 发送GET请求获取数据
   - 检测数据是否加密，如需要则进行解密
   - 将解密结果保存为JSON文件

## 配置指南

1. **频道配置**：修改`word`变量的值以获取不同频道的数据
2. **请求参数配置**：可以在代码中修改`cookies`和`headers`以适应不同的请求需求
3. **签名参数配置**：`url_info`、`data_info`和`other_info`参数可以根据API要求进行调整

## 输出说明

1. 控制台输出包含详细的执行日志，包括签名获取、请求发送、解密过程等信息
2. 解密结果保存在`decrypted_result_{word}.json`文件中
3. 如遇错误，控制台会显示详细的错误信息

## 注意事项

1. 确保`signDecrypt.js`中包含有效的`Ny`函数
2. 确保`dataDecrypt.js`中包含有效的`dataFilter`函数
3. 如遇到签名生成失败，程序会使用备用固定签名进行请求
4. 建议定期更新`cookies`以确保请求成功

## 故障排除

- **签名获取失败**：检查`signDecrypt.js`文件是否存在，以及`Ny`函数是否正确定义
- **解密失败**：检查`dataDecrypt.js`文件是否存在，以及`dataFilter`函数是否正确定义
- **请求失败**：检查网络连接、`cookies`和`headers`是否有效

## 版本信息

程序启动时会显示Python版本、操作系统信息和Node.js版本

## 许可证

保留所有权利