# Hatch UI 视觉系统

这份参考资料定义 Hatch 产品 UI 当前已经确定的视觉基础。它是产品界面、Web/Desktop 体验和 Agent 输出界面做视觉判断时的共享上下文；它不是完整的品牌识别手册，也不覆盖平面宣传物料、社交媒体模板或营销 campaign。

## 使用原则

- 涉及 Hatch UI、品牌表现、视觉系统、设计 token、字体、动效或 Atmospheric 时，按需读取本文件。
- 具体实现以公开 `hatch` 仓库的 `packages/brand` 与 `packages/ui` 为 source of truth；本文件用于解释意图和关键约束，不复制第二份实现。
- 不要在产品 app 中创建第二套颜色、字体、组件、渐变或动效 token。新增视觉角色应先更新共享 brand token，再更新 `@hatch/ui` 和产品消费者。
- Web、Tauri Desktop 与 Storybook 使用同一套 `@hatch/ui`；Storybook fixture 只能用于展示组件状态，不能作为产品运行时 fallback。

skill 内的可携带快照：

- [`visual-system/hatch-mark.svg`](visual-system/hatch-mark.svg)：当前正式 mark 的 SVG。
- [`visual-system/tokens.css`](visual-system/tokens.css)：当前完整 brand/UI token 快照。
- [`visual-system/README.md`](visual-system/README.md)：共享 UI design system 的消费与交互说明。

公开实现入口：

- [`packages/brand/tokens.css`](https://github.com/keithhchen/hatch/blob/master/packages/brand/tokens.css)：共享颜色、字体、类型尺度、圆角、阴影、动效和 Atmospheric 参数。
- [`packages/brand/hatch-mark.svg`](https://github.com/keithhchen/hatch/blob/master/packages/brand/hatch-mark.svg)：Hatch mark 资产。
- [`packages/ui/README.md`](https://github.com/keithhchen/hatch/blob/master/packages/ui/README.md)：共享 React design system 的消费方式和边界。
- [`packages/ui/src/HatchBrand.jsx`](https://github.com/keithhchen/hatch/blob/master/packages/ui/src/HatchBrand.jsx)：Wordmark 组件。
- [`packages/ui/src/AtmosphericPaper.jsx`](https://github.com/keithhchen/hatch/blob/master/packages/ui/src/AtmosphericPaper.jsx)：Atmospheric Paper 组件。
- [`packages/ui/src/hatch-ui.css`](https://github.com/keithhchen/hatch/blob/master/packages/ui/src/hatch-ui.css)：共享 UI CSS 和主题实现。

skill 内的快照用于在没有 `hatch` 源码 checkout 时读取这套定义；如果快照与公开实现出现差异，涉及当前实现的任务以公开 `hatch` 仓库为准，并应更新快照而不是维护两套长期 authority。

## Hatch identity

- Mark 是深色圆角方形中的圆形渐变：暖白 → 金色 → 赤陶色。
- Wordmark 使用 `Instrument Serif`，中文回退到 `Noto Serif SC` / 系统衬线字体。
- Wordmark 的句点使用 Hatch accent；不要用临时 glyph、emoji 或其他占位图形替代正式 mark/wordmark。
- 标题可以使用 display serif；UI 正文和控件使用 system sans；pill、label 和 mono 信息使用 Inter 系列。
- display serif 使用轻微负 tracking 和紧凑 leading；UI sans、中文 fallback glyph 和 controls 保持正常字距。

## Color and surfaces

当前视觉基调是温暖的纸面中性色，配合低饱和的 clay、ochre、moss 色彩。关键 semantic token 包括：

- Canvas / paper：`#f3ede3`；Atmospheric base：`#f3efe8`。
- Ink：`#000000`；主 accent：`#a64e35`；accent hover：`#8f402d`。
- Panel：`#fbf7f0`；muted panel：`#ece4d8`；inverse surface：`#202522`。
- 语义状态使用 moss / amber / danger 的低饱和背景与深色文字，不把颜色只当装饰。
- Surface 层级通过透明度、细边框、内外阴影和 paper 色差表达；不要为每个页面重新发明渐变背景。

上述值只能通过共享 tokens 消费。若视觉判断需要新的语义角色，应先确认是否真的是新的角色，而不是在消费者 CSS 中加一个近似色。

## Atmospheric Paper

Atmospheric Paper 是 Hatch 的环境层：它描述光和色彩在一个表面上的缓慢变化，不模拟信纸、收据、书本或其他实体物件。

- 基底是暖白纸面。
- warm field 使用 clay / amber；cool field 使用 moss / amber，作为低对比度的环境色场。
- 当前共享参数：strength `.72`、grain `.045`、warm blur `30px`、cool blur `38px`、warm duration `30s`、cool duration `36s`。
- grain 是轻微的纸面噪声，必须保持克制，不能影响文本可读性。
- 通过 `AtmosphericPaper` 和共享 gradient recipe 使用；不要在产品消费者里复制一套 radial-gradient 或固定动画。
- 背景 artwork 不是文本对比度的依赖；文字和控件必须在没有背景艺术效果时仍满足可读性。

## Motion

动效用于表达状态变化、层级和空间关系，而不是持续吸引注意力：

- control：`150ms cubic-bezier(.4, 0, .2, 1)`
- popover：`180ms cubic-bezier(.455, .03, .515, .955)`
- layout：`260ms cubic-bezier(.43, .07, .59, .94)`
- 控件 hover、focus、active、popover、dialog、drawer、tabs 和布局变化应消费 semantic motion token。
- Atmospheric 的慢速变化属于环境层，不能替代交互反馈，也不能让核心操作产生不必要的等待感。
- 需要减少动效时，应保留状态和层级信息，避免把 motion 当成产品逻辑。

## Scope boundary

当前 Hatch UI 视觉定义到这里为止已经足够支撑产品建设：Wordmark、色彩、字体、surface、Atmospheric Paper 和 motion。除非出现明确产品需求，不要把这份 UI reference 扩展成完整平面设计或营销品牌规范。
