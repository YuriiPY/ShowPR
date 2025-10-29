'use client'

import clsx from 'clsx'
import { motion } from 'framer-motion'
import { useTranslations } from 'next-intl'
import { usePathname } from 'next/navigation'
import SegmentedButton from '../../buttons/SegmentedButton/SegmentedButton'
import style from './ActiveHeader.module.scss'

// type HeaderProps = {
//     customStyle: string | React.CSSProperties
// }


export default function ActiveHeader(
    // { customStyle }: HeaderProps
) {
    const firstPathName = usePathname()
    const pathName = firstPathName.slice(3)
    const t = useTranslations("NavigateButtons")


    const NavigationButtonData = [
        {
            buttonName: t("home"),
            link: "/",
            isSelected: pathName === '/'
        },
        {
            buttonName: t("menu"),
            link: "/menu",
            isSelected: pathName === '/menu'
        },
        {
            buttonName: t("contacts"),
            link: "/contacts",
            isSelected: pathName === '/contacts'
        }
    ]

    return (
        <motion.div
            className={clsx(style.activeHeader)}
            initial={{ y: -300 }}
            animate={{ y: 0 }}
            exit={{ y: -300 }}
            transition={{ duration: .9, ease: "easeInOut" }}
        >
            <div className={style.activeContent}>
                <div className={style.col_1}>
                    <div className={style.mainMenu}>
                        <nav aria-hidden={true} className={style.navigationActive}>
                            <SegmentedButton type={"text"} buttonsList={NavigationButtonData} hoverType={'changeColor'} selfSelect={false} selectType={'hoverStyle'} />
                        </nav>
                    </div >
                </div>
            </div >
        </motion.div >
    )
}