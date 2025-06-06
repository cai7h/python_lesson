from datetime import datetime
from typing import Dict, List, Optional


class Product:
    """商品信息类
    
    Attributes:
        barcode (str): 商品唯一条码（主键）
        name (str): 商品名称
        price (float): 商品单价（元）
        stock (int): 当前库存数量（件）
    """
    
    def __init__(self, barcode: str, name: str, price: float, stock: int) -> None:
        """商品对象初始化
        
        Args:
            barcode: 商品条码（唯一标识，长度5-10位数字）
            name: 商品名称（不超过20字符）
            price: 商品单价（元，≥0）
            stock: 库存数量（件，≥0）
        """
        self.barcode: str = barcode
        self.name: str = name
        self.price: float = price
        self.stock: int = stock


class CartItem:
    """购物车条目类
    
    Attributes:
        product (Product): 关联的商品对象
        quantity (int): 购买数量（正整数）
    """
    
    def __init__(self, product: Product, quantity: int) -> None:
        """购物车条目初始化
        
        Args:
            product: 关联的商品对象（必须有效）
            quantity: 购买数量（必须为≥1的整数）
            
        Raises:
            ValueError: 当quantity≤0时抛出
        """
        if quantity < 1:
            raise ValueError("购买数量必须大于0")
        self.product: Product = product
        self.quantity: int = quantity


class Cart:
    """购物车管理类
    
    Attributes:
        items (List[CartItem]): 购物车中的商品条目列表
    """
    
    def __init__(self) -> None:
        self.items: List[CartItem] = []

    def add_item(self, product: Product, quantity: int) -> None:
        """向购物车添加商品（自动扣减库存）
        
        Args:
            product: 要添加的商品对象
            quantity: 购买数量（≥1的整数）
            
        注意：库存不足时会打印提示，不会添加条目
        """
        try:
            if quantity < 1:
                raise ValueError("数量必须大于0")
                
            if product.stock >= quantity:
                self.items.append(CartItem(product, quantity))
                product.stock -= quantity
            else:
                print(f"❗库存不足：{product.name} 仅剩 {product.stock} 件")
        except ValueError as e:
            print(f"❌ 无效数量：{str(e)}")

    def calculate_total(self) -> float:
        """计算购物车总金额
        
        Returns:
            总金额（元，保留2位小数）
        """
        return round(sum(item.product.price * item.quantity for item in self.items), 2)


class PaymentProcessor:
    """支付处理类（支持现金/扫码支付）
    
    Attributes:
        SUPPORTED_METHODS (set[str]): 支持的支付方式集合
    """
    
    SUPPORTED_METHODS: set[str] = {'cash', 'qr'}
    
    def process_payment(self, amount: float, method: str = 'cash') -> bool:
        """执行支付操作
        
        Args:
            amount: 支付金额（元，≥0）
            method: 支付方式（'cash'现金/'qr'扫码）
            
        Returns:
            支付成功返回True，失败返回False
            
        Raises:
            ValueError: 当amount<0时抛出
        """
        if amount < 0:
            raise ValueError("支付金额不能为负数")
            
        print(f"\n正在处理支付：方式={method}, 金额=¥{amount:.2f}")
        
        if method not in self.SUPPORTED_METHODS:
            print("❌ 不支持的支付方式（仅支持cash/qr）")
            return False
            
        if method == 'cash':
            print(f"✅ 现金支付成功：¥{amount:.2f}")
        elif method == 'qr':
            print(f"📱 扫码支付成功：¥{amount:.2f}")
            
        return True


class ReceiptPrinter:
    """电子收据打印机类
    
    Attributes:
        HEADER_TEMPLATE (str): 收据头部模板
        ITEM_TEMPLATE (str): 商品条目模板
        FOOTER_TEMPLATE (str): 收据尾部模板
    """
    
    HEADER_TEMPLATE: str = "====== 收据 Receipt ======\n时间：{timestamp}\n"
    ITEM_TEMPLATE: str = "{name} x {quantity} = ¥{subtotal:.2f}"
    FOOTER_TEMPLATE: str = "\n总计 Total: ¥{total:.2f}\n=========================="
    
    def print_receipt(self, cart: Cart) -> None:
        """打印格式化收据
        
        Args:
            cart: 已结算的购物车对象（必须非空）
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(self.HEADER_TEMPLATE.format(timestamp=timestamp))
        
        for item in cart.items:
            subtotal = item.product.price * item.quantity
            print(self.ITEM_TEMPLATE.format(
                name=item.product.name,
                quantity=item.quantity,
                subtotal=subtotal
            ))
            
        print(self.FOOTER_TEMPLATE.format(total=cart.calculate_total()))


def load_demo_products() -> Dict[str, Product]:
    """加载示例商品数据（模拟数据库查询）
    
    Returns:
        商品字典（键：条码，值：商品对象）
    """
    return {
        "1": Product("1", "农夫山泉 water", 2.0, 5),
        "2": Product("2", "雪碧 spirit", 3.0, 10),
        "3": Product("3", "可乐 Coke", 3.0, 20)
    }


def display_product_list(products: Dict[str, Product]) -> None:
    """显示当前可购买的商品列表
    
    Args:
        products: 商品字典（键：条码）
    """
    print("📦 商品列表:")
    for code, product in products.items():
        print(f"{code}: {product.name} - ¥{product.price:.2f} (库存: {product.stock})")


def collect_user_input(products: Dict[str, Product], cart: Cart) -> None:
    """收集用户输入的商品条码和数量
    
    Args:
        products: 商品字典（键：条码）
        cart: 目标购物车对象
    """
    while True:
        barcode = input("\n请输入商品条码（或输入 q 结账）：").strip()
        
        if barcode.lower() == 'q':
            break
            
        if barcode not in products:
            print("❌ 商品条码无效")
            continue
            
        try:
            quantity = int(input("请输入购买数量："))
            cart.add_item(products[barcode], quantity)
        except ValueError:
            print("❌ 请输入有效的正整数")


def main_checkout_process(cart: Cart) -> None:
    """主结账流程处理
    
    Args:
        cart: 当前购物车对象
    """
    if not cart.items:
        print("🛒 购物车为空，已退出")
        return
        
    total = cart.calculate_total()
    print(f"\n🧾 应付总额：¥{total:.2f}")
    
    payment_method = input("请输入支付方式（cash/扫码支付输入qr）：").strip().lower()
    processor = PaymentProcessor()
    
    try:
        if processor.process_payment(total, payment_method):
            ReceiptPrinter().print_receipt(cart)
        else:
            _rollback_stock(cart)
    except Exception as e:
        print(f"⚠️ 支付异常：{str(e)}")
        _rollback_stock(cart)


def _rollback_stock(cart: Cart) -> None:
    """库存回滚（支付失败时恢复库存）
    
    Args:
        cart: 需要回滚的购物车对象
    """
    print("⚠️ 支付失败，回滚库存...")
    for item in cart.items:
        item.product.stock += item.quantity
    cart.items.clear()


if __name__ == "__main__":
    try:
        demo_products = load_demo_products()
        shopping_cart = Cart()
        
        display_product_list(demo_products)
        collect_user_input(demo_products, shopping_cart)
        main_checkout_process(shopping_cart)
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"系统异常：{str(e)}")