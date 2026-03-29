import streamlit as st
from db_manager import SeerDatabaseManager
from pokemon_type_calculator import PokemonTypeCalculator

def get_spirit_attributes(spirit_data):
    """
    提取精灵的主副属性
    
    参数:
        spirit_data (tuple): 精灵数据 (id, name_cn, attribute1, attribute2)
    
    返回:
        list: 属性列表，如果是双属性则返回[attribute1, attribute2]，单属性则返回[attribute1]
    """
    _, _, attr1, attr2 = spirit_data
    if attr2:
        return [attr1, attr2]
    else:
        return [attr1]

def format_spirit_display(spirit_data):
    """
    格式化精灵显示文本
    
    参数:
        spirit_data (tuple): 精灵数据 (id, name_cn, attribute1, attribute2)
    
    返回:
        str: 格式化的显示文本
    """
    _, name, attr1, attr2 = spirit_data
    if attr2:
        return f"{name} ({attr1}/{attr2}系)"
    else:
        return f"{name} ({attr1}系)"

def calculate_battle_result(attack_spirit, defense_spirit):
    """
    计算战斗结果
    
    参数:
        attack_spirit (tuple): 攻击方精灵数据
        defense_spirit (tuple): 防御方精灵数据
    
    返回:
        tuple: (攻击方属性列表, 防御方属性列表, 克制倍率)
    """
    attack_attrs = get_spirit_attributes(attack_spirit)
    defense_attrs = get_spirit_attributes(defense_spirit)
    multiplier = PokemonTypeCalculator.calculate_effectiveness(attack_attrs, defense_attrs)
    
    return attack_attrs, defense_attrs, multiplier

def get_multiplier_color(multiplier):
    """
    根据克制倍率返回对应的颜色
    
    参数:
        multiplier (float): 克制倍率
    
    返回:
        str: 颜色名称
    """
    if multiplier >= 2.0:
        return "green"
    elif multiplier >= 1.5:
        return "lightgreen"
    elif multiplier == 1.0:
        return "blue"
    elif multiplier >= 0.5:
        return "orange"
    elif multiplier > 0.0:
        return "red"
    else:
        return "gray"

def get_multiplier_description(multiplier):
    """
    根据克制倍率返回描述文本
    
    参数:
        multiplier (float): 克制倍率
    
    返回:
        str: 描述文本
    """
    if multiplier >= 2.0:
        return "🔥 强力克制"
    elif multiplier >= 1.5:
        return "⚡ 克制"
    elif multiplier == 1.0:
        return "⚖️ 正常"
    elif multiplier >= 0.5:
        return "🛡️ 抵抗"
    elif multiplier > 0.0:
        return "💪 强力抵抗"
    else:
        return "❌ 免疫"

def render_sidebar(spirits, spirit_options):
    """
    渲染侧边栏阵容管理
    
    参数:
        spirits (list): 所有精灵数据列表
        spirit_options (dict): 精灵选项字典
    """
    st.sidebar.title("🎒 我的背包/阵容管理")
    st.sidebar.markdown("---")
    
    # 初始化阵容状态
    if "my_team" not in st.session_state:
        st.session_state.my_team = []
    
    # 创建精灵显示选项列表
    spirit_display_options = list(spirit_options.keys())
    
    # 多选框选择阵容精灵
    st.sidebar.subheader("选择阵容精灵")
    st.sidebar.info("💡 提示：最多可选择 6 只精灵")
    
    # 获取当前阵容中的精灵显示名称
    current_team_displays = [format_spirit_display(spirit) for spirit in st.session_state.my_team]
    
    # 多选框选择
    selected_displays = st.sidebar.multiselect(
        "从全库中选择精灵",
        options=spirit_display_options,
        default=current_team_displays,
        key="team_selection"
    )
    
    # 限制最多6只精灵
    if len(selected_displays) > 6:
        st.sidebar.warning(f"⚠️ 阵容最多只能选择 6 只精灵，已自动截取前 6 只")
        selected_displays = selected_displays[:6]
    
    # 更新阵容状态
    st.session_state.my_team = [spirit_options[display] for display in selected_displays]
    
    st.sidebar.markdown("---")
    
    # 显示当前阵容
    st.sidebar.subheader("当前阵容")
    if st.session_state.my_team:
        for i, spirit in enumerate(st.session_state.my_team, 1):
            _, name, attr1, attr2 = spirit
            attr_str = f"{attr1}/{attr2}" if attr2 else attr1
            st.sidebar.write(f"{i}. **{name}** ({attr_str}系)")
        
        # 显示阵容统计
        st.sidebar.markdown("---")
        st.sidebar.metric("阵容数量", f"{len(st.session_state.my_team)}/6")
        
        # 清空阵容按钮
        if st.sidebar.button("🗑️ 清空阵容", key="clear_team"):
            st.session_state.my_team = []
            st.rerun()
    else:
        st.sidebar.info("📭 阵容为空，请从上方选择精灵")
    
    st.sidebar.markdown("---")
    
    # 数据录入功能
    with st.sidebar.expander("➕ 录入新精灵"):
        with st.form("add_spirit_form"):
            spirit_name = st.text_input("精灵名称", key="new_spirit_name")
            
            # 获取所有可用属性
            available_attributes = list(PokemonTypeCalculator.TYPE_MATRIX.keys())
            
            # 主属性选择
            primary_attr = st.selectbox(
                "主属性",
                options=available_attributes,
                key="new_spirit_attr1"
            )
            
            # 副属性选择（允许"无"）
            secondary_attr = st.selectbox(
                "副属性",
                options=["无"] + available_attributes,
                key="new_spirit_attr2"
            )
            
            # 提交按钮
            submitted = st.form_submit_button("确认录入", type="primary")
            
            if submitted:
                if spirit_name.strip():
                    # 处理副属性
                    attr2 = secondary_attr if secondary_attr != "无" else None
                    
                    # 调用数据库插入函数
                    db = SeerDatabaseManager()
                    success = db.insert_spirit(spirit_name.strip(), primary_attr, attr2)
                    db.close()
                    
                    if success:
                        st.success(f"✅ 成功录入精灵：{spirit_name}")
                        st.info("🔄 页面将自动刷新以更新数据...")
                        st.rerun()
                    else:
                        st.error("❌ 录入失败，请检查输入信息")
                else:
                    st.warning("⚠️ 请输入精灵名称")

def render_spirit_selection(title, icon, spirits, spirit_options, key_prefix):
    """
    渲染精灵选择区域
    
    参数:
        title (str): 标题
        icon (str): 图标
        spirits (list): 所有精灵数据列表
        spirit_options (dict): 精灵选项字典
        key_prefix (str): 键前缀
    
    返回:
        tuple: 选中的精灵数据
    """
    st.subheader(f"{icon} {title}")
    
    # 创建标签页
    tab1, tab2 = st.tabs(["🎯 从阵容选择", "🔍 全库搜索"])
    
    selected_spirit = None
    
    with tab1:
        # 从阵容选择
        if st.session_state.my_team:
            team_options = {format_spirit_display(spirit): spirit for spirit in st.session_state.my_team}
            selection = st.selectbox(
                "从阵容中选择精灵",
                options=list(team_options.keys()),
                key=f"{key_prefix}_team"
            )
            if selection:
                selected_spirit = team_options[selection]
        else:
            st.warning("⚠️ 请先在左侧边栏配置阵容")
            st.info("💡 点击左侧边栏的'我的背包/阵容管理'来添加精灵到阵容")
    
    with tab2:
        # 全库搜索
        spirit_display_options = list(spirit_options.keys())
        selection = st.selectbox(
            "输入精灵名称快速搜索",
            options=spirit_display_options,
            key=f"{key_prefix}_all"
        )
        if selection:
            selected_spirit = spirit_options[selection]
    
    return selected_spirit

def main():
    """
    Streamlit应用主函数
    """
    # 设置页面配置
    st.set_page_config(
        page_title="赛尔号精灵属性克制计算器",
        page_icon="⚔️",
        layout="wide"
    )
    
    # 页面标题
    st.title("⚔️ 赛尔号精灵属性克制计算器")
    st.markdown("---")
    
    # 初始化数据库连接
    try:
        db = SeerDatabaseManager()
        spirits = db.get_all_spirits()
        
        if not spirits:
            st.error("数据库中没有精灵数据，请先运行 db_manager.py 添加精灵数据！")
            return
        
        # 创建精灵选项字典
        spirit_options = {format_spirit_display(spirit): spirit for spirit in spirits}
        
        # 渲染侧边栏
        render_sidebar(spirits, spirit_options)
        
        # 创建两列布局
        col1, col2 = st.columns(2)
        
        with col1:
            attack_spirit = render_spirit_selection("攻击方精灵", "🗡️", spirits, spirit_options, "attack")
        
        with col2:
            defense_spirit = render_spirit_selection("防御方精灵", "🛡️", spirits, spirit_options, "defense")
        
        # 计算按钮
        st.markdown("---")
        col_button = st.columns([1, 2, 1])
        with col_button[1]:
            calculate_clicked = st.button("🎯 计算克制倍率", type="primary", width="stretch")
        
        # 计算并显示结果
        if calculate_clicked:
            if attack_spirit and defense_spirit:
                # 计算战斗结果
                attack_attrs, defense_attrs, multiplier = calculate_battle_result(
                    attack_spirit, defense_spirit
                )
                
                # 提取精灵名称和属性信息
                _, attack_name, _, _ = attack_spirit
                _, defense_name, _, _ = defense_spirit
                
                # 格式化属性显示
                attack_attr_str = "/".join(attack_attrs)
                defense_attr_str = "/".join(defense_attrs)
                
                # 获取颜色和描述
                color = get_multiplier_color(multiplier)
                description = get_multiplier_description(multiplier)
                
                # 显示结果
                st.markdown("---")
                st.subheader("📊 计算结果")
                
                # 使用metric显示倍率
                col_result1, col_result2, col_result3 = st.columns(3)
                
                with col_result1:
                    st.metric(
                        label="克制倍率",
                        value=f"{multiplier} 倍",
                        delta=description
                    )
                
                with col_result2:
                    st.metric(
                        label="攻击方",
                        value=attack_name,
                        delta=f"{attack_attr_str}系"
                    )
                
                with col_result3:
                    st.metric(
                        label="防御方",
                        value=defense_name,
                        delta=f"{defense_attr_str}系"
                    )
                
                # 详细结果文本
                st.markdown("---")
                result_text = f"### {attack_name} ({attack_attr_str}系) 攻击 {defense_name} ({defense_attr_str}系)，最终伤害倍率：**{multiplier} 倍**"
                
                if multiplier >= 2.0:
                    st.success(result_text)
                elif multiplier == 1.0:
                    st.info(result_text)
                elif multiplier > 0.0:
                    st.warning(result_text)
                else:
                    st.error(result_text)
                
                # 显示详细计算过程
                st.markdown("---")
                st.subheader("🔍 详细计算过程")
                
                # 计算每个属性组合的倍率
                calculation_steps = []
                for i, attack_attr in enumerate(attack_attrs):
                    for j, defense_attr in enumerate(defense_attrs):
                        step_multiplier = PokemonTypeCalculator.calculate_effectiveness(
                            attack_attr, defense_attr
                        )
                        calculation_steps.append({
                            "攻击属性": attack_attr,
                            "防御属性": defense_attr,
                            "倍率": step_multiplier
                        })
                
                # 显示计算步骤表格
                if calculation_steps:
                    st.table(calculation_steps)
                    
                    # 显示总倍率计算公式
                    if len(calculation_steps) > 1:
                        multipliers = [step["倍率"] for step in calculation_steps]
                        formula = " × ".join([str(m) for m in multipliers])
                        st.info(f"📐 总倍率计算公式: {formula} = {multiplier}")
            else:
                st.warning("⚠️ 请先选择攻击方和防御方精灵")
                if not attack_spirit:
                    st.info("💡 请在左侧选择攻击方精灵")
                if not defense_spirit:
                    st.info("💡 请在右侧选择防御方精灵")
        
        # 显示数据库中的精灵列表
        st.markdown("---")
        with st.expander("📋 查看所有精灵数据"):
            st.write(f"数据库中共有 **{len(spirits)}** 个精灵")
            spirit_list_data = []
            for spirit in spirits:
                spirit_id, name, attr1, attr2 = spirit
                attr_str = f"{attr1}/{attr2}" if attr2 else attr1
                spirit_list_data.append({
                    "ID": spirit_id,
                    "名称": name,
                    "属性": attr_str
                })
            st.dataframe(spirit_list_data, width="stretch")
        
        # 关闭数据库连接
        db.close()
        
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        st.info("请确保数据库文件存在且包含精灵数据")

if __name__ == "__main__":
    main()
