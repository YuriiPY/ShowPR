'use client'
import { useTranslations } from 'next-intl'
import Image from 'next/image'

import AboutChildComponent from '../AboutAreaChild/AboutAreaChild'
import styles from './AboutArea.module.scss'
import { useEffect, useMemo, useState } from 'react'

type AreaItem = {
    title: string,
    description: string,
    imgBig: string,
    imgSmall: string,
    slug: string,
}

type AreaInfo = AreaItem & { link: string }

export default function AboutArea() {
    const t = useTranslations("MainPage.MainArea")


    const [areaInfo, setAreaInfo] = useState<AreaInfo[]>([])


    const areaItems: AreaItem[] = useMemo(() => [
        {
            title: t("areaInfo1.title"),
            description: t("areaInfo1.description"),
            imgBig: "/MainPage/AboutArea/BigImg/dumplings1.jpg",
            imgSmall: "/MainPage/AboutArea/SmallImg/dessert2.jpg",
            slug: "dumplings"
        },
        {
            title: t("areaInfo2.title"),
            description: t("areaInfo2.description"),
            imgBig: "/MainPage/AboutArea/BigImg/dessert.jpg",
            imgSmall: "/MainPage/AboutArea/SmallImg/dumplings2.jpg",
            slug: "soups"
        },
        {
            title: t("areaInfo3.title"),
            description: t("areaInfo3.description"),
            imgBig: "/MainPage/AboutArea/BigImg/dessert.jpg",
            imgSmall: "/MainPage/AboutArea/SmallImg/dumplings2.jpg",
            slug: "meats"
        }
    ], [t])

    useEffect(() => {

        const baseUrl = new URL(window.location.href)
        baseUrl.pathname = "/menu"

        const enrichedAreaInfo: AreaInfo[] = areaItems.map((item) => {
            const url = new URL(baseUrl)
            url.searchParams.set("tab", item.slug)

            return {
                ...item,
                link: url.toString()
            }
        })

        setAreaInfo(enrichedAreaInfo)

    }, [areaItems])

    return (
        <section className={styles.aboutArea}>
            <div aria-hidden={true} className={styles.icon1}>
                <Image src="/icons/AboutAreaIcons/1.png" alt="icon1" width={150} height={200} />
            </div>
            <div aria-hidden={true} className={styles.icon2}>
                <Image src="/icons/AboutAreaIcons/2.png" alt="icon2" width={150} height={150} />
            </div>
            <div aria-hidden={true} className={styles.icon3}>
                <Image src="/icons/AboutAreaIcons/3.png" alt="icon3" width={150} height={130} />
            </div>
            <div className={styles.container}>
                <div className={styles.stable}>
                    {areaInfo.map((item, index) => (
                        < AboutChildComponent key={index} id={index} title={item.title} description={item.description} imgBig={item.imgBig} imgSmall={item.imgSmall} link={item.link} />
                    ))}
                    <ul className={styles.foodList}>
                        <li>
                            <Image src="/icons/AboutAreaIcons/fresh-ingredients.png" alt="icon3" width={50} height={50} />
                            <span>Fresh Ingredients</span>
                        </li>
                        <li>
                            <Image src="/icons/AboutAreaIcons/dumplings-board.png" alt="icon3" width={50} height={50} />
                            <span>Expert cooker</span>
                        </li>
                    </ul>
                </div>
            </div>
        </section>
    )
}