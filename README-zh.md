# env-sample-guard

`env-sample-guard` 是一个小型 CLI，用来检查源码中使用的环境变量是否已经写入
`.env.example` 等示例文件。

它通过静态启发式扫描源码，解析示例环境变量文件，并报告：

- 源码使用但示例文件缺失的变量
- 示例文件声明但源码未使用的过期变量
- 适合 CI 使用的确定性 JSON 输出

该工具不会执行项目代码，扫描源码目录时也不会读取真实 `.env` 密钥文件。

## 本地使用

从仓库克隆并在本地检出目录中安装：

```bash
git clone <repository-url>
cd env-sample-guard
python -m pip install -e .[dev]
```

检查当前目录和默认 `.env.example`：

```bash
env-sample-guard check
```

指定源码目录和示例文件：

```bash
env-sample-guard check --source src --source scripts --sample .env.example
```

输出 JSON：

```bash
env-sample-guard check --json
```

将过期变量视为失败：

```bash
env-sample-guard check --strict-stale
```

忽略已知的精确变量名：

```bash
env-sample-guard check --ignore CI --ignore NODE_ENV
```

按命名空间前缀忽略变量：

```bash
env-sample-guard check --ignore-prefix GITHUB_ --ignore-prefix AWS_
```

前缀忽略会从已使用、已声明、缺失和过期结果中排除匹配的变量名。

## 开发

```bash
python -m pytest -q
ruff check .
ruff format --check .
python -m build
```

## 许可证

MIT。详情见 [LICENSE](LICENSE)。
