class PokemonTypeCalculator:
    """
    赛尔号精灵属性计算工具类
    用于计算攻击方精灵对防御方精灵的克制倍率
    """
    
    # 基础属性克制倍率矩阵
    # 格式: {攻击属性: {防御属性: 倍率}}
    TYPE_MATRIX = {
        # 草系
        "草": {
            "草": 0.5, "水": 2, "火": 0.5, "电": 1, "光": 1, "暗": 1, "飞": 0.5, "地": 2, "战斗": 1, "龙": 1, "神圣": 1, "混沌": 1
        },
        # 水系
        "水": {
            "草": 0.5, "水": 0.5, "火": 2, "电": 1, "光": 1, "暗": 1, "飞": 1, "地": 1, "战斗": 1, "龙": 1, "神圣": 1, "混沌": 1
        },
        # 火系
        "火": {
            "草": 2, "水": 0.5, "火": 0.5, "电": 1, "光": 1, "暗": 1, "飞": 1, "地": 1, "战斗": 1, "龙": 1, "神圣": 1, "混沌": 1
        },
        # 电系
        "电": {
            "草": 1, "水": 2, "火": 1, "电": 0.5, "光": 1, "暗": 1, "飞": 2, "地": 0, "战斗": 1, "龙": 1, "神圣": 1, "混沌": 1
        },
        # 光系
        "光": {
            "草": 1, "水": 1, "火": 1, "电": 1, "光": 0.5, "暗": 2, "飞": 1, "地": 1, "战斗": 1, "龙": 1, "神圣": 0.5, "混沌": 2
        },
        # 暗系
        "暗": {
            "草": 1, "水": 1, "火": 1, "电": 1, "光": 2, "暗": 0.5, "飞": 1, "地": 1, "战斗": 1, "龙": 1, "神圣": 2, "混沌": 0.5
        },
        # 飞行系
        "飞": {
            "草": 2, "水": 1, "火": 1, "电": 0.5, "光": 1, "暗": 1, "飞": 0.5, "地": 0, "战斗": 2, "龙": 1, "神圣": 1, "混沌": 1
        },
        # 地面系
        "地": {
            "草": 0.5, "水": 2, "火": 2, "电": 2, "光": 1, "暗": 1, "飞": 1, "地": 0.5, "战斗": 1, "龙": 1, "神圣": 1, "混沌": 1
        },
        # 战斗系
        "战斗": {
            "草": 1, "水": 1, "火": 1, "电": 1, "光": 1, "暗": 1, "飞": 0.5, "地": 1, "战斗": 0.5, "龙": 2, "神圣": 2, "混沌": 1
        },
        # 龙系
        "龙": {
            "草": 1, "水": 1, "火": 1, "电": 1, "光": 1, "暗": 1, "飞": 1, "地": 1, "战斗": 0.5, "龙": 2, "神圣": 1, "混沌": 1
        },
        # 神圣系
        "神圣": {
            "草": 1, "水": 1, "火": 1, "电": 1, "光": 2, "暗": 0.5, "飞": 1, "地": 1, "战斗": 0.5, "龙": 1, "神圣": 0.5, "混沌": 2
        },
        # 混沌系
        "混沌": {
            "草": 1, "水": 1, "火": 1, "电": 1, "光": 0.5, "暗": 2, "飞": 1, "地": 1, "战斗": 1, "龙": 1, "神圣": 0.5, "混沌": 0.5
        }
    }
    
    @classmethod
    def add_custom_type(cls, type_name, effectiveness):
        """
        添加自定义属性及其克制关系
        
        参数:
            type_name (str): 自定义属性名称
            effectiveness (dict): 克制关系字典，格式为 {防御属性: 倍率}
        """
        if type_name not in cls.TYPE_MATRIX:
            cls.TYPE_MATRIX[type_name] = effectiveness
        else:
            cls.TYPE_MATRIX[type_name].update(effectiveness)
        
        # 为所有现有属性添加对新属性的默认克制关系（默认为1倍）
        for existing_type in cls.TYPE_MATRIX:
            if existing_type != type_name and type_name not in cls.TYPE_MATRIX[existing_type]:
                cls.TYPE_MATRIX[existing_type][type_name] = 1
    
    @classmethod
    def calculate_effectiveness(cls, attack_type, defense_type):
        """
        计算攻击方对防御方的克制倍率
        
        参数:
            attack_type (str or list): 攻击方属性，可以是单属性字符串或双属性列表
            defense_type (str or list): 防御方属性，可以是单属性字符串或双属性列表
        
        返回:
            float: 最终克制倍率
        """
        # 确保攻击方属性是列表形式
        if isinstance(attack_type, str):
            attack_types = [attack_type]
        else:
            attack_types = attack_type
        
        # 确保防御方属性是列表形式
        if isinstance(defense_type, str):
            defense_types = [defense_type]
        else:
            defense_types = defense_type
        
        total_multiplier = 1.0
        
        # 遍历攻击方的每个属性
        for atk_type in attack_types:
            # 遍历防御方的每个属性
            for def_type in defense_types:
                # 检查属性是否存在于矩阵中
                if atk_type in cls.TYPE_MATRIX and def_type in cls.TYPE_MATRIX[atk_type]:
                    multiplier = cls.TYPE_MATRIX[atk_type][def_type]
                else:
                    # 对于不存在的属性组合，默认为1倍
                    multiplier = 1.0
                
                total_multiplier *= multiplier
        
        return total_multiplier

# 测试用例
if __name__ == "__main__":
    # 测试1: 光暗系精灵攻击草系
    print("测试1: 光暗系精灵攻击草系")
    result1 = PokemonTypeCalculator.calculate_effectiveness(["光", "暗"], "草")
    print(f"光暗系 → 草系: {result1}倍")
    print()
    
    # 测试2: 战斗系攻击火系
    print("测试2: 战斗系攻击火系")
    result2 = PokemonTypeCalculator.calculate_effectiveness("战斗", "火")
    print(f"战斗系 → 火系: {result2}倍")
    print()
    
    # 测试3: 草系攻击水系
    print("测试3: 草系攻击水系")
    result3 = PokemonTypeCalculator.calculate_effectiveness("草", "水")
    print(f"草系 → 水系: {result3}倍")
    print()
    
    # 测试4: 电系攻击地面系
    print("测试4: 电系攻击地面系")
    result4 = PokemonTypeCalculator.calculate_effectiveness("电", "地")
    print(f"电系 → 地面系: {result4}倍")
    print()
    
    # 测试5: 光系攻击暗系
    print("测试5: 光系攻击暗系")
    result5 = PokemonTypeCalculator.calculate_effectiveness("光", "暗")
    print(f"光系 → 暗系: {result5}倍")
    print()
    
    # 测试6: 双属性攻击双属性
    print("测试6: 草电系攻击飞地系")
    result6 = PokemonTypeCalculator.calculate_effectiveness(["草", "电"], ["飞", "地"])
    print(f"草电系 → 飞地系: {result6}倍")
    print()
    
    # 测试7: 添加自定义属性
    print("测试7: 添加自定义属性并测试")
    PokemonTypeCalculator.add_custom_type("机械", {"草": 1, "水": 1, "火": 2, "电": 0.5})
    result7 = PokemonTypeCalculator.calculate_effectiveness("机械", "火")
    print(f"机械系 → 火系: {result7}倍")
    result8 = PokemonTypeCalculator.calculate_effectiveness("火", "机械")
    print(f"火系 → 机械系: {result8}倍")
