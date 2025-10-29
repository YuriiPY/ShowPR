'use client'

import clsx from 'clsx'
import React, { useEffect, useRef } from 'react'
import { useInView } from 'react-intersection-observer'
import { useLocale } from 'next-intl'
import { useSearchParams } from 'next/navigation'

import styles from './MobileMenuTabs.module.scss'

type TableNames = {
    [key: string]: { [key: string]: string }
}

interface MobileMenuTabsProps {
    tableNames: TableNames,
    selectedTable: string,
    tableInView: string,
    setSelectedTable: (tableName: string) => void
}

const MobileMenuTabs = React.memo(({ tableNames, selectedTable, tableInView, setSelectedTable }: MobileMenuTabsProps) => {

    const searchParams = useSearchParams()
    const tab = searchParams.get('tab')

    const locale = useLocale()

    const { ref, inView } = useInView({
        rootMargin: '0px 0px 100% 0px'
    })

    const tabsRefs = useRef<{ [key: string]: HTMLDivElement | null }>({})

    useEffect(() => {

        if (tab) {
            setSelectedTable(tab)
        }
    }, [setSelectedTable, tab])

    useEffect(() => {
        if (selectedTable !== tableInView) {
            setSelectedTable("")
        }

        const targetElement = tabsRefs.current[tableInView]

        targetElement?.scrollIntoView({ behavior: "smooth", block: "start" })
    }, [selectedTable, tableInView, setSelectedTable])

    return (
        <div ref={ref}>
            <div className={clsx(styles.selectorGroupContainer, { [styles.selectorGroupFixed]: !inView })}>
                {
                    Object.entries(tableNames).map(([tableName, translatedValue], index) => {

                        const translatedTableName = translatedValue["translation_" + locale]

                        const upperTableName = translatedTableName.charAt(0).toUpperCase() + tableName.slice(1)
                        return (
                            <div key={index}
                                ref={(el) => { tabsRefs.current[tableName] = el }}
                                className={styles.selectorBtnContainer}>
                                <button className={styles.submenuBtn} onClick={() => {
                                    setSelectedTable(tableName)
                                }}>
                                    <span className={clsx(styles.submenuBtnText, { [styles.selected]: tableInView === tableName })}>{upperTableName}</span>
                                </button>
                            </div>
                        )
                    }
                    )
                }
            </div>
        </div>
    )
})

MobileMenuTabs.displayName = 'MobileMenuTabs'

export default MobileMenuTabs