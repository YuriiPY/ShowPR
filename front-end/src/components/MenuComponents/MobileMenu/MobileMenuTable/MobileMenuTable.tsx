'use client'

import { useLocale } from 'next-intl'
import Image from 'next/image'
import React, { useEffect, useRef } from 'react'

import { useInView } from 'react-intersection-observer'
import { useStoreContext } from '../../Menu/Menu'
import MobileProductCard from '../MobileProductCard/MobileProductCard'
import styles from './MobileMenuTable.module.scss'


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

interface MobileMenuTableProps {
    menuData: MenuData,
    selectedTable: string,
    tableInView: string,
    setTableInView: React.Dispatch<React.SetStateAction<string>>
}

const MobileMenuTable = React.memo(({ menuData, selectedTable, setTableInView }: MobileMenuTableProps) => {

    const tableRefs = useRef<{ [key: string]: HTMLDivElement | null }>({})

    useEffect(() => {
        const targetElement = tableRefs.current[selectedTable]

        targetElement?.scrollIntoView({ behavior: "smooth", block: "start" })
    }, [selectedTable])

    return (
        Object.entries(menuData).map(([tableName, tableData], index) => {

            return (
                <Table
                    key={index}
                    tableName={tableName}
                    tableData={tableData}
                    selectedTable={selectedTable}
                    setTableInView={setTableInView}
                />
            )
        }

        )

    )

})


interface TableProps {
    tableName: string,
    tableData: { [key: string]: MenuItem },
    selectedTable: string,
    setTableInView: React.Dispatch<React.SetStateAction<string>>
}


const Table = React.memo(({ tableName, tableData, selectedTable, setTableInView }: TableProps) => {

    const store = useStoreContext()

    const locale = useLocale()

    const tableRef = useRef<HTMLDivElement | null>(null)
    const [ref, inView] = useInView({
        threshold: 0.1
    })

    useEffect(() => {
        if (inView) {
            setTableInView(tableName)
        }
    }, [inView, tableName, setTableInView])

    useEffect(() => {
        if (selectedTable === tableName && tableRef.current) {
            tableRef.current.scrollIntoView({ behavior: "smooth", block: "start" })
        }
    }, [selectedTable, tableName])

    const upperTableName = tableName.charAt(0).toUpperCase() + tableName.slice(1)
    return (
        <div
            ref={(el) => {
                tableRef.current = el
                ref(el)
            }}
            className={styles.menuFoodList}>
            <div className={styles.tableMenuTitle}>
                <h1>{upperTableName}</h1>
                <Image src={'/icons/under-line.png'} alt={''} width={200} height={10} />
            </div>
            <div className={styles.menuProductCardContainer}>
                {Object.entries(tableData).map(([itemId, itemData]) => {
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
                        <MobileProductCard
                            key={itemId}
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
                }
                )}
            </div>
        </div>
    )
})

MobileMenuTable.displayName = 'MobileMenuTable'
Table.displayName = 'Table'

export default MobileMenuTable

