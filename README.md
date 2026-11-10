# 课程设计专家 Skill

帮助你从课程定位、学员起点和目标出发，设计课程阶段、逐课框架、交付标准及反馈安排。课程框架确定后，如果你明确要求单课教学设计，还可按需要使用知识课、长课或体验课参考。

## 安装到 Codex

在 Codex 中告诉 `$skill-installer`：

> 从 `littlexiaohui/course-design-expert` 安装 Skill，仓库根目录是 Skill 路径 `.`，安装名为 `course-design-expert`。

也可以在 macOS 或 Linux 终端运行安装器（要求本机已安装 Codex 和 Python 3）：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo littlexiaohui/course-design-expert --path . --name course-design-expert
```

如果目标 Skill 已存在，安装器会停止以避免覆盖；请先按下文确认安装方式并备份。安装完成后，在 Codex 的下一轮对话中使用即可。其他系统可以优先使用上面的 `$skill-installer` 对话方式。

另一种方式是在目标目录不存在时直接克隆（macOS 或 Linux）：

```bash
git clone https://github.com/littlexiaohui/course-design-expert.git ~/.codex/skills/course-design-expert
```

## 使用示例

可直接描述需求，也可以显式指定 Skill。例如：

> `$course-design-expert` 帮我设计一门面向零基础成年人的手机摄影入门课。每周一次，共四周，线上直播。请先明确学员起点、课程目标和适合的组织路线。

完成定位与所需路线选择后，Skill 可以继续输出阶段目标、逐课框架、交付标准和反馈安排。若已有确定的课程框架，也可以明确说：“请把其中一节课设计成包含示范、练习和反馈的教案。”单课设计是按需使用的下游参考；讲稿、课件和运营方案须按需要另行要求。

已有信息和明确要求优先；不必预先整理成课程术语。输出是设计建议，不能替代学科专业审核或真实试教。

## 更新已安装的 Skill

**先确认当前安装目录的类型和位置，保留自己的修改。** 如果它是符号链接，或位于其他项目的工作区，先确认真实编辑源和维护方式；不要直接覆盖，也不要因为上级目录恰好有 Git 仓库就对它执行下面的更新命令。

### 用 Git 克隆安装

先检查安装目录本身是否为这个仓库的克隆、`origin` 是否指向本仓库，以及是否有未提交或未跟踪的个人文件：

```bash
git -C ~/.codex/skills/course-design-expert rev-parse --show-toplevel
git -C ~/.codex/skills/course-design-expert remote get-url origin
git -C ~/.codex/skills/course-design-expert status --short --untracked-files=all
```

确认仓库根目录就是安装目录、远端正确且没有需要保留的未提交改动后，再更新：

```bash
git -C ~/.codex/skills/course-design-expert pull --ff-only
```

### 用安装器下载

安装器下载的目录通常不含 Git 历史，不能直接用 `git pull`。确认它是普通目录而非符号链接后，先将原目录备份或重命名到一个**不存在的新位置**，然后重新运行上面的安装器命令。安装失败时保留备份并恢复；确认新版本可用后，再自行处理备份。

如果需要安装一个已确认的标签或提交，可在安装器命令后增加 `--ref` 和对应版本标识。使用 `main` 会获取当时的默认版本；更新内容与本地修改冲突时先比较，不强制覆盖。

## 来源与使用许可

运行所需参考文件在本仓库内。部分单课设计建议借鉴未随包分发的私人课程转写或研究材料，使用者可能无法独立核验原件；[来源状态](references/单课设计来源与证据状态.md)说明了可用范围与未核事项。案例标识经过匿名化，不提供私人原件、来源映射或账号信息。

本仓库允许个人下载、安装和使用；未经权利人授权，不开放修改或再分发。具体范围见[个人使用许可](LICENSE)；这不是允许自由修改和再分发的开源许可证。GitHub 公开仓库在平台上的浏览、fork 等仍受 [GitHub 服务条款](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)约束。

## 维护

本仓库是可安装的分发仓库。原维护者的编辑源位于其工作区的 `skill-sources/course-design-expert`；安装目录用于运行，本机若以符号链接指向编辑源，应先确认链接目标，不要把安装副本误认为编辑源。维护和发布须在权利人授权范围内进行。

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

`--check` 只比较清单文件与所选来源，不能证明来源正确或内容适合公开。链接脚本仅检查文字与路径均不含嵌套括号、且没有标题的行内相对文件链接；复杂链接需人工核查，脚本也不核对网页或章节锚点。格式检查需要本机有 Codex 的 `skill-creator` 和 `uv`。同步脚本只复制文件，不提交或推送。

发布前还要检查未跟踪文件及将进入提交的完整内容和 Git 历史，确认不包含私人原件、来源映射、账号信息或许可未核的原文；新增来源和文件须先审核。对受修改影响的典型用例运行一次 Skill，记录实际读取的文件和结果；模拟不等于真实教学效果。当前任务包含或已授权发布时，再提交并推送。
