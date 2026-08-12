# 发布到 GitHub（SSH 方式）

> 本项目已在本地完成 Git 初始化与提交；发布时推荐使用 SSH 远程地址，避免 HTTPS Token 认证和网络层波动带来的麻烦。

## 发布前检查

- 当前分支：`main`
- 作者署名：`tanchunzhuo`
- 不要把真实简历、身份证号、手机号、公司机密或任何 `workspace/` 工作数据提交到公开仓库。
- 在 GitHub 新建一个**空仓库**，建议名为 `ai-career-position`；创建时不要勾选 README、`.gitignore` 或 License（本地已有）。

## 1. 确认 GitHub 账户 ID

仓库地址使用的是 GitHub 的 **账户 ID（username）**，不是 Settings 中可随意填写的显示昵称（Name）。

例如个人主页为：

```text
https://github.com/tanchunzhuo
```

则 SSH 远程地址应为：

```text
git@github.com:tanchunzhuo/ai-career-position.git
```

请将下面命令中的 `你的账户ID` 替换为个人主页 URL 中的那一段。

## 2. 第一次配置 SSH 密钥（仅需一次）

如你的电脑尚未配置 GitHub SSH 密钥，在**你自己的电脑终端**执行：

```bash
ssh-keygen -t ed25519 -C "你的GitHub注册邮箱"
```

一路按提示操作即可；建议为私钥设置口令。随后打印公钥：

```bash
cat ~/.ssh/id_ed25519.pub
```

复制整行内容，前往 GitHub：**头像 → Settings → SSH and GPG keys → New SSH key**，粘贴并保存。

验证连接：

```bash
ssh -T git@github.com
```

首次询问主机指纹时，确认是 GitHub 后输入 `yes`。成功时会看到 GitHub 的认证欢迎提示（GitHub 不提供 shell 登录是正常的）。

> 私钥文件 `~/.ssh/id_ed25519` 绝不能上传、发送或粘贴给任何人；只添加后缀为 `.pub` 的公钥。

## 3. 推送本项目

解压本项目压缩包后进入项目目录，执行：

```bash
cd ai-career-position
git status
git remote add origin git@github.com:你的账户ID/ai-career-position.git
git push -u origin main
```

如果此前已经设置过 `origin`，改用：

```bash
git remote set-url origin git@github.com:你的账户ID/ai-career-position.git
git push -u origin main
```

## 4. 日常更新

每次修改后建议先检查变更，再提交推送：

```bash
git status
git add .
git commit -m "feat: 简要说明本次更新"
git push
```

在 `git add .` 前，务必确认没有把个人求职资料、密钥或其他敏感信息加入暂存区。

## 常见问题

### `Repository not found`

通常是下列原因之一：

1. `你的账户ID` 写成了显示昵称，而不是 GitHub URL 中的 username；
2. GitHub 仓库名拼写不一致；
3. 当前 SSH 密钥绑定的是另一个 GitHub 账号；
4. 仓库尚未创建，或你没有其写入权限。

查看当前远程地址：

```bash
git remote -v
```

账号 ID 或仓库名变化后，立即更新：

```bash
git remote set-url origin git@github.com:新的账户ID/新的仓库名.git
```

### SSH 的 22 端口被网络限制

可使用 GitHub 的 SSH over port 443。创建或编辑 `~/.ssh/config`：

```sshconfig
Host github.com
  Hostname ssh.github.com
  Port 443
  User git
```

然后重新测试 `ssh -T git@github.com` 并推送。此配置只应在确认 22 端口受限时使用。

### `Permission denied (publickey)`

重新确认公钥已添加到正确的 GitHub 账号，并检查本机私钥权限与 SSH agent 配置；不要改用复制私钥的方式解决问题。
