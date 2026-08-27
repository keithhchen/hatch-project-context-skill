# Hatch Project Context Skill

这个仓库同时提供两种入口，正文保持一致：

- OpenAI/Codex：根目录的 `SKILL.md` 和 `agents/openai.yaml`。
- Anthropic Agent Skills：`skills/hatch-project-context/`，这是一个可独立安装的纯 skill 目录，包含 `SKILL.md` 和自己的 `references/`。

Anthropic 入口就是独立纯 skill；将 `skills/hatch-project-context/` 目录复制到目标 Agent 的 skills 目录即可。

```bash
python3 scripts/validate_skill.py
```

OpenAI/Codex 入口继续使用原来的 `$hatch-project-context` skill。若将仓库作为本地 skill 目录使用，目录名应为 `hatch-project-context`，以便与 `SKILL.md` 的 `name` 对齐。

本地开发完成后运行以下检查，确保两个入口没有产生漂移：

```bash
python3 scripts/validate_skill.py
```

Hatch UI 的产品视觉定义位于 `references/visual-system.md`，两个入口各自维护一份以保持独立安装可用；其中的 `references/visual-system/` 还携带 `hatch-mark.svg`、完整 `tokens.css` 和 UI README 快照。它覆盖 Wordmark、色彩、字体、surface、Atmospheric Paper 与 motion；具体实现仍以公开 `hatch` 仓库的 `packages/brand` 和 `packages/ui` 为准，不扩展为完整平面品牌手册。

`feishu-cli` 是这个 skill 的必需 dependency，对应的命令是 `lark-cli`。读取飞书资料需要网络访问和已有认证；如果检测不到 `lark-cli`，skill 会提示：

`帮我安装飞书 CLI：https://open.feishu.cn/document/no_class/mcp-archive/feishu-cli-installation-guide.md`

更多详情：[Feishu CLI](https://www.feishu.cn/feishu-cli)

如果命令不在 `PATH`，可通过 `LARK_CLI_BIN` 指定其路径。
