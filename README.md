# Hatch Project Context Skill

这个仓库同时提供两种入口，正文保持一致：

- OpenAI/Codex：根目录的 `SKILL.md` 和 `agents/openai.yaml`。
- Anthropic/Claude Code：`.claude-plugin/plugin.json` 和 `skills/hatch-project-context/SKILL.md`。

Claude Code 插件需要从仓库根目录加载；插件会发现 `skills/hatch-project-context/`，该目录包含自己的 `references/`：

```bash
claude plugin validate .
claude --plugin-dir .
```

OpenAI/Codex 入口继续使用原来的 `$hatch-project-context` skill。若将仓库作为本地 skill 目录使用，目录名应为 `hatch-project-context`，以便与 `SKILL.md` 的 `name` 对齐。

本地开发完成后运行以下检查，确保两个入口没有产生漂移：

```bash
python3 scripts/validate_skill.py
```

`feishu-cli` 是这个 skill 的必需 dependency，对应的命令是 `lark-cli`。读取飞书资料需要网络访问和已有认证；如果检测不到 `lark-cli`，skill 会提示：

`帮我安装飞书 CLI：https://open.feishu.cn/document/no_class/mcp-archive/feishu-cli-installation-guide.md`

更多详情：[Feishu CLI](https://www.feishu.cn/feishu-cli)

如果命令不在 `PATH`，可通过 `LARK_CLI_BIN` 指定其路径。
