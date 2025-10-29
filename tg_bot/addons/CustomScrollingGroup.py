from typing import Dict, List, Optional

from aiogram.types import CallbackQuery, InlineKeyboardButton

from typing import Optional
from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.widgets.kbd import ScrollingGroup
from aiogram_dialog.widgets.common import WhenCondition, OnPageChangedVariants


class CustomScrollingGroup(ScrollingGroup):
    def __init__(
        self,
        *buttons,
        id: str,
        width: Optional[int] = None,
        height: int = 0,
        when: WhenCondition = None,
        on_page_changed: OnPageChangedVariants = None,
        hide_on_single_page: bool = False,
        hide_pager: bool = False,
    ):
        super().__init__(
            *buttons, id=id, width=width, height=height, when=when,
            on_page_changed=on_page_changed, hide_on_single_page=hide_on_single_page,
            hide_pager=hide_pager
        )

    async def _render_pager(
        self,
        pages: int,
        manager: DialogManager
    ) -> RawKeyboard:
        if self.hide_pager:
            return []
        if pages == 0 or (pages == 1 and self.hide_on_single_page):
            return []

        last_page = pages - 1
        current_page = min(last_page, await self.get_page(manager))
        next_page = min(last_page, current_page + 1)
        prev_page = max(0, current_page - 1)

        return [
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=self._item_callback_data(prev_page),
                ),
                InlineKeyboardButton(
                    text=str(current_page + 1)+"/"+str(pages),
                    callback_data=self._item_callback_data(current_page),
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=self._item_callback_data(next_page),
                ),
            ]
        ]
