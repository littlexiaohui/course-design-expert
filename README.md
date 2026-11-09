# 课程设计专家 Skill

帮助你从课程定位、学员起点和目标出发，设计课程阶段、逐课框架、交付标准及反馈安排。课程框架确定后，如果你明确要求单课教学设计，还可按需要使用知识课、长课或体验课参考。

## 安装到 Codex

在 Codex 中告诉 `$skill-installer`：

> 从 `littlexiaohui/course-design-expert` 安装 Skill，仓库根目录是 Skill 路径 `.`，安装名为 `course-design-expert`。

也可以运行安装器（要求本机已安装 Codex）：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo littlexiaohui/course-design-expert --path . --name course-design-expert
```

如果目标 Skill 已存在，安装器会停止以避免覆盖；请先自行确认如何备份或更新。安装完成后，在 Codex 的下一轮对话中使用即可。

另一种方式是在目标目录不存在时直接克隆：

```bash
git clone https://github.com/littlexiaohui/course-design-expert.git ~/.codex/skills/course-design-expert
```

若目标目录已存在，不要直接覆盖。

## 使用示例

- “我想设计一门面向初学者的课程，请先帮我明确学员、目标和课程组织路线。”
- “课程框架已确定，请把其中一节课设计成包含示范、练习和反馈的教案。”

可以直接描述已有材料、学员和交付条件；不必预先整理成课程术语。用户已确定的条件和明确要求优先。技能输出是设计建议，不能替代学科专业审核或真实试教。

## 来源与范围

运行所需参考文件在本仓库内。部分单课设计建议借鉴未随包分发的私人课程转写或研究材料，使用者可能无法独立核验原件；[来源状态](references/单课设计来源与证据状态.md)说明了可用范围与未核事项。本仓库不包含这些原件、私人来源映射或账号信息。

仓库公开供获取和安装；目前未附加额外的开源许可证。

## 维护

本仓库是可安装的分发仓库。原维护者的编辑源位于其工作区的 `skill-sources/course-design-expert`；安装目录用于运行，本机若以符号链接指向编辑源，应先确认链接目标。其他维护者可以在自己的克隆或分叉中维护，不要把安装副本误认为原维护者的编辑源。

从已审核的编辑源同步时，先确认源路径及双方未提交改动，再参照 [AGENTS.md](AGENTS.md)和[同步清单](sync-manifest.json)：

```bash
python3 tools/sync-skill.py --source /path/to/course-design-expert
python3 tools/sync-skill.py --source /path/to/course-design-expert --check
git status --short --untracked-files=all
git diff
git diff --cached
python3 tools/check-links.py
uv run --no-project --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

`--check` 只比较清单文件与所选来源，不能证明来源正确或内容适合公开。链接检查只核对 Markdown 行内相对文件链接，不核对网页或章节锚点；格式检查需要本机有 Codex 的 `skill-creator` 和 `uv`。同步脚本只复制文件，不提交或推送。

发布前还要检查未跟踪文件及将进入提交的完整内容和 Git 历史，确认不包含私人原件、来源映射、账号信息或许可未核的原文；新增来源和文件须先审核。对受修改影响的典型用例运行一次 Skill，记录实际读取的文件和结果；模拟不等于真实教学效果。当前任务包含或已授权发布时，再提交并推送。
