'use client'

import React, { useState } from 'react'

import styles from './MobileMenu.module.scss'
import MobileMenuTable from './MobileMenuTable/MobileMenuTable'
import MobileMenuTabs from './MobileMenuTabs/MobileMenuTabs'

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

const MobileMenu = React.memo(({ menuData, tableNames }: MenuTableProps) => {


    const [selectedTable, setSelectedTable] = useState<string>("")

    const [tableInView, setTableInView] = useState<string>("")


    return (
        <div className={styles.menuTab}>
            <div className={styles.tabPane}>
                <div className={styles.container}>
                    <div className={styles.menuFoodSelector}>
                        <div className={styles.containerBtnSelector}>
                            <h2>Menu</h2>
                            <div className={styles.selectorGroup}>
                                <MobileMenuTabs
                                    tableNames={tableNames}
                                    selectedTable={selectedTable}
                                    tableInView={tableInView}
                                    setSelectedTable={setSelectedTable} />
                            </div>
                        </div>
                    </div>
                </div>
                <div className={styles.menuClassListContainer}>
                    <MobileMenuTable
                        menuData={menuData}
                        selectedTable={selectedTable}
                        tableInView={tableInView}
                        setTableInView={setTableInView}
                    />
                </div>
            </div>
        </div>
    )
})

MobileMenu.displayName = 'MobileMenu'

export default MobileMenu