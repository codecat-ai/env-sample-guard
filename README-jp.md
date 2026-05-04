# env-sample-guard

`env-sample-guard` は、ソースコードで使われている環境変数が
`.env.example` などのサンプルファイルに記載されているかを確認する小さな CLI
です。

静的なヒューリスティックでソースを走査し、サンプル env ファイルを解析して、
次の内容を報告します。

- コードでは使われているがサンプルにない変数
- サンプルにはあるがコードでは見つからない古い変数
- CI で扱いやすい決定的な JSON 出力

このツールはプロジェクトのコードを実行しません。また、ソースディレクトリの
走査中に実際の `.env` 秘密ファイルを読みません。

## ローカルでの使い方

リポジトリをクローンし、ローカルのチェックアウトからインストールします。

```bash
git clone <repository-url>
cd env-sample-guard
python -m pip install -e .[dev]
```

現在のディレクトリを既定の `.env.example` と照合します。

```bash
env-sample-guard check
```

ソースパスとサンプルファイルを指定します。

```bash
env-sample-guard check --source src --source scripts --sample .env.example
```

JSON を出力します。

```bash
env-sample-guard check --json
```

古い変数を失敗として扱います。

```bash
env-sample-guard check --strict-stale
```

既知の変数を無視します。

```bash
env-sample-guard check --ignore CI --ignore NODE_ENV
```

## 開発

```bash
python -m pytest -q
ruff check .
ruff format --check .
python -m build
```

## ライセンス

MIT。詳しくは [LICENSE](LICENSE) を参照してください。
