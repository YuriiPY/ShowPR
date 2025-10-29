"use client"

import Image from 'next/image'
import React, { useEffect, useMemo, useRef, useState } from 'react'

import clsx from 'clsx'
import { useLocale } from 'next-intl'
import { useStoreContext } from '../../Menu/Menu'
import ProductCard from '../ProductCard/ProductCard'
import styles from './MenuTable.module.scss'

type MenuItem = {
    price: number
    id: number
    img: string
    type: "by portion" | "by weight"
    name: string
    name_ua: string
    name_pl: string
    description: string
    description_ua: string
    description_pl: string
    status: boolean
}

type MenuData = {
    [key: string]: { [key: string]: MenuItem }

}

type TableNames = {
    [key: string]: { [key: string]: string }
}


type MenuTableProps = {
    menuData: MenuData,
    tableNames: TableNames
}

const MenuTable = React.memo(({ menuData, tableNames }: MenuTableProps) => {
    const store = useStoreContext()

    const locale = useLocale()

    const [selectedTable, setSelectedTable] = useState<keyof MenuData>()

    const focusContentRef = useRef<HTMLButtonElement | null>(null)

    const menuTabsRefs = useRef<{ [key: string]: HTMLButtonElement | null }>({})

    useEffect(() => {
        setSelectedTable(Object.keys(menuData)[0])
    }, [menuData])


    const menuTabs = useMemo(() => (
        Object.entries(tableNames).map(([tableName, translatedValue], index) => {
            const translatedTableName = translatedValue["translation_" + locale]
            return (
                <div key={index} className={styles.selectorBtnContainer}>
                    <button
                        ref={(el) => {
                            menuTabsRefs.current[tableName] = el
                        }}
                        onClick={() => {
                            setSelectedTable(tableName)
                        }}
                        onKeyDown={(e) => {
                            if (e.key === "ArrowRight" && focusContentRef.current) {
                                focusContentRef.current.focus()
                            }
                        }}
                        className={styles.submenuBtn}
                    >
                        <span className={clsx(styles.submenuBtnText, { [styles.selected]: selectedTable === tableName })}>{translatedTableName}</span>
                    </button>
                </div>
            )
        })
    ), [tableNames, selectedTable, locale])


    const Menu = useMemo(() => (
        Object.entries(menuData).map(([tableName, tableData], index) => {
            if (tableName === selectedTable) {
                return (
                    <div key={index} className={styles.menuFoodList}>
                        <div className={styles.tableMenuTitle}>
                            <h1>{tableNames[tableName]["translation_" + locale]}</h1>
                            <Image aria-hidden={true} src={'/icons/under-line.png'} alt={''} width={200} height={10} />
                        </div>
                        <div className={styles.menuProductCardContainer}>
                            {Object.entries(tableData).map(([itemId, itemData], index) => {
                                const name = {
                                    "en": itemData.name,
                                    "ua": itemData.name_ua,
                                    "pl": itemData.name_pl,
                                }[locale]!

                                const description = {
                                    "en": itemData.description,
                                    "ua": itemData.description_ua,
                                    "pl": itemData.description_pl,
                                }[locale]!

                                return (
                                    <ProductCard
                                        key={itemId}
                                        index={index}
                                        ref={focusContentRef}
                                        menuTabsRef={menuTabsRefs}
                                        tableName={tableName}
                                        itemId={Number(itemId)}
                                        name={name}
                                        img={itemData.img}
                                        description={description}
                                        price={itemData.price}
                                        type={itemData.type}
                                        status={store ? itemData.status : store}
                                    />
                                )
                            })}
                        </div>
                    </div>
                )
            }

        })

    ), [menuData, selectedTable, tableNames, locale, store])

    return (
        <div className={styles.menuTab}>
            <div className={styles.tabPane}>
                <div className={styles.container}>
                    <div className={styles.menuFoodSelector}>
                        <div className={styles.containerBtnSelector}>
                            <h2>Menu</h2>
                            <div className={styles.selectorGroup}>
                                {menuTabs}
                            </div>
                        </div>
                    </div>
                </div>
                <div className={styles.menuClassListContainer}>
                    {Menu}
                </div>
            </div>
        </div>
    )
})

MenuTable.displayName = 'MenuTable'

export default MenuTable
