'use client'

import { createContext, memo, useContext, useEffect, useRef, useState } from 'react'

import MobileMenu from '../MobileMenu/MobileMenu'
import styles from './Menu.module.scss'

import { SmallLoadingWindow } from '@/components/Loading/SmallLoadingWindow/SmallLoadingWindow'
import { useTranslations } from 'next-intl'
import "react-spring-bottom-sheet/dist/style.css"
import FrozenMenuIcon from '../../svgIcons/frozenMenu'
import HotMenuIcon from '../../svgIcons/hotMenu'
import MenuTable from '../DesktopMenu/MenuTable/MenuTable'


type MenuItem = {
    tableName: string
    id: number
    price: number
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

type TableNames = {
    [key: string]: { [key: string]: string }
}

type MenuData = {
    Menu: {
        cookedMenu: {
            [key: string]: { [key: string]: MenuItem }
        }
        frozenMenu: {
            [key: string]: { [key: string]: MenuItem }
        }
    }
    TableNames: {
        cookedTableNames: TableNames
        frozenTableNames: TableNames
    }
}

type StoreStatus = {
    isOpen: boolean
    until: string
    changedAt: string
}

const StoreContext = createContext<boolean>(false)

const Menu = memo(function Menu() {
    const t = useTranslations("MenuStaticText")
    const screenReaderText = useTranslations("TextForScreenReader.menuText")

    const [menuData, setMenuData] = useState<MenuData>({
        TableNames: {
            cookedTableNames: {},
            frozenTableNames: {}
        },
        Menu: {
            cookedMenu: {},
            frozenMenu: {}
        }
    })

    const [storeStatus, setStoreStatus] = useState<StoreStatus>({
        isOpen: false,
        until: "",
        changedAt: ""
    })

    const tabRef = useRef<HTMLDivElement | null>(null)
    useEffect(() => {
        tabRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
    }, [])


    const [selectedTableType, setSelectedTableType] = useState<keyof MenuData["Menu"]>("cookedMenu")

    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL
    const apiUrlGetMenu = new URL("products/get-menu", backendUrl).href
    const apiUrlGetStoreStatus = new URL("store/status", backendUrl).href

    const [windowWidth, setWindowWidth] = useState<number | null>(null)

    const [isMenuDataLoading, setIsMenuDataLoading] = useState(true)

    useEffect(() => {
        if (typeof window !== 'undefined') setWindowWidth(window.innerWidth)

        const fetchData = async () => {
            try {
                const response = await fetch(apiUrlGetMenu)

                if (!response.ok) {
                    throw new Error(`Failed to fetch data from ${apiUrlGetMenu}`)
                }
                const data = await response.json()
                setMenuData(data)
                console.log("MENU->", data)
            } catch (error) {
                console.error(error)
            }
        }

        const fetchStoreStatus = async () => {
            try {
                const response = await fetch(apiUrlGetStoreStatus)

                if (!response.ok) {
                    throw new Error(`Failed to fetch data from ${apiUrlGetStoreStatus}`)
                }

                const data = await response.json()
                setStoreStatus(data)
                setIsMenuDataLoading(false)
            } catch (error) {
                console.error(error)
            }
        }

        fetchData()
        fetchStoreStatus()
    }, [apiUrlGetMenu, apiUrlGetStoreStatus])



    return (
        <>
            <div ref={tabRef} className={styles.container}>
                <div className={styles.column}>
                    <h1>{t("title")}</h1>
                    {
                        !storeStatus.isOpen
                            ? storeStatus.until
                                ? <div className={styles.closeTimeContainer}>
                                    <h2>Store is closed until {storeStatus.until}</h2>
                                </div>
                                : <div className={styles.closeTimeContainer}>
                                    <h2>Store is close before open</h2>
                                </div>
                            : null
                    }
                </div>
                <div className={styles.tablistMenu}>
                    <div className={styles.row}>
                        <nav className={styles.selector}>
                            <button
                                type='button'
                                aria-label={screenReaderText("navigation.chooseMenu.cookedButton")}
                                disabled={selectedTableType === "cookedMenu"} onClick={() => {
                                    setSelectedTableType("cookedMenu")
                                }} className={styles.btnTableSelector}>
                                <span><HotMenuIcon /></span>
                                {t("tabsButtonName.cooked")}
                            </button>
                            <button
                                type='button'
                                aria-label={screenReaderText("navigation.chooseMenu.frozenButton")}
                                disabled={selectedTableType === "frozenMenu"} onClick={() => {
                                    setSelectedTableType("frozenMenu")
                                }} className={styles.btnTableSelector}>
                                <span><FrozenMenuIcon /></span>
                                {t("tabsButtonName.frozen")}
                            </button>
                        </nav>
                    </div>
                </div>
                {
                    isMenuDataLoading ?
                        <div className={styles.Loading}>
                            <div className={styles.parentLoadingContainer}>
                                <SmallLoadingWindow />
                            </div>
                        </div>
                        : (
                            windowWidth !== null && windowWidth <= 768
                                ? <StoreContext.Provider value={storeStatus?.isOpen}>
                                    <MobileMenu menuData={menuData["Menu"][selectedTableType]} tableNames={
                                        selectedTableType === "cookedMenu"
                                            ? menuData["TableNames"]["cookedTableNames"]
                                            : menuData["TableNames"]["frozenTableNames"]
                                    } />
                                </StoreContext.Provider>
                                :
                                <StoreContext.Provider value={storeStatus?.isOpen}>
                                    <MenuTable menuData={menuData["Menu"][selectedTableType]} tableNames={
                                        selectedTableType === "cookedMenu"
                                            ? menuData["TableNames"]["cookedTableNames"]
                                            : menuData["TableNames"]["frozenTableNames"]
                                    } />
                                </StoreContext.Provider>
                        )
                }
            </div >
        </>
    )
}
)

export const useStoreContext = () => {
    const context = useContext(StoreContext)
    return context
}

export default Menu

