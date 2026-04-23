import streamlit as st
import streamlit.components.v1 as components

# ================= 新增：控制页面置顶的黑科技 =================
def scroll_to_top():
    # 注入一段隐形的 JS 脚本，强制让包含内容的滚动条回到 0 的位置
    js = """
    <script>
        var body = window.parent.document.querySelector(".main");
        if (body) {
            body.scrollTop = 0;
        }
    </script>
    """
    components.html(js, height=0)

# 1. 初始化页码状态和置顶标记
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1
if 'need_scroll_top' not in st.session_state:
    st.session_state.need_scroll_top = False

# 每次页面刷新时，检查是否需要置顶
if st.session_state.need_scroll_top:
    scroll_to_top()
    st.session_state.need_scroll_top = False # 执行完立刻关掉，防止正常滑动受影响

# 2. 定义翻页函数（绑定点击按钮时的动作）
def next_page():
    st.session_state.page_number += 1
    st.session_state.need_scroll_top = True # 标记：下一页需要回到顶部

def prev_page():
    st.session_state.page_number -= 1
    st.session_state.need_scroll_top = True # 标记：上一页也要回到顶部
# 3. 页面布局容器（保证翻页按钮始终在最下面）
main_container = st.container()

with main_container:
    # ====== 第一页：封面与交互大纲 ======
    if st.session_state.page_number == 1:
        st.markdown("<h1 style='text-align: center;'>让 AI 更准：全阶实战指南</h1>", unsafe_allow_html=True)
        st.write("---")

        st.markdown("### 📅 分享大纲")
        st.write("点击下方章节可直接跳转至对应内容：")

        # 使用两列布局展示大纲按钮
        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("1️⃣ 认知拉齐：用对工具是第一步", use_container_width=True):
                st.session_state.page_number = 2
                st.rerun()
            if st.button("3️⃣ 插件应用：打破 AI 能力盲区", use_container_width = True):
                st.session_state.page_number = 8
                st.rerun()
        with col_b:
            if st.button("2️⃣ 知识库与数据库：从盲猜到开卷", use_container_width=True):
                st.session_state.page_number = 5
                st.rerun()
            if st.button("4️⃣ 多模型协作：建立 AI 数字大军", use_container_width=True):
                st.session_state.page_number = 9
                st.rerun()

        st.write("---")
        st.info("💡 **核心目标**：直击“结果不可控”痛点，提供从小白到高阶的 AI 准确率系统解法。")

        # 底部保留一个全局开始按钮
        st.write("")
        if st.button("顺序开始分享 🚀", type="primary", use_container_width=True):
            st.session_state.page_number = 2
            st.rerun()

    # ====== 第二页：互动游戏 ======
    elif st.session_state.page_number == 2:
        import random

        st.header("第一关：认知拉齐 - 业务场景连连看")
        st.write("不要杀鸡用牛刀。请为下方的真实业务场景，匹配最合适的 AI 武器。")

        # 1. 上下排版：上方先展示武器库（修正了定义，去掉了“定时”这种误导性词汇）
        st.info("🛠️ **武器库 (AI 工具)**\n\n"
                "* **AI 对话 (Chat)**：人类发号施令。一问一答，适合单次、发散、需要脑暴的任务。\n"
                "* **工作流 (Workflow)**：人类设定步骤。像流水线一样严格执行 SOP，适合大批量、路径确定的任务。\n"
                "* **智能体 (Agent)**：人类设定目标。AI 自主做项目经理，自己决定调用什么工具、走什么路径。")

        st.write("---")
        st.subheader("🎯 实战场景匹配")

        # 2. 重新设计题库（强调：确定性步骤 vs 自主决策）
        if 'shuffled_scenarios' not in st.session_state:
            raw_scenarios = {
                "把刚出台的《二手电子产品合规法案》扔给 AI，让它帮我总结 3 个对我们业务影响最大的风险点？": "AI 对话 (Chat)",
                "快速起草一封发给战略合作伙伴（如京东）的阶段性汇报邮件？": "AI 对话 (Chat)",
                "每晚 12 点，自动去邮箱下载各渠道的回收报价单，提取价格并写入飞书多维表格？（注：步骤固定）": "工作流 (Workflow)",
                "批量听取今天所有的门店回收录音，严格按照【打招呼、验机、报价】三个节点进行合规打分？": "工作流 (Workflow)",
                "给AI一个新业务线的目标，AI自己去网上查行业研报、调用分析插件，结合内部其他业务线的数据情况，最后生成一份市场调研 PPT？（注：路径未知）": "智能体 (Agent)",
                "逸飞想搞一个有意思的分享课件，不知道从何下手？": "AI 对话 (Chat)",
                "自动监控客诉系统：自主判断客诉情绪，如果是轻微抱怨就自动发券安抚；如果识别到“打12315投诉”等极端风险，立刻停止自动回复并飞书拉群告警？": "智能体 (Agent)"
            }
            # 将字典转为列表并打乱
            items = list(raw_scenarios.items())
            random.shuffle(items)
            st.session_state.shuffled_scenarios = items

        options = ["请选择...", "AI 对话 (Chat)", "工作流 (Workflow)", "智能体 (Agent)"]
        score = 0

        # 3. 下方展示题目
        for i, (question, correct_answer) in enumerate(st.session_state.shuffled_scenarios):
            user_choice = st.selectbox(f"**场景 {i + 1}：** {question}", options, key=f"q_{i}")

            if user_choice != "请选择...":
                if user_choice == correct_answer:
                    st.success("✅ 选对了！")
                    score += 1
                else:
                    st.error(f"❌ 再想想：这件事的“执行步骤”是死板的还是需要灵活变通的？最合适的是：{correct_answer}")

        if score == len(st.session_state.shuffled_scenarios):
            st.balloons()
            st.success("🏆 满分！你已经完全掌握了给 AI 定岗的精髓！")
    # ====== 第三页：工作流 vs 智能体 ======
    elif st.session_state.page_number == 3:
        st.header("第二关：控制权之争 - 工作流 vs 智能体")
        st.write("它们的核心区别不在于能不能“定时”，而在于：**遇到突发情况，控制权在谁手里？**")

        # 核心金句
        st.info(
            "💡 **速记金句：**\n* **工作流 (Workflow)**：人脑写死 SOP，AI 当苦力（绿皮火车，绝不脱轨，但也绝不绕路）。\n* **智能体 (Agent)**：人脑只给目标，AI 当项目经理（自动驾驶，见机行事）。")
        st.write("---")

        st.subheader("🎯 互动沙盘：处理一次极端的门店客诉")
        st.write(
            "**突发事件：** 系统捕获到一条刚刚生成的门店客诉文本：\n> 😡 *“你们收手机乱压价！店员态度极差！我已经录音了，明天就在抖音曝光你们！”*")

        # 让演示者/观众选择处理模式
        mode = st.radio("请选择指派谁来处理这次危机：",
                        ["请选择...", "👷‍♂️ 指派【工作流】按 SOP 处理", "🦸‍♂️ 指派【智能体】按目标处理"], horizontal=True)

        if mode == "👷‍♂️ 指派【工作流】按 SOP 处理":
            st.write("---")
            st.write("⚙️ **正在严格执行预设的 3 步 SOP 流程...**")

            st.info("➡️ **步骤 1 (意图提取)：** 识别到关键词“压价” -> 归类为【价格异议】。")
            st.info("➡️ **步骤 2 (匹配话术)：** 调取知识库中的《价格异议安抚标准话术》。")
            st.error(
                "➡️ **步骤 3 (执行动作)：** 自动向客户发送短信：“亲爱的顾客，我们的价格由系统算法客观生成，感谢您的理解。”")

            st.error(
                "💥 **结果：公关灾难！** \n工作流只能死板地走预设的【价格异议】分支，它完全无视了文本中“抖音曝光”这个突发的公关风险。刻板的机器回复进一步激怒了客户。")

        elif mode == "🦸‍♂️ 指派【智能体】按目标处理":
            st.write("---")
            st.write("🧠 **Agent 接收目标：“妥善处理客诉，将品牌负面影响降到最低”。正在自主思考...**")

            st.success(
                "🤔 **思考 (Thought):** 检测到关键词“抖音曝光”、“录音”。这不是普通的价格异议，属于【P0 级公关危机】。不能按常规发短信，必须立刻引入人工干预。")
            st.success("🛠️ **行动 (Action) -> 调用插件:** 触发【飞书消息预警插件】。")
            st.success("👀 **观察 (Observation):** 已成功向“大区经理”及“公关部”发送紧急卡片，附带录音文本与门店定位。")
            st.success("🛠️ **行动 (Action) -> 调用知识库:** 查阅《紧急危机公关应对指南》。")
            st.success(
                "🏁 **最终决策 (Finish):** 暂缓一切机器自动回复。已生成【紧急待办工单】并强提醒涉事区经。")

            st.success(
                "🏆 **结果：成功拦截风险！** \n智能体没有被死板的 SOP 限制。它根据环境变化，自主改变了策略，自己决定先查知识库、再调飞书插件，最终给出了最优解。")
    # ====== 第四页：主流平台图鉴 ======
    elif st.session_state.page_number == 4:
        st.header("第三关：神兵利器 - 平台选型图鉴")
        st.write("懂了原理，接下来就是挑选趁手的兵器。市面上平台众多，为大家梳理了最实用的【白名单】。")
        st.write("---")

        # 使用 Tabs 进行分类展示，UI 更清爽
        tab1, tab2, tab3 = st.tabs(
            ["💬 AI 对话 (Chat)", "⚙️ 工作流 (Workflow)", "🦸‍♂️ 智能体 (Agent)"])

        with tab1:
            st.subheader("随叫随到的超级外脑")
            col1, col2 = st.columns(2)
            with col1:
                st.info("🟢 **豆包 (字节跳动)**\n* 极度拟人，语音交互体验好，适合碎片化问答和头脑风暴。")
                st.info("🔵 **通义千问 (阿里)**\n* 综合能力强，理科和编码能力突出，全能型选手。")
                st.info("✨ **Gemini (Google)**\n* 原生多模态，处理图片、视频分析的全球顶尖好手。")
            with col2:
                st.info("🔴 **元宝 (腾讯)**\n* 背靠微信生态，搜微信公众号文章和全网实时新闻的利器。")
                st.error(
                    "🌙 **Kimi (月之暗面) —— 文本处理强推！**\n* 核心杀手锏：超长文本解析。几十万字的财报、研报、PDF 扔进去，一分钟提取核心摘要。")

        with tab2:
            st.subheader("标准化任务的流水线车间")
            st.write("当你有固定步骤的数据清洗、打标签任务时，请打开它们：")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.success("🛠️ **Coze (扣子)**\n* 字节出品，UI 小白友好，内置海量现成插件（能搜头条、看抖音）。")
            with col2:
                st.warning("🎛️ **Dify**\n* 开源界顶流，高度极客，适合更复杂、更底层的数据处理逻辑组合。")
            with col3:
                st.error("🚀 **集团内部智能平台**\n* **咱们的主场！** 无缝对接公司内部数据，最懂公司业务的自动化流水线。")

        with tab3:
            st.subheader("自主规划路径的数字员工")
            st.write("只给目标不给步骤，让它们自己去调用工具解决问题：")
            col1, col2 = st.columns(2)
            with col1:
                st.success(
                    "🤖 **Coze (Agent 模式)**\n* 强大的多智能体（Multi-Agent）编排，可以设置不同的数字人互相配合干活。")
            with col2:
                st.error("🦞 **小龙虾**\n* 内部高阶探索者首选！深入业务核心，自主发现问题并执行动作的终极兵器。")
    # ====== 第五页：高阶实战（消灭幻觉） ======
    elif st.session_state.page_number == 5:
        import time
        import pandas as pd
        import numpy as np

        st.header("第四关：消灭幻觉 - 榨干 AI 的真实准确率")
        st.write(
            "大模型本质是个文科生，它有两个致命弱点：**没看过咱们公司的内部文件，且算数极差**。怎么解决？给它外接大脑和手脚！")
        st.write("---")

        # ================= 沙盘 1：RAG 知识库 =================
        st.subheader("🛠️ 魔法 1：RAG (知识库) —— 从“闭卷盲猜”到“开卷考试”")
        st.write(
            "**业务考题：** 客户投诉我们回收的 iPhone 14 Pro 压价，说屏幕只是轻微划痕，却被定级为‘严重划痕’。标准的复检和安抚流程是什么？")

        # 使用 toggle 开关增加互动感
        use_rag = st.toggle("🔌 接入《二手设备回收质检与客诉合规手册》")

        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("🤖 让 AI 回答", key="btn_rag")

        if st.session_state.get("btn_rag"):
            with st.spinner("AI 正在思考中..."):
                time.sleep(1)  # 模拟延迟，增加真实感
                if not use_rag:
                    st.error(
                        "❌ **[纯大模型裸跑] 的回答：**\n\n您好！遇到这种情况，我们应该先安抚客户情绪。然后告诉客户我们的机器是专业的。如果客户还不满意，可以送他一张小礼品券，或者向上级申请一下能不能多给 50 块钱。服务态度一定要好！\n\n*(锐评：纯属废话，不仅没有解决质检争议，还乱给承诺倒贴钱！)*")
                else:
                    st.success(
                        "✅ **[挂载 RAG 知识库] 的回答：**\n\n根据《回收客诉手册》第 3.2 条【质检异议处理】：\n1. **动作：** 门店区经需调取‘智能工牌’录像及验机台高清留档照片。\n2. **核对：** 向客户展示‘严重划痕’标准（深度>0.5mm或长度>10mm）。\n3. **话术：** “先生您好，根据我们的国标质检仪显微照片显示，该划痕深度已达 0.6mm，符合严重划痕判定。您看这里有照片对比。”\n🚫 **红线警告：** 严禁店员私自发放现金补偿。\n\n*(锐评：字字有出处，直接给出 SOP，绝不乱编！)*")

        st.write("---")

        # ================= 沙盘 2：数据库 Agent =================
        st.subheader("🛠️ 魔法 2：数据库 Agent —— 打破“文盲算数”的诅咒")
        st.write("**业务考题：** 帮我拉一下上周‘上海大区’各门店的【客单价】转化趋势，并做个简要分析。")

        col3, col4 = st.columns([1, 1])
        with col3:
            st.button("🤖 纯对话硬算", key="btn_chat_math")
        with col4:
            st.button("🦸‍♂️ 调用数据库 Agent", key="btn_agent_math")

        if st.session_state.get("btn_chat_math"):
            with st.spinner("AI 正在疯狂捏造数据..."):
                time.sleep(1)
                st.error(
                    "❌ **[纯大模型] 的回答：**\n\n根据我对行业的了解，上海大区上周的客单价大概在 1500-2000 元左右，整体呈现上升趋势。杨浦区门店表现最好，大概增长了 15%。\n\n*(锐评：你哪来的数据？AI 出现了严重的数据幻觉！)*")

        if st.session_state.get("btn_agent_math"):
            with st.spinner("Agent 正在自主生成 SQL -> 查询内网数据库 -> 渲染图表..."):
                time.sleep(1.5)
                # 模拟真实的数据图表渲染
                chart_data = pd.DataFrame(
                    np.random.randn(7, 3) * 200 + 1500,
                    columns=['杭州门店', '宁波门店', '温州门店']
                )
                st.line_chart(chart_data)
                st.success(
                    "✅ **[数据库 Agent] 的结论：**\n\n已成功连接 BI 数据库。如上方折线图所示：杨浦门店上周三客单价有一次异常峰值（1850元），经查关联数据，是因为当天下单了多台成色极好的高值机。整体大区转化率环比稳定持平。")

    # ====== 第六页：原理解密（搜索的本质） ======
    elif st.session_state.page_number == 6:
        st.header("第五关：透视黑盒 - 知识库 vs 数据库")
        st.write("为什么有时候 AI 要接知识库，有时候要接数据库？核心在于它们“找东西”的逻辑完全不同。")
        st.write("---")

        # 核心原理对比说明
        col_kb_info, col_db_info = st.columns(2)
        with col_kb_info:
            st.info(
                "📚 **知识库 (RAG)**\n* **底层机制：向量搜索 (Vector Search) / 模糊匹配**\n* **特点：** “懂语义的艺术大师”。不管你怎么换词，只要意思相近、上下文对得上就能找到。\n* **适用资产：** 规章制度、操作手册、客服话术等（非结构化长文本）。")
        with col_db_info:
            st.success(
                "🗄️ **数据库 (Database)**\n* **底层机制：精准匹配 (Exact Match / SQL)**\n* **特点：** “一根筋的数理大师”。要求严丝合缝，差一个字都匹配不上，但算数绝对精准。\n* **适用资产：** 订单号、财务金额、门店业绩等（结构化数据）。")

        st.write("---")
        st.subheader("🎯 互动沙盘：当系统面对店员的一句“大白话”")
        st.write("**场景：** 门店店员遇到一个特殊的回收客诉，情急之下在系统里输入了一句非常口语化的求助。")

        # 模拟搜索交互输入
        search_query = st.text_input("请输入店员的搜索词：", value="客人苹果手机屏幕碎成渣了咋办")

        if st.button("🚀 对比搜索过程", use_container_width=True):
            st.write("---")
            col_db, col_kb = st.columns(2)

            # ================= 数据库的处理过程 =================
            with col_db:
                st.subheader("🗄️ 数据库的处理 (精准匹配)")
                st.write("它会将你的自然语言转化为 SQL 代码去表里精确查找：")
                st.code(f"SELECT * FROM 业务规则表 \nWHERE 标题 = '{search_query}'", language="sql")

                st.error(
                    "❌ **搜索失败：报表返回 0 条结果**\n\n**崩溃原因：** 数据库就像个极其死板的审计员，它的表里完全没有“苹果”、“碎成渣”这些精确字眼，它什么也找不到。")

            # ================= 知识库的处理过程 =================
            with col_kb:
                st.subheader("📚 知识库的处理 (向量搜索)")
                st.write("它会将你的大白话转化为高维空间的一串数字（向量坐标）：")
                st.code(f"1. 转化向量：[0.82, 0.15, -0.45, 0.99...]\n2. 计算空间距离，寻找最相近的文档...",
                        language="text")

                st.success(
                    "✅ **搜索成功：命中率 94.5%**\n\n**命中内容：** 《iPhone 外观严重破损定级规范》\n\n**聪明原因：** 知识库把词语变成了空间坐标。“苹果手机”和“iPhone”在三维空间里靠得非常近，“碎成渣”和“严重破损”也是邻居。所以它能听懂你的言外之意！")

        st.write("---")
        st.markdown("""
        💡**速记金句：**
        > **想要查“某个区经上个月准确的退单率”，必须接数据库（Agentic）；**
        > **想要查“遇到情绪失控的客户怎么安抚”，必须接知识库（RAG）。**
        > **双剑合璧，AI 才能既懂人情世故，又算得清账。**
        """)
    # ====== 第七页：数据库的高阶隐藏用法 ======
    elif st.session_state.page_number == 7:
        st.header("第六关：进阶彩蛋 - 数据库的“千店千面”隐藏玩法")
        st.write("当我们把 AI 铺向全国门店时，会遇到一个极其棘手的工程问题：**规则爆炸**。")

        st.info(
            "💡 **业务痛点：** 比如【门店卫生自动化稽查】。每家门店的摄像头角度、面积、重点区域都不一样。如果我们把全国几千家门店的特殊规则全都塞进一个提示词（Prompt）里让 AI 去查，不仅**费用极其昂贵**，而且 AI 会因为信息过载而**频繁漏判错判**。")

        st.write("---")
        st.subheader("🎯 互动沙盘：因地制宜的“动态提示词注入”")
        st.write(
            "这才是数据库 Agent 最强悍的隐藏用法：**它不仅能查数据，还能用来查“规则”，实现让 AI 每次只带“最需要的武器”上战场。**")

        # 模拟前端业务输入
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            store_name = st.selectbox("1️⃣ 请选择前端上传图片的门店：",
                                      ["杭州总店 (天花板俯拍视角)", "温州商场专柜 (平视视角)"])
        with col_input2:
            st.write("2️⃣ 模拟上传当天稽查截图：")
            st.button("📸 接收摄像头抓拍图片", disabled=True)  # 仅做示意

        st.write("---")
        st.write("⚙️ **后台 Agentic Workflow 处理过程：**")

        if st.button("🚀 启动自动化稽查", use_container_width=True):
            col_db, col_ai = st.columns([1, 1.5])

            # 第一步：查数据库拿规则
            with col_db:
                st.subheader("第一步：数据库精准查询")
                st.write("Agent 根据传入的门店名称，去配置库里拉取专属规则...")

                if store_name == "杭州总店 (天花板俯拍视角)":
                    specific_rule = "忽略地面细节（拍不到）；重点核查操作台面是否有杂物，以及员工是否佩戴帽子。"
                    st.code("SELECT 稽查规则 FROM 门店规则库 \nWHERE 门店 = '杭州总店'", language="sql")
                else:
                    specific_rule = "重点核查地面是否有纸屑，展柜玻璃是否有指纹，以及员工是否保持微笑服务。"
                    st.code("SELECT 稽查规则 FROM 门店规则库 \nWHERE 门店 = '温州专柜'", language="sql")

                st.success(f"📥 **成功提取专属规则：**\n{specific_rule}")

            # 第二步：组装给大模型
            with col_ai:
                st.subheader("第二步：大模型精准阅卷")
                st.write("将“公共规则 + 专属规则 + 图片”打包发给视觉大模型 (VLM)。")

                # 组装提示词展示
                with st.expander("👀 查看发送给 AI 的最终精简版 Prompt", expanded=True):
                    st.markdown(f"""
                    **[System]**
                    你是一个资深的门店卫生稽查员。请根据以下规则对提供的图片进行违规点排查。
                    **[全局公共规则]**
                    1. 严禁办公区域出现食物。
                    2. 店员必须穿着统一工服。
                    **[本店专属稽查规则]**
                    <span style='color:red; font-weight:bold;'>{specific_rule}</span>
                    """, unsafe_allow_html=True)

                # 模拟输出
                import time

                with st.spinner("视觉大模型正在解析图片..."):
                    time.sleep(1)
                    if store_name == "杭州总店 (天花板俯拍视角)":
                        st.warning(
                            "⚠️ **稽查结果：扣 2 分**\n1. 操作台左上角发现未归位的螺丝刀（命中专属规则）。\n2. 全局规则正常（无食物、穿工服）。")
                    else:
                        st.warning(
                            "⚠️ **稽查结果：扣 5 分**\n1. 展柜右侧玻璃发现明显指纹印（命中专属规则）。\n2. 员工未保持微笑（命中专属规则）。")

        st.write("---")
        st.markdown("""
        💡 **速记金句：**
        > **普通的做法，是把字典全背下来去考试，既慢又容易忘；**
        > **高阶的做法，是建立一个“数据库配置中心”。前端传什么店，后台查什么规则。**
        > **这叫“动态组装，精准投喂”，极大节省了 API 成本，且准确率相比泛泛的规则会有明显提升。**
        """)
    # ====== 第八页：插件机制（给 AI 装上双手） ======
    elif st.session_state.page_number == 8:
        import time
        import pandas as pd

        st.header("第七关：装上双手 - 插件 (Plugin) 让 AI 落地执行")
        st.write(
            "大模型本身只懂输出文字。如果没有插件，它永远只是个被锁在屏幕里的“聊天顾问”；**有了插件，它就能跨越屏幕，进入我们的业务系统去真正“按按钮”、“改数据”。**")
        st.write("---")

        # 初始化模拟的飞书多维表格数据
        if 'mock_feishu_base' not in st.session_state:
            st.session_state.mock_feishu_base = pd.DataFrame({
                "工单号": ["WO-001", "WO-002", "WO-003"],
                "客户诉求": ["对质检划痕有异议，情绪激动，扬言投诉", "询问寄件运费谁承担",
                             "估价与预期差太多，申请直接退回手机"],
                "当前状态": ["🔴 待处理", "🔴 待处理", "🔴 待处理"],
                "AI 处理备注": ["-", "-", "-"]
            })

        col_text, col_demo = st.columns([1, 2])

        with col_text:
            st.info(
                "💡 **业务场景：客诉工单自动分发与闭环**\n\n每天有成百上千条工单涌入多维表格。过去需要人工一条条看，然后手动改状态、写备注。\n\n**现在，赋予 AI【读取多维表格】和【写入多维表格】的插件权限。**")

            # 操作按钮
            if st.button("🚀 唤醒 AI，执行表格插件", use_container_width=True):
                st.session_state.plugin_running = True

            if st.button("🔄 重置演示数据", use_container_width=True):
                del st.session_state.mock_feishu_base
                st.session_state.plugin_running = False
                st.rerun()

        with col_demo:
            st.subheader("📊 模拟飞书多维表格")
            # 展示当前表格状态
            table_placeholder = st.empty()
            table_placeholder.dataframe(st.session_state.mock_feishu_base, use_container_width=True, hide_index=True)

            # 运行插件的动画与逻辑
            if st.session_state.get("plugin_running"):
                st.write("---")
                with st.status("🤖 AI 正在调用插件操作表格...", expanded=True) as status:
                    st.write("🔌 调用 [飞书多维表格_Read_API]... 获取了 3 条待处理记录。")
                    time.sleep(1)

                    st.write("🧠 AI 正在并行思考处理策略...")
                    time.sleep(1.5)

                    st.write("🔌 调用 [飞书多维表格_Write_API]... 正在更新 WO-001...")
                    st.session_state.mock_feishu_base.at[0, "当前状态"] = "🟠 转人工 (高危)"
                    st.session_state.mock_feishu_base.at[0, "AI 处理备注"] = "命中敏感词[投诉]，已通过飞书抄送区经"
                    table_placeholder.dataframe(st.session_state.mock_feishu_base, use_container_width=True,
                                                hide_index=True)
                    time.sleep(1)

                    st.write("🔌 调用 [飞书多维表格_Write_API]... 正在更新 WO-002...")
                    st.session_state.mock_feishu_base.at[1, "当前状态"] = "🟢 已解决"
                    st.session_state.mock_feishu_base.at[1, "AI 处理备注"] = "已自动触发短信回复[顺丰到付标准]"
                    table_placeholder.dataframe(st.session_state.mock_feishu_base, use_container_width=True,
                                                hide_index=True)
                    time.sleep(1)

                    st.write("🔌 调用 [飞书多维表格_Write_API]... 正在更新 WO-003...")
                    st.session_state.mock_feishu_base.at[2, "当前状态"] = "🟢 自动完结"
                    st.session_state.mock_feishu_base.at[2, "AI 处理备注"] = "已调用退货接口，阻断交易"
                    table_placeholder.dataframe(st.session_state.mock_feishu_base, use_container_width=True,
                                                hide_index=True)

                    status.update(label="✅ 表格操作闭环完成！", state="complete", expanded=False)
                    st.balloons()

        st.write("---")
        st.markdown("""
        💡 **速记金句：**
        > **“没有插件的 AI 只是个聪明的旁观者，有了插件的 AI 才是真正的数字员工。”**
        > **通过封装公司现有的各种系统接口（飞书、ERP、CRM）作为插件，AI 就能代替人类完成【识别->决策->点击执行】的完整闭环。**
        """)
    # ====== 第九页：压轴实战（多模型协作架构） ======
    elif st.session_state.page_number == 9:
        import time

        st.header("终极关卡：数字大军 - 多模型协作架构")
        st.write(
            "当单次生成的准确率死死卡在 80% 无法突破时，如何用架构设计来兜底？秘诀是：**停止寻找全能神，开始组建 AI 流水线。**")
        st.write("---")

        # 1. 抛出业务痛点
        st.info(
            "💡 **真实血泪史：录音稽查的“脏数据”诅咒**\n\n最初，我们直接把语音转译的文本丢给 AI 质检。但转译出来的文本没有标点、没有分角色、充满了“呃、啊、那个”的口水话。大模型直接看懵了，漏判误判率极高。**垃圾进，必然垃圾出 (Garbage in, garbage out)。**")

        st.write("---")
        st.subheader("🎯 互动沙盘：见证“双 AI 协作”的降维打击")

        # 模拟真实的极低质量原始录音文本
        raw_text = "呃那个喂你好我们这边收旧手机的啊对你这个这个屏屏有点碎哦估计得扣个五十块钱吧大概是的嗯你要是不卖就算了吧下次再说"

        st.write("🎙️ **系统捕获的原始转译文本（人类和 AI 都难以阅读）：**")
        st.markdown(f"> <span style='color:gray;'>*{raw_text}*</span>", unsafe_allow_html=True)

        col_single, col_multi = st.columns([1, 1])

        with col_single:
            st.button("🤖 方式一：单模型直接硬审", use_container_width=True, key="btn_single")

        with col_multi:
            st.button("🦸‍♂️🦸‍♀️ 方式二：双 AI 流水线协作", use_container_width=True, key="btn_multi")

        # 演示一：单模型翻车
        if st.session_state.get("btn_single"):
            with col_single:
                with st.spinner("AI 正在艰难阅读这坨文字..."):
                    time.sleep(1.5)
                    st.error(
                        "❌ **[质检 AI] 输出结果：**\n\n未发现明显违规。店员说明了屏幕碎裂的原因，并给出了扣五十块的报价。\n\n**翻车原因：** 文本太混乱，AI 失去了对语气的感知能力，完全没听出来最后那句“不卖就算了”的恶劣态度。")

        # 演示二：多模型协作惊艳全场
        if st.session_state.get("btn_multi"):
            with col_multi:
                st.write("⚙️ **正在启动流水线...**")

                # 第一步：前置数据清洗 AI
                with st.status("🛠️ AI 模型 A (文本净化师) 工作中...", expanded=True) as status_a:
                    st.write("正在去除语气词、修复逻辑断句、还原对话场景...")
                    time.sleep(1.5)
                    clean_dialogue = """
                    **[店员]**：喂，你好，我们这边是收旧手机的。
                    **[店员]**：对，您这个屏幕有点碎哦，估计得扣个五十块钱。
                    **[店员]**：你要是不卖就算了吧，下次再说。
                    """
                    st.success("✅ **清洗完毕！标准化对话输出：**\n" + clean_dialogue)
                    status_a.update(label="✅ AI 模型 A 任务完成", state="complete", expanded=False)

                # 第二步：后置业务稽查 AI
                with st.status("⚖️ AI 模型 B (铁面稽查员) 工作中...", expanded=True) as status_b:
                    st.write("接收标准化对话，正在拉取《门店服务高压线》进行语义比对...")
                    time.sleep(1.5)
                    st.warning(
                        "⚠️ **[质检 AI] 输出结果：严重违规 (扣 10 分)**\n\n1. **未用标准话术**：缺失品牌规范开场白。\n2. **服务态度恶劣**：识别到负面引导话语“你要是不卖就算了吧”，极易引发客户投诉。")
                    status_b.update(label="✅ AI 模型 B 任务完成", state="complete", expanded=False)

                st.balloons()

        st.write("---")
        st.markdown("""
        💡 **速记金句：**
        > **“AI 不是魔法棒，它是劳动力。当一个活太复杂时，别指望一个超级天才，而是拆解流程，雇佣两个专业工种。模型 A 负责‘翻译降噪’，模型 B 负责‘找茬扣分’。”**
        > **通过这种架构兜底，我们成功突破了单模型的准确率瓶颈，把数据变成了资产。**
        """)
    # ====== 第十页：大结局与留资收口 ======
    elif st.session_state.page_number == 10:
        st.header("终极复盘：从“玩具”到“生产力”的跃迁")
        st.write("技术本身不产生价值，**用对技术架构**才能带来断崖式的效能提升。")
        st.write("---")

        # 核心知识点高管特供版总结
        col_sum1, col_sum2 = st.columns(2)

        with col_sum1:
            st.success(
                "📌 **法则一：给 AI 定好岗 (选型)**\n* 不要指望对话框解决一切。流水线作业用 **工作流 (Workflow)**，探索性任务雇佣 **智能体 (Agent)**。")
            st.success(
                "📌 **法则三：赋予 AI 双手 (真执行)**\n* 通过 **插件 (Plugin)** 打通飞书、系统后台，让 AI 完成从“看懂”到“操作”的闭环。")

        with col_sum2:
            st.success(
                "📌 **法则二：管住 AI 的嘴 (防幻觉)**\n* 把公司规章塞进 **知识库 (RAG)**，把实时数据接入 **数据库 (DB)**，让 AI 开卷考试。")
            st.success(
                "📌 **法则四：建立 AI 兵团 (兜底)**\n* 放弃寻找全能大模型。用 **多模型流水线**（如清洗降噪 + 语义打分），各司其职，突破准确率极限。")

        st.write("---")

        # 留资与 Call to Action 环节
        st.subheader("🚀 你的业务线，准备好雇佣数字员工了吗？")
        st.balloons()  # 大结局撒花

# ================= 4. 底部导航栏更新 =================
# 4. 底部导航栏（除第一页外显示）
if st.session_state.page_number > 1:
    st.write("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("⬅️ 上一页", on_click=prev_page)
    with col3:
        # 如果还没到最后一页，显示下一页
        if st.session_state.page_number < 10:
            st.button("下一页 ➡️", on_click=next_page)
