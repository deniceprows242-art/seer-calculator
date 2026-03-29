import sqlite3
from typing import List, Tuple, Optional

class SeerDatabaseManager:
    """
    赛尔号精灵数据库管理类
    用于管理精灵信息的SQLite数据库
    """
    
    def __init__(self, db_path: str = "seer_data.db"):
        """
        初始化数据库管理器
        
        参数:
            db_path (str): 数据库文件路径，默认为 seer_data.db
        """
        self.db_path = db_path
        self.conn = None
        self._initialize_database()
    
    def _initialize_database(self):
        """
        初始化数据库，创建spirits表
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # 创建spirits表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS spirits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_cn TEXT NOT NULL,
                    attribute1 TEXT NOT NULL,
                    attribute2 TEXT
                )
            ''')
            
            self.conn.commit()
            print(f"数据库初始化成功: {self.db_path}")
            
        except sqlite3.Error as e:
            print(f"数据库初始化失败: {e}")
            if self.conn:
                self.conn.close()
                self.conn = None
    
    def insert_spirit(self, name: str, attr1: str, attr2: Optional[str] = None) -> bool:
        """
        将精灵信息安全地插入到数据库中
        
        参数:
            name (str): 精灵中文名
            attr1 (str): 主属性
            attr2 (str, optional): 副属性，允许为空
        
        返回:
            bool: 插入是否成功
        """
        if not self.conn:
            print("数据库连接未建立")
            return False
        
        try:
            cursor = self.conn.cursor()
            
            # 使用参数化查询防止SQL注入
            cursor.execute('''
                INSERT INTO spirits (name_cn, attribute1, attribute2)
                VALUES (?, ?, ?)
            ''', (name, attr1, attr2))
            
            self.conn.commit()
            print(f"成功插入精灵: {name} (属性: {attr1}{f'/{attr2}' if attr2 else ''})")
            return True
            
        except sqlite3.Error as e:
            print(f"插入精灵失败: {e}")
            return False
    
    def get_all_spirits(self) -> List[Tuple[int, str, str, Optional[str]]]:
        """
        查询并返回所有精灵的信息
        
        返回:
            List[Tuple]: 精灵信息列表，每个元素为 (id, name_cn, attribute1, attribute2)
        """
        if not self.conn:
            print("数据库连接未建立")
            return []
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, name_cn, attribute1, attribute2 FROM spirits ORDER BY id')
            spirits = cursor.fetchall()
            return spirits
            
        except sqlite3.Error as e:
            print(f"查询精灵失败: {e}")
            return []
    
    def get_spirit_by_name(self, name: str) -> Optional[Tuple[int, str, str, Optional[str]]]:
        """
        根据名称查询精灵信息
        
        参数:
            name (str): 精灵中文名
        
        返回:
            Optional[Tuple]: 精灵信息 (id, name_cn, attribute1, attribute2)，如果未找到则返回None
        """
        if not self.conn:
            print("数据库连接未建立")
            return None
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, name_cn, attribute1, attribute2 
                FROM spirits 
                WHERE name_cn = ?
            ''', (name,))
            spirit = cursor.fetchone()
            return spirit
            
        except sqlite3.Error as e:
            print(f"查询精灵失败: {e}")
            return None
    
    def get_spirits_by_attribute(self, attr: str) -> List[Tuple[int, str, str, Optional[str]]]:
        """
        根据属性查询精灵信息
        
        参数:
            attr (str): 属性名称
        
        返回:
            List[Tuple]: 精灵信息列表，包含指定属性的精灵
        """
        if not self.conn:
            print("数据库连接未建立")
            return []
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, name_cn, attribute1, attribute2 
                FROM spirits 
                WHERE attribute1 = ? OR attribute2 = ?
                ORDER BY id
            ''', (attr, attr))
            spirits = cursor.fetchall()
            return spirits
            
        except sqlite3.Error as e:
            print(f"查询精灵失败: {e}")
            return []
    
    def delete_spirit(self, spirit_id: int) -> bool:
        """
        根据ID删除精灵
        
        参数:
            spirit_id (int): 精灵ID
        
        返回:
            bool: 删除是否成功
        """
        if not self.conn:
            print("数据库连接未建立")
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM spirits WHERE id = ?', (spirit_id,))
            self.conn.commit()
            
            if cursor.rowcount > 0:
                print(f"成功删除ID为 {spirit_id} 的精灵")
                return True
            else:
                print(f"未找到ID为 {spirit_id} 的精灵")
                return False
            
        except sqlite3.Error as e:
            print(f"删除精灵失败: {e}")
            return False
    
    def close(self):
        """
        关闭数据库连接
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            print("数据库连接已关闭")
    
    def __enter__(self):
        """
        支持with语句的上下文管理器
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        支持with语句的上下文管理器
        """
        self.close()


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("赛尔号精灵数据库管理测试")
    print("=" * 50)
    
    # 使用with语句确保数据库连接正确关闭
    with SeerDatabaseManager() as db:
        print("\n1. 插入测试精灵")
        print("-" * 50)
        
        # 插入哈莫雷特（龙系）
        db.insert_spirit("哈莫雷特", "龙")
        
        # 插入谱尼（神圣系）
        db.insert_spirit("谱尼", "神圣")
        
        # 插入更多测试精灵
        db.insert_spirit("雷伊", "电", "飞行")
        db.insert_spirit("布莱克", "暗", "战斗")
        db.insert_spirit("卡修斯", "地", "战斗")
        
        print("\n2. 查询所有精灵")
        print("-" * 50)
        all_spirits = db.get_all_spirits()
        print(f"共找到 {len(all_spirits)} 个精灵:")
        for spirit in all_spirits:
            spirit_id, name, attr1, attr2 = spirit
            attr_str = f"{attr1}/{attr2}" if attr2 else attr1
            print(f"  ID: {spirit_id}, 名称: {name}, 属性: {attr_str}")
        
        print("\n3. 根据名称查询精灵")
        print("-" * 50)
        spirit = db.get_spirit_by_name("哈莫雷特")
        if spirit:
            spirit_id, name, attr1, attr2 = spirit
            attr_str = f"{attr1}/{attr2}" if attr2 else attr1
            print(f"  找到精灵: ID: {spirit_id}, 名称: {name}, 属性: {attr_str}")
        else:
            print("  未找到该精灵")
        
        print("\n4. 根据属性查询精灵")
        print("-" * 50)
        battle_spirits = db.get_spirits_by_attribute("战斗")
        print(f"  属性为'战斗'的精灵:")
        for spirit in battle_spirits:
            spirit_id, name, attr1, attr2 = spirit
            attr_str = f"{attr1}/{attr2}" if attr2 else attr1
            print(f"    ID: {spirit_id}, 名称: {name}, 属性: {attr_str}")
        
        print("\n5. 删除精灵测试")
        print("-" * 50)
        db.delete_spirit(1)
        
        print("\n6. 删除后查询所有精灵")
        print("-" * 50)
        all_spirits = db.get_all_spirits()
        print(f"共找到 {len(all_spirits)} 个精灵:")
        for spirit in all_spirits:
            spirit_id, name, attr1, attr2 = spirit
            attr_str = f"{attr1}/{attr2}" if attr2 else attr1
            print(f"  ID: {spirit_id}, 名称: {name}, 属性: {attr_str}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)
