# Tulong Server

Tulong项目Python服务端，基于flask服务框架，核心识别使用OpenCV

## 安装依赖：

项目使用poetry配置虚拟环境和管理代码依赖，需事先全局安装：

```sh
pip install -r requirements.txt
```

## 启动服务

### 本地启动服务

```sh
flask run
```

建议使用vscode进行开发调试

### 部署服务

部署使用uwsgi + Nginx

