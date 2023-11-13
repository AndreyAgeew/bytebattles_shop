from typing import List, Union, Optional, overload

from goods.models import Goods


class ShoppingCart:
    """
    Класс корзины для товаров.

    Attributes:
        items (List[Goods]): Список товаров в корзине.

    Methods:
        add_item(item: Union[Goods, List[Goods]]) -> None:
            Добавляет товар(ы) в корзину.

        remove_item(item: Goods) -> None:
            Удаляет товар из корзины.

        clear_cart() -> None:
            Полностью очищает корзину.

        get_total_price() -> Optional[float]:
            Возвращает общую стоимость товаров в корзине. Если корзина пуста, возвращает None.

    """

    def __init__(self):
        self.items: List[Goods] = []

    @overload
    def add_item(self, item: Goods) -> None:
        ...

    @overload
    def add_item(self, item: List[Goods]) -> None:
        ...

    def add_item(self, item: Union[Goods, List[Goods]]) -> None:
        """
        Добавляет товар(ы) в корзину.

        Parameters:
            item (Union[Goods, List[Goods]]): Товар или список товаров для добавления в корзину.
        """
        if isinstance(item, list):
            self.items.extend(item)
        else:
            self.items.append(item)

    def remove_item(self, item: Goods) -> None:
        """
        Удаляет товар из корзины.

        Parameters:
            item (Goods): Товар для удаления из корзины.
        """
        if item in self.items:
            self.items.remove(item)

    def clear_cart(self) -> None:
        """
        Полностью очищает корзину.
        """
        self.items = []

    def get_total_price(self) -> Optional[float]:
        """
        Возвращает общую стоимость товаров в корзине.

        Returns:
            Optional[float]: Общая стоимость товаров в корзине. Если корзина пуста, возвращает None.
        """
        if not self.items:
            return None
        total_price = sum(item.price * item.quantity for item in self.items)
        return total_price