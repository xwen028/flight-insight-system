# 使用官方的 Node.js 作为基础镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装项目依赖
RUN npm install

# 复制项目的所有文件到工作目录
COPY . .

# 构建项目
RUN npm run build

# 安装一个简单的 web 服务器 serve
RUN npm install -g serve

# 暴露端口 3000
EXPOSE 3000

# 使用 serve 运行构建后的应用
CMD ["serve", "-s", "build", "-l", "3000"]