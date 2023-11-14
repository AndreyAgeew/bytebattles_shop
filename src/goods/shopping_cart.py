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

    def __iter__(self):
        # Возвращаем итератор по элементам корзины
        return iter(self.items)

    @overload
    async def add_item(self, item: Goods) -> None:
        ...

    @overload
    async def add_item(self, item: List[Goods]) -> None:
        ...

    async def add_item(self, item: Union[Goods, List[Goods]]) -> None:
        """
        Асинхронно добавляет товар(ы) в корзину.

        Parameters:
            item (Union[Goods, List[Goods]]): Товар или список товаров для добавления в корзину.
        """
        if isinstance(item, list):
            for i in item:
                if i in self.items:
                    raise ValueError(f"Товар {i} уже есть в корзине.")
            self.items.extend(item)
        else:
            if item in self.items:
                raise ValueError(f"Товар {item} уже есть в корзине.")
            self.items.append(item)

    async def remove_item(self, item: Goods) -> None:
        """
        Удаляет товар из корзины.

        Parameters:
            item (Goods): Товар для удаления из корзины.
        """
        if item not in self.items:
            raise ValueError(f"Товар {item} не найден в корзине.")
        self.items.remove(item)

    async def clear_cart(self) -> None:
        """
        Полностью очищает корзину.
        """
        self.items = []

    async def get_total_price(self) -> Optional[float]:
        """
        Возвращает общую стоимость товаров в корзине.

        Returns:
            Optional[float]: Общая стоимость товаров в корзине. Если корзина пуста, возвращает None.
        """
        if not self.items:
            return None
        total_price = sum(item.price * item.quantity for item in self.items)
        return total_price
