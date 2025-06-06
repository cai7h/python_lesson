from datetime import date
from typing import List, Optional, Callable, NoReturn

# 类型别名定义
OrderStatus = str

class Customer:
    """客户信息类，存储客户基本资料
    
    Attributes:
        name: 客户姓名
        contact: 联系电话
        delivery_address: 配送地址
        active: 客户状态
    """
    
    def __init__(self, name: str, contact: str, delivery_address: str, active: bool) -> None:
        """初始化客户对象
        
        Args:
            name: 客户姓名
            contact: 联系电话
            delivery_address: 配送地址
            active: 是否为活跃客户
        """
        self.name = name
        self.contact = contact
        self.delivery_address = delivery_address
        self.active = active

class Product:
    """商品类，包含商品属性和计算方法
    
    Attributes:
        title: 商品名称
        weight: 商品重量(kg)
        description: 商品描述
        price: 商品单价(元)
    """
    
    def __init__(self, title: str, weight: float, description: str, price: float) -> None:
        """初始化商品对象
        
        Args:
            title: 商品名称
            weight: 商品重量，单位kg
            description: 商品描述信息
            price: 商品单价，单位元
        """
        self.title = title
        self.weight = weight
        self.description = description
        self.price = price

    def get_price_for_quantity(self, quantity: int) -> float:
        """计算指定数量商品的总价
        
        Args:
            quantity: 商品数量
            
        Returns:
            商品总价
        """
        return self.price * quantity

    def get_weight(self) -> float:
        """获取商品重量
        
        Returns:
            商品重量(kg)
        """
        return self.weight

class OrderDetail:
    """订单详情类，关联商品和购买数量
    
    Attributes:
        product: 商品对象
        quantity: 购买数量
    """
    
    def __init__(self, product: Product, quantity: int) -> None:
        """初始化订单详情
        
        Args:
            product: 关联的商品对象
            quantity: 购买数量
        """
        self.product = product
        self.quantity = quantity

    def calculate_sub_total(self) -> float:
        """计算当前商品小计金额
        
        Returns:
            商品小计金额
        """
        return self.product.get_price_for_quantity(self.quantity)

    def calculate_weight(self) -> float:
        """计算当前商品总重量
        
        Returns:
            商品总重量(kg)
        """
        return self.product.get_weight() * self.quantity

class Payment:
    """支付信息类，记录支付金额
    
    Attributes:
        amount: 支付金额
    """
    
    def __init__(self, amount: float) -> None:
        """初始化支付信息
        
        Args:
            amount: 支付金额，单位元
        """
        self.amount = amount

class Order:
    """订单类，整合客户、支付和商品详情信息
    
    Attributes:
        create_date: 订单创建日期
        status: 订单状态
        customer: 客户对象
        payment: 支付信息
        details: 订单商品详情列表
    """
    
    def __init__(self, create_date: date, status: OrderStatus, 
                 customer: Customer, payment: Payment) -> None:
        """初始化订单对象
        
        Args:
            create_date: 订单创建日期
            status: 订单状态
            customer: 关联的客户对象
            payment: 关联的支付信息
        """
        self.create_date = create_date
        self.status = status
        self.customer = customer
        self.payment = payment
        self.details: List[OrderDetail] = []

    def add_detail(self, detail: OrderDetail) -> None:
        """添加订单商品详情
        
        Args:
            detail: 订单详情对象
        """
        self.details.append(detail)

    def get_total_amount(self) -> float:
        """计算订单总金额
        
        Returns:
            订单总金额，单位元
        """
        return sum(detail.calculate_sub_total() for detail in self.details)

    def get_total_weight(self) -> float:
        """计算订单总重量
        
        Returns:
            订单总重量，单位kg
        """
        return sum(detail.calculate_weight() for detail in self.details)

def validate_non_empty(value: str) -> bool:
    """验证字符串非空
    
    Args:
        value: 输入字符串
        
    Returns:
        验证结果，True表示有效
    """
    return len(value.strip()) > 0

def validate_positive_float(value: str) -> bool:
    """验证正浮点数
    
    Args:
        value: 输入字符串
        
    Returns:
        验证结果，True表示有效
    """
    try:
        float_val = float(value)
        return float_val > 0
    except ValueError:
        return False

def validate_non_negative_float(value: str) -> bool:
    """验证非负浮点数
    
    Args:
        value: 输入字符串
        
    Returns:
        验证结果，True表示有效
    """
    try:
        float_val = float(value)
        return float_val >= 0
    except ValueError:
        return False

def validate_positive_int(value: str) -> bool:
    """验证正整数
    
    Args:
        value: 输入字符串
        
    Returns:
        验证结果，True表示有效
    """
    try:
        int_val = int(value)
        return int_val > 0 and value.isdigit()
    except ValueError:
        return False

def validate_yes_no(value: str) -> bool:
    """验证是否为是/否回答
    
    Args:
        value: 输入字符串
        
    Returns:
        验证结果，True表示有效
    """
    return value.strip() in ["是", "否"]

def get_valid_input(prompt: str, validator: Callable[[str], bool], 
                    error_msg: Optional[str] = None) -> str:
    """通用输入验证函数，循环获取有效输入
    
    Args:
        prompt: 提示信息
        validator: 验证函数
        error_msg: 错误提示，可选
        
    Returns:
        验证通过的输入值
    """
    while True:
        user_input = input(prompt).strip()
        if validator(user_input):
            return user_input
        print(error_msg or "输入无效，请重试")

def input_customer_info() -> Customer:
    """收集客户信息并创建Customer对象
    
    Returns:
        客户对象
    """
    print("=== 客户信息输入 ===")
    name = get_valid_input("姓名：", validate_non_empty, "姓名不能为空")
    contact = get_valid_input("联系电话：", validate_non_empty, "联系电话不能为空")
    address = get_valid_input("邮寄地址：", validate_non_empty, "邮寄地址不能为空")
    
    active_input = get_valid_input(
        "是否激活（是/否）：", 
        validate_yes_no,
        "请输入'是'或'否'"
    )
    active = active_input == "是"
    
    return Customer(name, contact, address, active)

def input_product_info() -> OrderDetail:
    """收集商品信息并创建OrderDetail对象
    
    Returns:
        订单详情对象
    """
    print("\n=== 商品信息输入 ===")
    title = get_valid_input("商品名称：", validate_non_empty, "商品名称不能为空")
    
    weight = float(get_valid_input(
        "单件重量（kg）：", 
        validate_positive_float,
        "请输入有效的正浮点数"
    ))
    
    description = input("商品描述：").strip()
    
    price = float(get_valid_input(
        "单件价格（元）：", 
        validate_non_negative_float,
        "请输入有效的非负浮点数"
    ))
    
    quantity = int(get_valid_input(
        "购买数量：", 
        validate_positive_int,
        "请输入有效的正整数"
    ))
    
    product = Product(title, weight, description, price)
    return OrderDetail(product, quantity)

def create_order(customer: Customer, detail: OrderDetail) -> Order:
    """创建订单对象并处理支付信息
    
    Args:
        customer: 客户对象
        detail: 订单详情对象
        
    Returns:
        订单对象
    """
    print("\n=== 支付信息 ===")
    amount = detail.calculate_sub_total()
    payment = Payment(amount)
    
    order = Order(date.today(), "PAID", customer, payment)
    order.add_detail(detail)
    return order

def display_order_summary(order: Order) -> None:
    """显示订单摘要信息
    
    Args:
        order: 订单对象
    """
    print("\n=== 订单结果 ===")
    print(f"客户：{order.customer.name}")
    print(f"总金额：{order.get_total_amount():.2f}元")
    print(f"总重量：{order.get_total_weight():.2f}kg")

def main() -> None:
    """程序主入口函数"""
    try:
        customer = input_customer_info()
        detail = input_product_info()
        order = create_order(customer, detail)
        display_order_summary(order)
    except KeyboardInterrupt:
        print("\n操作已取消")
    except ValueError as ve:
        print(f"输入值错误：{str(ve)}")
    except Exception as e:
        print(f"发生未知错误：{str(e)}")

if __name__ == "__main__":
    main()